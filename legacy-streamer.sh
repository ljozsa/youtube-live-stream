#!/bin/bash
ffmpeg -i 'mmsh://195.113.161.100:80/tcs-muni-1?MSWMExt=.asf' -vcodec libx264 -preset veryfast -maxrate 1000k -bufsize 6000k -pix_fmt yuv420p -g 50 -acodec libmp3lame -q:a 0 -ac 2 -ar 44100 -strict -2 -f flv rtmp://a.rtmp.youtube.com/live2/51rh-5fbc-9x7d-7xq1
