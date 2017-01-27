#!/usr/bin/python
import libtmux

e104 = ('e104','226.22.36.128:4460','4p3s-bz2a-c9dh-6ws9')
e105 = ('e105','226.22.36.130:4464','rxb4-xtjr-3wwx-0gtq')
a112 = ('a112','226.22.36.134:4472','0k3z-e1zj-jryz-8s9s')
a113 = ('a113','226.22.36.136:4476','fxys-sb7h-pqhu-apg1')
d105_roomcam = ('d105_roomcam','226.22.36.120:4444','f805-1zek-5pws-cdxw')
d105 = ('d105','226.22.36.121:4446','f805-1zek-5pws-cdxw')
d0207 = ('d0207','226.22.36.125:4454','1h7g-axbq-peqp-7g9p')
d0206 = ('d0206','226.22.36.123:4450','1xub-purk-m9uk-2rtu')
e112 = ('e112','226.22.36.127:4458','9up5-w9bc-wchb-cr28')

rooms_to_stream = ( e105, a112, a113, d105, d0207, d0206, e112, e104 )
windows = []

server = libtmux.Server()
session = server.sessions[0]
for room in rooms_to_stream:
    windows.append(session.new_window(attach=False, window_name=room[0]))
    pane = windows[-1].panes[0]
    pane.send_keys('ffmpeg -i udp://' + room[1] + ' -vcodec libx264 -preset veryfast -maxrate 1000k -bufsize 6000k -pix_fmt yuv420p -g 50 -acodec libmp3lame -b:a 128k -ac 2 -ar 44100 -f flv rtmp://a.rtmp.youtube.com/live2/' + room[2], enter=True)
