/***************************************************
//Web: http://www.buydisplay.com
EastRising Technology Co.,LTD
Examples for ER-OLEDM0.95-2C
Display is Hardward SPI 4-Wire SPI Interface 
Tested and worked with: 
Works with Raspberry pi
****************************************************/

#include <bcm2835.h>
#include <stdio.h>
#include <time.h>
#include "ssd1331.h"

char value[10] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
int main(int argc, char **argv)
{
    time_t now;
    struct tm *timenow;
    FILE *pFile ;
    /* 1 pixel of 888 bitmap = 3 bytes */
    size_t pixelSize = 3;
    unsigned char bmpBuffer[OLED_WIDTH * OLED_HEIGHT * 3];

    if(!bcm2835_init())
    {
        return -1;
    }

 


  
    SSD1331_begin();
    SSD1331_mono_bitmap(0, 0, mono_bmp, 96, 64, GREEN);
    SSD1331_display();
    bcm2835_delay(2000);


   
    pFile = fopen("pic1.bmp", "r");

   if (pFile == NULL) {
        printf("file not exist\n");
        return 0;
    }
  
    fseek(pFile, 54, 0);
    fread(bmpBuffer, pixelSize, OLED_WIDTH * OLED_HEIGHT, pFile);
    fclose(pFile);

    SSD1331_bitmap24(0, 0, bmpBuffer, 96, 64);
    SSD1331_display();
    bcm2835_delay(2000);



   pFile = fopen("pic2.bmp", "r");

   if (pFile == NULL) {
        printf("file not exist\n");
        return 0;
    }

    fseek(pFile, 54, 0);
    fread(bmpBuffer, pixelSize, OLED_WIDTH * OLED_HEIGHT, pFile);
    fclose(pFile);

    SSD1331_bitmap24(0, 0, bmpBuffer, 96, 64);
    SSD1331_display();
    bcm2835_delay(2000);

   pFile = fopen("pic3.bmp", "r");

   if (pFile == NULL) {
        printf("file not exist\n");
        return 0;
    }

    fseek(pFile, 54, 0);
    fread(bmpBuffer, pixelSize, OLED_WIDTH * OLED_HEIGHT, pFile);
    fclose(pFile);

    SSD1331_bitmap24(0, 0, bmpBuffer, 96, 64);
    SSD1331_display();
    bcm2835_delay(2000);

   pFile = fopen("pic4.bmp", "r");

   if (pFile == NULL) {
        printf("file not exist\n");
        return 0;
    }

    fseek(pFile, 54, 0);
    fread(bmpBuffer, pixelSize, OLED_WIDTH * OLED_HEIGHT, pFile);
    fclose(pFile);

    SSD1331_bitmap24(0, 0, bmpBuffer, 96, 64);
    SSD1331_display();
    bcm2835_delay(2000);

   pFile = fopen("pic5.bmp", "r");

   if (pFile == NULL) {
        printf("file not exist\n");
        return 0;
    }

    fseek(pFile, 54, 0);
    fread(bmpBuffer, pixelSize, OLED_WIDTH * OLED_HEIGHT, pFile);
    fclose(pFile);

    SSD1331_bitmap24(0, 0, bmpBuffer, 96, 64);
    SSD1331_display();
    bcm2835_delay(2000);


   pFile = fopen("pic6.bmp", "r");

   if (pFile == NULL) {
        printf("file not exist\n");
        return 0;
    }

    fseek(pFile, 54, 0);
    fread(bmpBuffer, pixelSize, OLED_WIDTH * OLED_HEIGHT, pFile);
    fclose(pFile);

    SSD1331_bitmap24(0, 0, bmpBuffer, 96, 64);
    SSD1331_display();
    bcm2835_delay(2000);


    SSD1331_clear();
    printf("OLED example. Press Ctrl + C to exit.\n");
    while(1)
    {
        time(&now);
        timenow = localtime(&now);

        SSD1331_mono_bitmap(0, 2, Signal816, 16, 8, GOLDEN); 
        SSD1331_mono_bitmap(19, 2, Msg816, 16, 8, GOLDEN); 
        SSD1331_mono_bitmap(38, 2, Bluetooth88, 8, 8, GOLDEN); 
        SSD1331_mono_bitmap(52, 2, GPRS88, 8, 8, GOLDEN); 
        SSD1331_mono_bitmap(66, 2, Alarm88, 8, 8, GOLDEN); 
        SSD1331_mono_bitmap(80, 2, Bat816, 16, 8, GOLDEN); 

        SSD1331_string(0, 52, "MUSIC", 12, 0, PINK); 
        SSD1331_string(64, 52, "MENU", 12, 1, GOLDEN); 


        SSD1331_char(0, 16, value[timenow->tm_hour / 10], 12, 1,RED);
        SSD1331_char(14, 16, value[timenow->tm_hour % 10], 12, 1,RED);
        SSD1331_char(26, 16, ':' , 12, 1,WHITE);
        SSD1331_char(38, 16, value[timenow->tm_min / 10], 12, 1, GREEN);
        SSD1331_char(50, 16, value[timenow->tm_min % 10], 12, 1, GREEN);
        SSD1331_char(62, 16, ':' , 12, 1,WHITE);
        SSD1331_char(74, 16, value[timenow->tm_sec / 10], 12, 1, BLUE);
        SSD1331_char(86, 16, value[timenow->tm_sec % 10], 12, 1, BLUE);

        SSD1331_string(6, 32, "buydisplay.com", 12, 1,CYAN);
    
        SSD1331_display();
      
    }
    bcm2835_spi_end();
    bcm2835_close();
    return 0;
}

