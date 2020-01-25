/* This is used to understand GPIO performance if sent 
 * with DMA (which is: too low).
 * It might serve as an educational example though.
 */

#include <assert.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

// Physical Memory Allocation, from raspberrypi/userland demo.
#include "mailbox.h"

// GPIO which we want to toggle in this example.
extern unsigned int TOGGLE_GPIO;

// Raspberry Pi 2 or 1 ? Since this is a simple example, we don't
// bother auto-detecting but have it a compile-time option.
#ifndef PI_VERSION
#  define PI_VERSION 2
#endif

#define BCM2708_PI1_PERI_BASE  0x20000000
#define BCM2709_PI2_PERI_BASE  0x3F000000
#define BCM2711_PI4_PERI_BASE  0xFE000000

// --- General, Pi-specific setup.
#if PI_VERSION == 1
#  define PERI_BASE BCM2708_PI1_PERI_BASE
#elif PI_VERSION == 2 || PI_VERSION == 3
#  define PERI_BASE BCM2709_PI2_PERI_BASE
#else
#  define PERI_BASE BCM2711_PI4_PERI_BASE
#endif

#define PAGE_SIZE 4096

// ---- GPIO specific defines
#define GPIO_REGISTER_BASE 0x200000
#define GPIO_SET_OFFSET 0x1C
#define GPIO_CLR_OFFSET 0x28
#define PHYSICAL_GPIO_BUS (0x7E000000 + GPIO_REGISTER_BASE)

// ---- Memory mappping defines
#define BUS_TO_PHYS(x) ((x)&~0xC0000000)

// ---- Memory allocating defines
// https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface
#define MEM_FLAG_DIRECT           (1 << 2)
#define MEM_FLAG_COHERENT         (2 << 2)
#define MEM_FLAG_L1_NONALLOCATING (MEM_FLAG_DIRECT | MEM_FLAG_COHERENT)

// ---- DMA specific defines
#define DMA_CHANNEL       5   // That usually is free.
#define DMA_BASE          0x007000

// BCM2385 ARM Peripherals 4.2.1.2
#define DMA_CB_TI_NO_WIDE_BURSTS (1<<26)
#define DMA_CB_TI_SRC_INC        (1<<8)
#define DMA_CB_TI_DEST_INC       (1<<4)
#define DMA_CB_TI_TDMODE         (1<<1)

#define DMA_CS_RESET    (1<<31)
#define DMA_CS_ABORT    (1<<30)
#define DMA_CS_DISDEBUG (1<<28)
#define DMA_CS_END      (1<<1)
#define DMA_CS_ACTIVE   (1<<0)

#define DMA_CB_TXFR_LEN_YLENGTH(y) (((y-1)&0x4fff) << 16)
#define DMA_CB_TXFR_LEN_XLENGTH(x) ((x)&0xffff)
#define DMA_CB_STRIDE_D_STRIDE(x)  (((x)&0xffff) << 16)
#define DMA_CB_STRIDE_S_STRIDE(x)  ((x)&0xffff)

#define DMA_CS_PRIORITY(x) ((x)&0xf << 16)
#define DMA_CS_PANIC_PRIORITY(x) ((x)&0xf << 20)

// define the gpio to use
void set_gpio(unsigned int gpio);

// Documentation: BCM2835 ARM Peripherals @4.2.1.2
struct dma_channel_header {
  uint32_t cs;        // control and status.
  uint32_t cblock;    // control block address.
};

// @4.2.1.1
struct dma_cb {    // 32 bytes.
  uint32_t info;   // transfer information.
  uint32_t src;    // physical source address.
  uint32_t dst;    // physical destination address.
  uint32_t length; // transfer length.
  uint32_t stride; // stride mode.
  uint32_t next;   // next control block; Physical address. 32 byte aligned.
  uint32_t pad[2];
};

// A memory block that represents memory that is allocated in physical
// memory and locked there so that it is not swapped out.
// It is not backed by any L1 or L2 cache, so writing to it will directly
// modify the physical memory (and it is slower of course to do so).
// This is memory needed with DMA applications so that we can write through
// with the CPU and have the DMA controller 'see' the data.
// The UncachedMemBlock_{alloc,free,to_physical}
// functions are meant to operate on these.
struct UncachedMemBlock {
  void *mem;                  // User visible value: the memory to use.
  //-- Internal representation.
  uint32_t bus_addr;
  uint32_t mem_handle;
  size_t size;
};

void initialize_gpio_for_output(volatile uint32_t *gpio_registerset, int bit);

/* --------------------------------------------------------------------------
 * In each of the following run_* demos, we have a somewhat repetetive setup
 * for each of these. This is intentional, so that it is easy to read each
 * of these as independent example.
 * --------------------------------------------------------------------------
 */

/*
 * Direct output of data to the GPIO in a tight loop. This is the highest speed
 * it can get.
 */
void run_cpu_direct();

/*
 * Read data from memory and write to GPIO.
 * Memory is organized as 32-Bit data to be written to the GPIO. We expand
 * these using a mask to do the actual set/reset sequence.
 * This is pretty compact in memory and probably the 'usual' way how you
 * would send data to GPIO.
 */
void run_cpu_from_memory_masked();

/*
 * Read data from memory. Memory layout has set/reset already prepared.
 * While this is not necessarily useful for regular processing, it is a
 * good prepatory step to understand the layout in the DMA case.
 */
void run_cpu_from_memory_set_reset();

/*
 * Read data from UNCACHED memory with set/reset.
 * The exact same as the previous example, but different memory to read
 * from: no L1 or L2 cache help with perfomance accessing the memory.
 * This is not useful for anything in real life, but helps to better
 * understand (slow) DMA performance.
 */
void run_cpu_from_uncached_memory_set_reset();

/*
 * Writing data via DMA to GPIO. We do that in a 2D write with a stride that
 * skips the gap between the GPIO registers. Each of these GPIO operations
 * is described as a single control block.
 *
 * This requires a lot of overhead memory for the control blocks (each 8 byte
 * data requires a 32 byte control block). So we use about 40 bytes per
 * one 32-bit set/clear operation.
 */
void run_dma_single_transfer_per_cb();

/*
 * Here, we use a different trick with strides. We set up the source data
 * in a way that it mimicks the layout of the GPIO set/clr registers and
 * copy that from the source to the GPIO registers; we use the destination
 * stride to go _backwards_ to the start of the registers while we keep
 * going reading from the source.
 *
 * There is some stuff between the set and clr we are interested in, which
 * means there are 8 dead bytes between our payload. It means we have to
 * copy more data and waste more data 'setup' area. However, overall, we
 * are using less memory than in the
 */
void run_dma_multi_transfer_per_cb();

int usage(const char *prog);
