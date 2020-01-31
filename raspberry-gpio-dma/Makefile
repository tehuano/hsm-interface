# Overwrite PI-version just when compiling:
# $ PI_VERSION=1 make
PI_VERSION ?= 3

CC= gcc 
CFLAGS= -O3 -W -Wall -std=c99 -D_XOPEN_SOURCE=500 -g -DPI_VERSION=$(PI_VERSION)

all: test_gpio_dma.a gpio_dma.so

test_gpio_dma.a: test_gpio_dma.o gpio_dma.o mailbox.o
	gcc -o test_gpio_dma.a gpio_dma.o test_gpio_dma.o mailbox.o
	chmod +x test_gpio_dma.a

gpio_dma.so: gpio_dma.o mailbox.o
	gcc -fPIC -shared -o gpio_dma.so gpio_dma.o mailbox.o

clean:
	rm -f *.a *.so *.o

