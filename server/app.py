#!/usr/bin/env python

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

async_mode = None

app = Flask(__name__, template_folder='templates', static_folder='static')
socketio = SocketIO(app, async_mode=async_mode)


def emit_infoevent():
    emit('info_event', {'type': '0', 'data': 'UID        PID  PPID  C STIME TTY          TIME CMD \n\
root         1     0  0 20:03 ?        00:00:03 /sbin/init \n\
root         2     0  0 20:03 ?        00:00:00 [kthreadd] \n\
root         4     2  0 20:03 ?        00:00:00 [kworker/0:0H] \n\
root         6     2  0 20:03 ?        00:00:00 [mm_percpu_wq] \n\
root         7     2  0 20:03 ?        00:00:00 [ksoftirqd/0] \n\
root         8     2  0 20:03 ?        00:00:02 [rcu_sched] \n\
root         9     2  0 20:03 ?        00:00:00 [rcu_bh] \n\
root        10     2  0 20:03 ?        00:00:00 [migration/0] \n\
root        11     2  0 20:03 ?        00:00:00 [watchdog/0] \n\
root        12     2  0 20:03 ?        00:00:00 [cpuhp/0] \n\
root        13     2  0 20:03 ?        00:00:00 [cpuhp/1] \n\
root        14     2  0 20:03 ?        00:00:00 [watchdog/1] \n\
root        15     2  0 20:03 ?        00:00:00 [migration/1] \n\
root        16     2  0 20:03 ?        00:00:00 [ksoftirqd/1] \n\
root        18     2  0 20:03 ?        00:00:00 [kworker/1:0H] \n\
root        19     2  0 20:03 ?        00:00:00 [cpuhp/2] \n\
root        20     2  0 20:03 ?        00:00:00 [watchdog/2]'})
    emit('info_event', {'type': '1', 'data': 'Jun 20 22:18:44 WOPR-PC org.freedesktop.thumbnails.Thumbnailer1[2050]: Registered thumbailer gnome-thumbnail-font --size %s %u %o\n\
Jun 20 22:18:44 WOPR-PC org.freedesktop.thumbnails.Thumbnailer1[2050]: Registered thumbailer /usr/bin/gdk-pixbuf-thumbnailer -s %s %u %o\n\
Jun 20 22:18:44 WOPR-PC org.freedesktop.thumbnails.Thumbnailer1[2050]: Registered thumbailer atril-thumbnailer -s %s %u %o\n\
Jun 20 22:18:44 WOPR-PC org.freedesktop.thumbnails.Thumbnailer1[2050]: Registered thumbailer /usr/bin/gdk-pixbuf-thumbnailer -s %s %u %o\n\
Jun 20 22:18:44 WOPR-PC org.freedesktop.thumbnails.Thumbnailer1[2050]: Registered thumbailer gnome-raw-thumbnailer -s %s %u %o\n\
Jun 20 22:18:44 WOPR-PC dbus-daemon[2050]: [session uid=1000 pid=2050] Successfully activated service &apos;org.freedesktop.thumbnails.Thumbnailer1&apos;\n\
Jun 20 22:22:49 WOPR-PC dbus-daemon[2050]: [session uid=1000 pid=2050] Activating via systemd: service name=&apos;org.gnome.Terminal&apos; \n\
Jun 20 22:22:49 WOPR-PC systemd[1999]: Starting GNOME Terminal Server...\n\
Jun 20 22:22:49 WOPR-PC dbus-daemon[2050]: [session uid=1000 pid=2050] Successfully activated service &apos;org.gnome.Terminal&apos;\n\
Jun 20 22:22:49 WOPR-PC systemd[1999]: Started GNOME Terminal Server.'})
    emit('info_event', {'type': '2', 'data': 'Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    \n\
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   \n\
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      -                   \n\
tcp        0      0 192.168.192.21:48978    50.112.34.20:443        ESTABLISHED 3508/firefox        \n\
tcp        0      0 192.168.192.21:43818    216.58.208.106:80       TIME_WAIT   -                   \n\
tcp        0      0 192.168.192.21:43820    216.58.208.106:80       ESTABLISHED 3508/firefox        \n\
tcp6       0      0 ::1:631                 :::*                    LISTEN      -   '})

def emit_logevent():
    emit('log_event', {'host': 'a', 'data': '<pre><font color="#00FF00"><b>Host1</b></font>:<font color="#5C5CFF"><b>~</b></font>$ tail /var/log/syslog\n\
Jun 20 22:18:44 WOPR-PC dbus-daemon[2050]: [session uid=1000 pid=2050] Successfully activated service &apos;org.freedesktop.thumbnails.Thumbnailer1&apos;\n\
Jun 20 22:22:49 WOPR-PC dbus-daemon[2050]: [session uid=1000 pid=2050] Activating via systemd: service name=&apos;org.gnome.Terminal&apos; \n\
Jun 20 22:22:49 WOPR-PC systemd[1999]: Starting GNOME Terminal Server...\n\
Jun 20 22:22:49 WOPR-PC dbus-daemon[2050]: [session uid=1000 pid=2050] Successfully activated service &apos;org.gnome.Terminal&apos;\n\
Jun 20 22:22:49 WOPR-PC systemd[1999]: Started GNOME Terminal Server.\n\
</pre> ', 'clear': 1})

    emit('log_event', {'host': 'b', 'data': '<pre><font color="#00FF00"><b>192.168.1.10</b></font>:<font color="#5C5CFF"><b>~</b></font>$ dmesg | tail\n\
[ 9355.800927] [UFW BLOCK] IN=wlp2s0 OUT= MAC=34:f3:9a:ef:04:52:54:fa:3e:b2:d7:62:08:00 SRC=213.254.244.21 DST=192.168.192.21 LEN=40 TOS=0x00 PREC=0x00 TTL=50 ID=5109 DF PROTO=TCP SPT=443 DPT=38668 WINDOW=0 RES=0x00 RST URGP=0 \n\
[ 9355.801312] [UFW BLOCK] IN=wlp2s0 OUT= MAC=34:f3:9a:ef:04:52:54:fa:3e:b2:d7:62:08:00 SRC=213.254.244.21 DST=192.168.192.21 LEN=40 TOS=0x00 PREC=0x00 TTL=50 ID=5110 DF PROTO=TCP SPT=443 DPT=38668 WINDOW=0 RES=0x00 RST URGP=0 \n\
[ 9356.708626] [UFW BLOCK] IN=wlp2s0 OUT= MAC=34:f3:9a:ef:04:52:54:fa:3e:b2:d7:62:08:00 SRC=185.33.223.216 DST=192.168.192.21 LEN=40 TOS=0x08 PREC=0x20 TTL=53 ID=52265 DF PROTO=TCP SPT=443 DPT=35992 WINDOW=0 RES=0x00 RST URGP=0 \n\
[ 9356.709008] [UFW BLOCK] IN=wlp2s0 OUT= MAC=34:f3:9a:ef:04:52:54:fa:3e:b2:d7:62:08:00 SRC=185.33.223.216 DST=192.168.192.21 LEN=40 TOS=0x08 PREC=0x20 TTL=53 ID=52266 DF PROTO=TCP SPT=443 DPT=35992 WINDOW=0 RES=0x00 RST URGP=0 \n\
[ 9356.852962] [UFW BLOCK] IN=wlp2s0 OUT= MAC=34:f3:9a:ef:04:52:54:fa:3e:b2:d7:62:08:00 SRC=185.33.223.216 DST=192.168.192.21 LEN=40 TOS=0x08 PREC=0x20 TTL=53 ID=52289 DF PROTO=TCP SPT=443 DPT=36070 WINDOW=0 RES=0x00 RST URGP=0 \n\
[ 9356.854299] [UFW BLOCK] IN=wlp2s0 OUT= MAC=34:f3:9a:ef:04:52:54:fa:3e:b2:d7:62:08:00 SRC=185.33.223.216 DST=192.168.192.21 LEN=40 TOS=0x08 PREC=0x20 TTL=53 ID=52290 DF PROTO=TCP SPT=443 DPT=36070 WINDOW=0 RES=0x00 RST URGP=0 \n\
[ 9375.695245] [UFW BLOCK] IN=wlp2s0 OUT= MAC=34:f3:9a:ef:04:52:54:fa:3e:b2:d7:62:08:00 SRC=72.251.245.181 DST=192.168.192.21 LEN=40 TOS=0x00 PREC=0x00 TTL=54 ID=18635 DF PROTO=TCP SPT=443 DPT=46838 WINDOW=0 RES=0x00 RST URGP=0 \n\
[ 9394.486274] [UFW BLOCK] IN=wlp2s0 OUT= MAC=34:f3:9a:ef:04:52:54:fa:3e:b2:d7:62:08:00 SRC=185.33.223.216 DST=192.168.192.21 LEN=40 TOS=0x08 PREC=0x20 TTL=53 ID=56790 DF PROTO=TCP SPT=443 DPT=36346 WINDOW=0 RES=0x00 RST URGP=0 \n\
[ 9440.567993] [UFW BLOCK] IN=wlp2s0 OUT= MAC=34:f3:9a:ef:04:52:54:fa:3e:b2:d7:62:08:00 SRC=37.252.161.184 DST=192.168.192.21 LEN=40 TOS=0x08 PREC=0x20 TTL=53 ID=582 DF PROTO=TCP SPT=443 DPT=41938 WINDOW=0 RES=0x00 RST URGP=0 \n\
[ 9444.206527] [UFW BLOCK] IN=wlp2s0 OUT= MAC=34:f3:9a:ef:04:52:54:fa:3e:b2:d7:62:08:00 SRC=52.17.116.123 DST=192.168.192.21 LEN=40 TOS=0x00 PREC=0x00 TTL=237 ID=11084 DF PROTO=TCP SPT=443 DPT=52198 WINDOW=0 RES=0x00 RST URGP=0 \n\
</pre>', 'clear': 1})
    emit('log_event', {'host': 'a', 'data': 'hello2a', 'clear': 0})

def emit_selecttabevent_byindex(index):
    emit('select_tab_event', {'host_index': index})

def emit_selecttabevent_byname(host):
    emit('select_tab_event', {'host_name': host})

def emit_addhostsevent():
    emit('add_hosts_event', {'hosts': 'a', 'apearance': '1'})
    emit('add_hosts_event', {'hosts': 'b', 'edges': {'from':'a', 'to': 'b'}, 'apearance': '1'})

def emit_updatehostsevent():
    emit('update_hosts_event', {'hosts': 'a', 'apearance': '2'})

def emit_removehostsevent():
    emit('remove_hosts_event', {'hosts': 'a'})


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('get_page_data', namespace='')
def get_page_data(data):
    print "get_page_data"
    emit_removehostsevent()

@socketio.on('get_hosts', namespace='')
def get_page_data(data):
    print "get_hotst"
    emit_addhostsevent() #emit_updatehostsevent()

@socketio.on('get_logging_data', namespace='')
def get_page_data(data):
    print "get_logging_data"
    emit_logevent()

@socketio.on('get_info_data', namespace='')
def get_page_data(data):
    print "get_info_data"
    emit_infoevent()

@socketio.on('set_focus', namespace='')
def get_page_data(data):
    print "set_focus"
    emit_selecttabevent_byindex('0')    #emit_selecttabevent_byname('localhost')

if __name__ == '__main__':
    socketio.run(app, debug=True)
