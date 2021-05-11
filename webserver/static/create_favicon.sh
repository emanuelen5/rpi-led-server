#!/usr/bin/env bash

for size in 16 32 48 ; do
    convert \
        -background lightgray \
        -fill black \
        -resize ${size}x${size} \
        -gravity center \
        -bordercolor black \
        -border 1 \
        rpi.svg \
        icon_${size}.bmp;
done

convert icon_*.bmp favicon.ico