E105_MCAST=226.22.36.130:4464
E105_YT=redhatczech-6420.z4c1-2mu7-xves-fjx8
A112_MCAST=226.22.36.134:4472
A112_YT=redhatczech-6420.ppeu-y6m0-db0s-0br7
A113_MCAST=226.22.36.136:4476
A113_YT=redhatczech-6420.9ugj-rq34-96k0-6kjj
D105_PRES_MCAST=226.22.36.120:4444
D105_PRES_YT=redhatczech-6420.abwy-9fs2-9sgk-8wuw
D105_MCAST=226.22.36.121:4446
D105_YT=redhatczech-6420.yhah-f4pt-y2rj-4uc2
D0207_MCAST=226.22.36.125:4454
D0207_YT=redhatczech-6420.yjbx-wtkq-p5vz-exfm
D0206_MCAST=226.22.36.123:4450
D0206_YT=redhatczech-6420.6975-9g70-13e5-6vww
E112_MCAST=226.22.36.127:4458
E112_YT=redhatczech-6420.q3xu-jpus-a8mg-55jx
E104_MCAST=226.22.36.128:4460
E104_YT=redhatczech-6420.zsta-xckx-vyj2-6vkw

ffmpeg -i udp:// -vcodec libx264 -preset veryfast -maxrate 1000k -bufsize 6000k -pix_fmt yuv420p -g 50 -acodec libmp3lame -b:a 128k -ac 2 -ar 44100 -f flv rtmp://a.rtmp.youtube.com/live2/
