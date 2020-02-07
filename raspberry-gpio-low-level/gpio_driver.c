#include "gpio_driver.h"

int  mem_fd;
void *gpio_map;
volatile unsigned *gpio;

unsigned char gpio_bus[GPIO_BUS_SIZE] = {24, 4, 17, 22, 9, 25, 18, 23};
unsigned char clock_pin = 8;
unsigned char key_pin = 10;
unsigned char bus_dir_pin = 21;
unsigned initialized = 0x00;

// Set up a memory regions to access GPIO
void setup_io() {
   /* open /dev/mem */
   if ((mem_fd = open("/dev/mem", O_RDWR|O_SYNC) ) < 0) {
      printf("can't open /dev/mem \n");
      exit(-1);
   }
   /* mmap GPIO */
   gpio_map = mmap(
      NULL,             //Any adddress in our space will do
      BLOCK_SIZE,       //Map length
      PROT_READ|PROT_WRITE,// Enable reading & writting to mapped memory
      MAP_SHARED,       //Shared with other processes
      mem_fd,           //File to map
      GPIO_BASE         //Offset to GPIO peripheral
   );
   close(mem_fd); //No need to keep mem_fd open after mmap
   if (gpio_map == MAP_FAILED) {
      printf("mmap error %d\n", (int)gpio_map);//errno also set!
      exit(-1);
   }
   // Always use volatile pointer!
   gpio = (volatile unsigned *)gpio_map;
   initialized = 0x01;
} // setup_io

void send_key_byte(unsigned char value) {
    int i = 0;
    if (0x00 == initialized) {
        init();
    }        
    GPIO_CLR = 1 << clock_pin;
    GPIO_SET = 1 << bus_dir_pin;
    GPIO_SET = 1 << key_pin;
    for(i = 0; i < GPIO_BUS_SIZE; i++) {
        INP_GPIO(gpio_bus[i]); 
        OUT_GPIO(gpio_bus[i]);
        if (0x01 == ((value >> i) & 0x01)) {
            GPIO_SET = 1 << gpio_bus[i];
        } else {
            GPIO_CLR = 1 << gpio_bus[i];
        }
    }
    usleep(CLK_DELAY);
    GPIO_SET = 1 << clock_pin;
    usleep(CLK_DELAY);
    GPIO_CLR = 1 << clock_pin;
    GPIO_CLR = 1 << bus_dir_pin;
    GPIO_CLR = 1 << key_pin;
    usleep(CLK_DELAY);
    printf("Out: %x\n", value);
}

void send_data_byte(unsigned char value) {
    int i = 0;
    if (0x00 == initialized) {
        init();
    }        
    GPIO_CLR = 1 << clock_pin;
    GPIO_SET = 1 << bus_dir_pin;
    for(i = 0; i < GPIO_BUS_SIZE; i++) {
        INP_GPIO(gpio_bus[i]); 
        OUT_GPIO(gpio_bus[i]);
        if (0x01 == ((value >> i) & 0x01)) {
            GPIO_SET = 1 << gpio_bus[i];
        } else {
            GPIO_CLR = 1 << gpio_bus[i];
        }
    }
    usleep(CLK_DELAY);
    GPIO_SET = 1 << clock_pin;
    usleep(CLK_DELAY);
    GPIO_CLR = 1 << clock_pin;
    GPIO_CLR = 1 << bus_dir_pin;
    usleep(CLK_DELAY);
    printf("Out: %x\n", value);
}

unsigned char get_byte() {
    unsigned char value = 0x00;
    int i = 0;
    if (0x00 == initialized) {
        init();
    }        
    GPIO_CLR = 1 << bus_dir_pin;
    GPIO_SET = 1 << clock_pin;
    usleep(CLK_DELAY);
    for(i = 0; i < GPIO_BUS_SIZE; i++) {
        INP_GPIO(gpio_bus[i]);
        if (GET_GPIO(gpio_bus[i])) {
            value |= 1 << i;
        }
    }
    GPIO_CLR = 1 << clock_pin;
    usleep(CLK_DELAY);
    printf("In: %x\n", value);
    return value;
}

void init(){
    setup_io();
    INP_GPIO(clock_pin); 
    OUT_GPIO(clock_pin);
    INP_GPIO(key_pin); 
    OUT_GPIO(key_pin);
    INP_GPIO(bus_dir_pin); 
    OUT_GPIO(bus_dir_pin); 
    printf("Driver initialized\n");
}
