#include <stdio.h>
#include "ssd1331.h"
#include "fonts.h"

char buffer[OLED_WIDTH * OLED_HEIGHT * 2];

void SSD1331_begin() {
};
void SSD1331_display() {
};
void SSD1331_clear() {
};
void SSD1331_pixel(int x,int y, char color) {
};
void SSD1331_mono_bitmap(uint8_t x, uint8_t y, const uint8_t *pBmp, char chWidth, char chHeight, uint16_t hwColor) {
};
void SSD1331_bitmap24(uint8_t x, uint8_t y, uint8_t *pBmp, char chWidth, char chHeight) {
};
void SSD1331_string(uint8_t x, uint8_t y, const char *pString, uint8_t Size, uint8_t Mode, uint16_t hwColor) {
};
void SSD1331_char1616(uint8_t x, uint8_t y, uint8_t chChar, uint16_t hwColor) {
};
void SSD1331_char3216(uint8_t x, uint8_t y, uint8_t chChar, uint16_t hwColor) {
};
void SSD1331_char(uint8_t x, uint8_t y, char acsii, char size, char mode, uint16_t hwColor) {
};
void SSD1331_clear_screen(uint16_t hwColor) {
};
void SSD1331_draw_point(int chXpos, int chYpos, uint16_t hwColor) {
};
