#!/usr/bin/env bash

set -e

folder=$(basename $1)
echo "Processing the service in ./$folder/output"
echo
ffmpeg -i "./$folder/output/Worship $folder.mp4" "./$folder/output/$folder Service Audio.mp3"
echo
echo "Opening './$folder/output/$folder Service Audio.mp3' in Audacity..."
open -a Audacity "./$folder/output/$folder Service Audio.mp3"
