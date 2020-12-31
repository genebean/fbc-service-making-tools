#!/usr/bin/env bash

set -e

folder=$(basename $1)
echo "Processing the service in ./$folder/output"

file_size=$(ls -lh $folder/output/*Audio.mp3| tr -s ' ' |cut -d ' ' -f 5)
number=$(expr $(echo $file_size | sed 's/M//') / 10 + 1)
echo
echo "Splitting $file_size file into $number parts..."
echo
mp3splt -S $number -d $folder/split -o @f_@n $folder/output/$folder\ Service\ Audio.mp3
echo
echo 'Splitting complete, starting ./fbc-mp3-mailer.py'
echo
./fbc-mp3-mailer.py -d $folder/split -c $number
