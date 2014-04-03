#!/bin/bash

rm -rf cards
mkdir -p cards
cd cards
mkdir -p output

wget "http://vectorized-playing-cards.googlecode.com/files/SVG_and_EPS_Vector_Playing_Cards_Version_1.3.zip"
unzip -u "SVG_and_EPS_Vector_Playing_Cards_Version_1.3.zip"

for SVG in `find "SVG_Vector_Playing_Cards_Version_1.3/52-Individual-Color-Vector-Playing_Cards-1.3_(SVG-Format_No_Crop_Marks)" -iname *.svg`
do
    PNG=`basename "$SVG" | sed -e 's/svg/png/g'`
    convert +antialias -background none "$SVG" -crop 228x316+258+368 -resize 123x170 output/"$PNG"
done

SVG="SVG_Vector_Playing_Cards_Version_1.3/Backs_and_pips_1.3_(No_Crop_Marks)/Blue_Back.svg"
convert +antialias -background none "$SVG" -crop 228x316+258+368 -resize 123x170 output/back.png

cp output/*.png ../../dealer/static/img/cards
cd ..
rm -rf cards
