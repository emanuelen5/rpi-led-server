# Creating recording with ffmpeg
```bash
ffmpeg.exe -ss 3.6 -to 33 -i 2021-04-04_17-37-39.mkv -filter:v "crop=1050:800:170:150" -vol 0 output.mp4 -y
```