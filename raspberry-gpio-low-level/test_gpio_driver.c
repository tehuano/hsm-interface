#include "gpio_driver.h"

int main(int argc, char *argv[]) {
  int g,rep;
  // Set up gpi pointer for direct register access
  setup_io();
  // Switch GPIO 7..11 to output mode

  /************************************************************************\
   * You are about to change the GPIO settings of your computer.          *
   * Mess this up and it will stop working!                               *
   * It might be a good idea to 'sync' before running this program        *
   * so at least you still have your code changes written to the SD-card! *
  \************************************************************************/
  printf("Running => Arguments: %d, Program: %s\n", argc, argv[0]);
  // Set GPIO pins 7-11 to output
  for (g = 0; g < GPIO_BUS_SIZE; g++) {
    INP_GPIO(gpio_bus[g]); // must use INP_GPIO before we can use OUT_GPIO
    OUT_GPIO(gpio_bus[g]);
  }

  for (rep=0; rep<10; rep++)
  {
     for (g=0; g< GPIO_BUS_SIZE; g++)
     {
       GPIO_SET = gpio_bus[g];
       sleep(1);
     }
     for (g=0; g<GPIO_BUS_SIZE; g++)
     {
       GPIO_CLR = 1<<gpio_bus[g];
       sleep(1);
     }
  }

  return 0;

} // main
