# FBC Service Making tools

The tools in this repo are used to simplify processes used while having services online.
## Getting audio to Kiss 102.7

1. Run `./create-mp3.sh` and pass it the folder with this weeks bits in it
2. Verify there are no spikes in the audio from the service
3. Run `./split-and-send.sh` and pass it the same folder

## Preparing to use these tools

- `brew install ffmpeg mp3split python`
- install Audacity with ffmpeg https://www.audacityteam.org/download/mac/
