#!/bin/sh

function usage() {
	echo "$0 input output" >&2
	exit -1
}

if [ $# -lt 2 ]; then
	usage
fi

# See: http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html and https://superuser.com/a/556031/585199
palette="/tmp/palette.png"

filters="fps=20"

ffmpeg -v warning -i $1 -vf "$filters,palettegen" -y $palette
ffmpeg -v warning -i $1 -i $palette -lavfi "$filters [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=1" -y $2

echo "File size:"
echo $(du -sh $2)
