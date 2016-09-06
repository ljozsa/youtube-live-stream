#!/usr/bin/python
import libtmux

e105 = ('e105','226.22.36.130:4464','redhatczech-6420.z4c1-2mu7-xves-fjx8')
a112 = ('a112','226.22.36.134:4472','redhatczech-6420.ppeu-y6m0-db0s-0br7')
a113 = ('a113','226.22.36.136:4476','redhatczech-6420.9ugj-rq34-96k0-6kjj')
d105_roomcam = ('d105_roomcam','226.22.36.120:4444','redhatczech-6420.abwy-9fs2-9sgk-8wuw')
d105 = ('d105','226.22.36.121:4446','redhatczech-6420.yhah-f4pt-y2rj-4uc2')
d0207 = ('d0207','226.22.36.125:4454','redhatczech-6420.yjbx-wtkq-p5vz-exfm')
d0206 = ('d0206','226.22.36.123:4450','redhatczech-6420.6975-9g70-13e5-6vww')
e112 = ('e112','226.22.36.127:4458','redhatczech-6420.q3xu-jpus-a8mg-55jx')
e104 = ('e104','226.22.36.128:4460','redhatczech-6420.zsta-xckx-vyj2-6vkw')

rooms_to_stream = ( e105, a112, a113, d105_roomcam, d105, d0207, d0206, e112, e104 )
windows = []

server = libtmux.Server()
session = server.sessions[0]
for room in rooms_to_stream:
    windows.append(session.new_window(attach=False, window_name=room[0]))
    pane = windows[-1].panes[0]
    pane.send_keys('ffmpeg -i udp://' + room[1] + ' -vcodec libx264 -preset veryfast -maxrate 1000k -bufsize 6000k -pix_fmt yuv420p -g 50 -acodec libmp3lame -b:a 128k -ac 2 -ar 44100 -f flv rtmp://a.rtmp.youtube.com/live2/' + room[2], enter=True)
