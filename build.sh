#!/usr/bin/env bash

# Descarga FFmpeg versión estática
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o ffmpeg.tar.xz

# Extrae y mueve solo el ejecutable
tar -xf ffmpeg.tar.xz
mv ffmpeg-*-amd64-static/ffmpeg ffmpeg
chmod +x ffmpeg

# Lo pone en un directorio accesible
mkdir -p ~/.local/bin
mv ffmpeg ~/.local/bin/
