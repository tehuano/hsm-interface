# Overwrite PI-version just when compiling:
# $ PI_VERSION=1 make
PI_VERSION ?= 2

CFLAGS=-O3 -W -Wall -std=c99 -D_XOPEN_SOURCE=500 -g -DPI_VERSION=$(PI_VERSION)

test_gpio_dma: test_gpio_dma.o mailbox.o

clean:
	rm -f test_gpio_dma *.o

