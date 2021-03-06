#include <bcm2835.h>
#include <stdio.h>
#include "ssd1331.h"
#include "fonts.h"

void command(char cmd) {
    bcm2835_gpio_write(DC, LOW);
    bcm2835_spi_transfer(cmd);
}

void SSD1331_begin()
{
    bcm2835_gpio_fsel(RST, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(DC, BCM2835_GPIO_FSEL_OUTP);

    bcm2835_spi_begin();
    bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);     //The default
    bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);                  //The default
    bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_64);  //The default
    bcm2835_spi_chipSelect(BCM2835_SPI_CS0);                     //The default
    bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW);     //the default

    bcm2835_gpio_write(RST, HIGH);
    bcm2835_delay(10);
    bcm2835_gpio_write(RST, LOW);
    bcm2835_delay(10);
    bcm2835_gpio_write(RST, HIGH);

    command(DISPLAY_OFF);          //Display Off
    command(SET_CONTRAST_A);       //Set contrast for color A
    command(0xFF);                     //145 0x91
    command(SET_CONTRAST_B);       //Set contrast for color B
    command(0xFF);                     //80 0x50
    command(SET_CONTRAST_C);       //Set contrast for color C
    command(0xFF);                     //125 0x7D
    command(MASTER_CURRENT_CONTROL);//master current control
    command(0x06);                     //6
    command(SET_PRECHARGE_SPEED_A);//Set Second Pre-change Speed For ColorA
    command(0x64);                     //100
    command(SET_PRECHARGE_SPEED_B);//Set Second Pre-change Speed For ColorB
    command(0x78);                     //120
    command(SET_PRECHARGE_SPEED_C);//Set Second Pre-change Speed For ColorC
    command(0x64);                     //100
    command(SET_REMAP);            //set remap & data format
    command(0x72);                     //0x72              
    command(SET_DISPLAY_START_LINE);//Set display Start Line
    command(0x0);
    command(SET_DISPLAY_OFFSET);   //Set display offset
    command(0x0);
    command(NORMAL_DISPLAY);       //Set display mode
    command(SET_MULTIPLEX_RATIO);  //Set multiplex ratio
    command(0x3F);
    command(SET_MASTER_CONFIGURE); //Set master configuration
    command(0x8E);
    command(POWER_SAVE_MODE);      //Set Power Save Mode
    command(0x00);                     //0x00
    command(PHASE_PERIOD_ADJUSTMENT);//phase 1 and 2 period adjustment
    command(0x31);                     //0x31
    command(DISPLAY_CLOCK_DIV);    //display clock divider/oscillator frequency
    command(0xF0);
    command(SET_PRECHARGE_VOLTAGE);//Set Pre-Change Level
    command(0x3A);
    command(SET_V_VOLTAGE);        //Set vcomH
    command(0x3E);
    command(DEACTIVE_SCROLLING);   //disable scrolling
    command(NORMAL_BRIGHTNESS_DISPLAY_ON);//set display on
}

void SSD1331_end() {
	bcm2835_spi_end();
}

void SSD1331_display(char *buffer) {
    command(SET_COLUMN_ADDRESS);
    command(0);         //cloumn start address
    command(OLED_WIDTH - 1); //cloumn end address
    command(SET_ROW_ADDRESS);
    command(0);         //page atart address
    command(OLED_HEIGHT - 1); //page end address
    bcm2835_gpio_write(DC, HIGH);
    bcm2835_spi_transfern(buffer, OLED_WIDTH * OLED_HEIGHT * 2);
}
