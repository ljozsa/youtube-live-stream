#!/usr/bin/python
import libtmux

e104 = ('e104','226.22.36.128:4460','zm60-ghd6-thr6-7ux8')
e105 = ('e105','226.22.36.130:4464','p0jv-pkv1-pdfm-1p36')
d105_roomcam = ('d105_roomcam','226.22.36.120:4444','e3w1-59rg-rdp5-bckd')
d105 = ('d105','226.22.36.121:4446','acgx-2290-9h8t-8k37')
d0207 = ('d0207','226.22.36.125:4454','vv1q-7byg-h66b-a7yu')
d0206 = ('d0206','226.22.36.123:4450','atf8-7mh4-294k-780f')
e112 = ('e112','226.22.36.127:4458','t04h-rzud-ux8j-15g6')
g202 = ('g202','226.22.36.132:4468','m3mt-udve-5tbz-6yks')

rooms_to_stream = ( d105_roomcam, e104, e105, d105, d0207, d0206, e112, g202 )
windows = []

server = libtmux.Server()
session = server.sessions[0]
for room in rooms_to_stream:
    windows.append(session.new_window(attach=False, window_name=room[0]))
    pane = windows[-1].panes[0]
    pane.send_keys('ffmpeg -i udp://' + room[1] + ' -vcodec libx264 -preset veryfast -maxrate 1000k -bufsize 6000k -pix_fmt yuv420p -g 50 -acodec libmp3lame -b:a 128k -ac 2 -ar 44100 -f flv rtmp://a.rtmp.youtube.com/live2/' + room[2], enter=True)
