#include "gpio_dma.h"

int main(int argc, char *argv[]) {
  if (argc != 2) {
    return usage(argv[0]);
  }

  switch (atoi(argv[1])) {
  case 1:
    run_cpu_direct();
    break;
  case 2:
    run_cpu_from_memory_masked();
    break;
  case 3:
    run_cpu_from_memory_set_reset();
    break;
  case 4:
    run_cpu_from_uncached_memory_set_reset();
    break;
  case 5:
    run_dma_single_transfer_per_cb();
    break;
  case 6:
    run_dma_multi_transfer_per_cb();
    break;
  default:
    return usage(argv[0]);
  }
  return 0;
}

