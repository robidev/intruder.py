#!/usr/bin/env python3
#sanic???
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

import socket
import json
import compose
import subprocess

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

@socketio.on('start_level', namespace='')
def start_level(data):
  print("starting level")
  ret = subprocess.check_output(['docker-compose', '-f', '/levels/docker-compose.sheep.yml', 'up', '-d'])
  print(ret)

@socketio.on('stop_level', namespace='')
def stop_level(data):
  print("stopping level")
  ret = subprocess.check_output(['docker-compose', '-f', '/levels/docker-compose.sheep.yml', 'down'])
  print(ret)

@socketio.on('reset_level', namespace='')
def reset_level(data):
  print("resetting level")
  stop_level(data)
  get_page_data(data)
  start_level(data)

@socketio.on('deploy', namespace='')
def deploy(data):
  print("deploying intruder.py on sheep")
  #copy file (volume copy, html post, tcp post, ssh upload)
  #ret = subprocess.check_output(['docker', 'cp', 'foo.py', 'levels_sheep1_1:/foo.py'])
  #execute file (file watch, html post, tcp post, ssh command)
  #ret = subprocess.check_output(['docker', 'exec', 'levels_sheep1_1', 'python', '/foo.py'])
  

@socketio.on('set_focus', namespace='')
def get_page_data5(data):
  global focus
  focus = data
  emit_selecttabevent_byname(data)


def worker():
  global focus
  socketio.sleep(tick)
  UDP_IP = "0.0.0.0"
  UDP_PORT = 10514
  sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
  sock.setblocking(False)
  sock.bind((UDP_IP, UDP_PORT))
  while True:
    socketio.sleep(tick)
    try:
      data, addr = sock.recvfrom(65356) # buffer size is 64k bytes
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

