#!/usr/bin/env python
#sanic???
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

import socket
import json
import compose

#import webbrowser

thread = None
tick = 0.001
focus = ''

async_mode = None

app = Flask(__name__, template_folder='templates', static_folder='static')
socketio = SocketIO(app, async_mode=async_mode)


def emit_infoevent(type, data):
  emit('info_event', {'type': type, 'data': data})

def emit_selecttabevent_byindex(index):
  emit('select_tab_event', {'host_index': index})

def emit_selecttabevent_byname(host):
  emit('select_tab_event', {'host_name': host})

#####################################
def emit_addhostsevent():
  emit('add_hosts_event', {'hosts': 'a', 'apearance': '1'})
  emit('add_hosts_event', {'hosts': 'b', 'edges': {'from':'a', 'to': 'b'}, 'apearance': '1'})

def emit_updatehostsevent():
  emit('update_hosts_event', {'hosts': 'a', 'apearance': '2'})

def emit_removehostsevent():
  emit('remove_hosts_event', {'hosts': 'a'})
######################################

@app.route('/')
def index():
  return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('get_page_data', namespace='')
def get_page_data(data):
  print("get_page_data")

@socketio.on('get_hosts', namespace='')
def get_page_data2(data):
  print("get_host")

@socketio.on('get_logging_data', namespace='')
def get_page_data3(data):
  print("get_logging_data")

@socketio.on('get_info_data', namespace='')
def get_page_data4(data):
  print("get_info_data")

@socketio.on('set_focus', namespace='')
def get_page_data5(data):
  global focus
  print("set_focus to '%s'" % data)
  focus = data
  emit_selecttabevent_byname(data)


def worker():
  global focus
  socketio.sleep(tick)
  UDP_IP = "0.0.0.0"
#  UDP_IP = "172.16.0.1"
#  UDP_IP = "192.168.192.21"
#  UDP_IP = "127.0.0.1"
  UDP_PORT = 10514
  sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
  sock.setblocking(False)
  sock.bind((UDP_IP, UDP_PORT))
  while True:
    socketio.sleep(tick)
    try:
      data, addr = sock.recvfrom(65356) # buffer size is 1024 bytes
      if data:
        loaded_json = json.loads(data)
        if loaded_json['event']=='info_event':
          if loaded_json['data']['host']==focus:
            socketio.emit('info_event', {'type': loaded_json['data']['type'], 'data': loaded_json['data']['data']})
        else:
          socketio.emit(loaded_json['event'], loaded_json['data'])
    except socket.error as msg:
      pass


@socketio.on('connect', namespace='')
def test_connect():
  global thread
  if thread is None:
    thread = socketio.start_background_task(target=worker)

if __name__ == '__main__':
  socketio.run(app, debug=True)

