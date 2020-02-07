# Overwrite PI-version just when compiling:
# $ PI_VERSION=1 make
PI_VERSION ?= 3

CC= gcc 
CFLAGS= -O3 -W -Wall -std=c99 -D_XOPEN_SOURCE=500 -g -DPI_VERSION=$(PI_VERSION)

all: test_gpio_driver.a gpio_driver.so

test_gpio_driver.a: test_gpio_driver.o gpio_driver.o 
	gcc -o test_gpio_driver.a gpio_driver.o test_gpio_driver.o 
	chmod +x test_gpio_driver.a

gpio_driver.so: gpio_driver.o 
	gcc -fPIC -shared -o gpio_driver.so gpio_driver.o
	chmod +x gpio_driver.so
	mv gpio_driver.so ../lib
clean:
	rm -f *.a *.so *.o

