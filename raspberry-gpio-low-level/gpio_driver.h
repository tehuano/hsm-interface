// Memory Mapped GPIO example
// mmgpio.cpp
//http:elinux.org/RPi_GPIO_Code_Samples
//
// How to access GPIO registers from C-code on the Raspberry-Pi
// Example program
// 15-January-2012
// Dom and Gert
// Revised: 15-Feb-2013

// Raspberry Pi 1, Raspberry Pi 2, or Raspberry Pi 3

//#define BCM2708_PERI_BASE 0x20000000 /* Pi 1 */
#define BCM2708_PERI_BASE 0x3F000000 /* Pi 2 & Pi 3 */

#define GPIO_BASE (BCM2708_PERI_BASE + 0x200000) /* GPIO controller */


#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

#define PAGE_SIZE (4*1024)
#define BLOCK_SIZE (4*1024)

#define GPIO_BUS_SIZE 8
#define CLK_DELAY  10

extern int  mem_fd;
extern void *gpio_map;

// I/O access
extern volatile unsigned *gpio;
extern unsigned char gpio_bus[GPIO_BUS_SIZE];

// GPIO setup macros. Always use INP_GPIO(x) before using OUT_GPIO(x) or SET_GPIO_ALT(x,y)
#define INP_GPIO(g) *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g) *(gpio+((g)/10)) |= (1<<(((g)%10)*3))
#define SET_GPIO_ALT(g,a) *(gpio+(((g)/10))) |= (((a)<=3?(a)+4:(a)==4?3:2)<<(((g)%10)*3))

#define GPIO_SET *(gpio+7) // sets bits which are 1 ignores bits which are 0
#define GPIO_CLR *(gpio+10) // clears bits which are 1 ignores bits which are 0

#define GET_GPIO(g) (*(gpio+13)&(1<<g)) // 0 if LOW, (1<<g) if HIGH

#define GPIO_PULL *(gpio+37) // Pull up/pull down
#define GPIO_PULLCLK0 *(gpio+38) // Pull up/pull down clock

// this function prints to a register
unsigned char read_byte();
// this function sends a data to the gpio
void send_key_byte(unsigned char byte);
void send_data_byte(unsigned char byte);
// this function initializes the gpio ports
void init();
// Set up a memory regions to access GPIO
void setup_io();
