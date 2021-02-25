#ifndef _BCM2835_H_
#define _BCM2835_H_

#define HIGH 1
#define LOW 0

#define BCM2835_SPI_CS0 0
#define BCM2835_SPI_CLOCK_DIVIDER_64 0
#define BCM2835_SPI_MODE0 0
#define BCM2835_SPI_BIT_ORDER_MSBFIRST 0
#define BCM2835_GPIO_FSEL_OUTP 0

static void bcm2835_delay(int a) {};
static void bcm2835_gpio_fsel(int a, int b) {};
static void bcm2835_gpio_write(int a, int b) {};
static void bcm2835_spi_begin(void) {};
static void bcm2835_spi_chipSelect(int a) {};
static void bcm2835_spi_setBitOrder(int a) {};
static void bcm2835_spi_setChipSelectPolarity(int a, int b) {};
static void bcm2835_spi_setClockDivider(int a) {};
static void bcm2835_spi_setDataMode(int a) {};
static void bcm2835_spi_transfer(int a) {};
static void bcm2835_spi_transfern(char *a, int b) {};

#endif