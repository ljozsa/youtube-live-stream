ffmpeg -i udp://239.1.1.1:11111 -vcodec libx264 -preset veryfast -maxrate 1000k -bufsize 6000k -pix_fmt yuv420p -g 50 -acodec libmp3lame -b:a 128k -ac 2 -ar 44100 -f flv rtmp://a.rtmp.youtube.com/live2/l.jozsa.rh76-djc7-6jc4-1wc2
