#!/usr/bin/python
import libtmux

e104 = ('e104','226.22.36.128:4460','cwvh-93gs-bw3d-b7f5')
e105 = ('e105','226.22.36.130:4464','e8qp-adsv-0yp0-0u2q')
d105_roomcam = ('d105_roomcam','226.22.36.120:4444','r7ms-08jq-d9bj-e2au')
d105 = ('d105','226.22.36.121:4446','8ddp-qzts-2x4z-df0u')
d0207 = ('d0207','226.22.36.125:4454','5w38-h1ty-1gy2-2ttr')
d0206 = ('d0206','226.22.36.123:4450','a4wa-b3rr-gkdr-56ss')
e112 = ('e112','226.22.36.127:4458','cmfe-ej05-d9v3-7aje')
g202 = ('g202','226.22.36.132:4468','zsxz-6137-69xv-67h0')

rooms_to_stream = ( d105_roomcam, e104, e105, d105, d0207, d0206, e112, g202 )
windows = []

server = libtmux.Server()
session = server.sessions[0]
for room in rooms_to_stream:
    windows.append(session.new_window(attach=False, window_name=room[0]))
    pane = windows[-1].panes[0]
    pane.send_keys('ffmpeg -i udp://' + room[1] + ' -vcodec libx264 -preset veryfast -maxrate 1000k -bufsize 6000k -pix_fmt yuv420p -g 50 -acodec libmp3lame -b:a 128k -ac 2 -ar 44100 -f flv rtmp://a.rtmp.youtube.com/live2/' + room[2], enter=True)
