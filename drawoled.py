import oled
from datetime import datetime

if __name__=="__main__":
    oled.init()
    oled.clear()
    while True:
        oled.string(0, 16, datetime.now().strftime("%Y-%m-%d %H:%M"), color=(255, 0, 0))
        oled.display()

# int main(int argc, char **argv)
# {
#     if(!bcm2835_init())
#     {
#         return -1;
#     }
#
#     SSD1331_begin();
#     SSD1331_clear();
#     printf("OLED example. Press Ctrl + C to exit.\n");
#     while(1)
#     {
#         struct timeval tv;
#         struct tm *timenow;
#
#         gettimeofday(&tv, NULL);
#         timenow = localtime(&tv.tv_sec);
#
#         char str_buf[50];
#         sprintf(str_buf, "%02d", timenow->tm_hour);
#         SSD1331_string(0, 16, str_buf, 12, 1, RED);
#         SSD1331_char(26, 16, ':' , 12, 1,WHITE);
#         sprintf(str_buf, "%02d", timenow->tm_min);
#         SSD1331_string(38, 16, str_buf, 12, 1, GREEN);
#         SSD1331_char(62, 16, ':' , 12, 1,WHITE);
#         sprintf(str_buf, "%02d", timenow->tm_sec);
#         SSD1331_string(74, 16, str_buf, 12, 1, BLUE);
#         SSD1331_char(14, 32, '.' , 12, 1,WHITE);
#         sprintf(str_buf, "%06ld", tv.tv_usec);
#         SSD1331_string(26, 32, str_buf, 12, 1, PURPLE);
#
#         SSD1331_string(6, 46, "emaus demo", 12, 1, CYAN);
#
#         SSD1331_display();
#
#     }
#     bcm2835_spi_end();
#     bcm2835_close();
#     return 0;
# }