#!/usr/bin/env python3
from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, emit
from werkzeug import secure_filename

import socket
import json
import compose
import subprocess
import paramiko
import time

thread = None
tick = 0.001
focus = ''
hosts_info = {}

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
def emit_removehostsevent(host):
  emit('remove_hosts_event', {'hosts': 'host'})
######################################

@app.route('/')
def index():
  return render_template('index.html', async_mode=socketio.async_mode)
	
@app.route('/uploader', methods = ['POST'])
def uploader():
  if request.method == 'POST':
    try:
      f = request.files['file']
      #f.save(secure_filename(f.filename))
      f.save(secure_filename('intruder.py'))
      deploy("")
      return "Success"
    except Exception as Err:
      f = None
      print(Err)
      return "Error"#redirect(url_for('index'))

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
  print("deploying intruder.py on sheep1")
  #copy file (volume copy, html post, tcp post, ssh upload)
  ret = subprocess.check_output(['docker', 'cp', 'intruder.py', 'sheep1:/intruder.py'])
  #execute file (file watch, html post, tcp post, ssh command)
  ret = subprocess.check_output(['docker', 'exec', 'sheep1', 'python', '/intruder.py'])
  

@socketio.on('set_focus', namespace='')
def set_focus(data):
  global focus
  global hosts_info
  focus = data
  if focus in hosts_info:
    if '0' in hosts_info[focus]:
      socketio.emit('info_event', {'type': '0', 'data': hosts_info[focus]['0']})
    if '1' in hosts_info[focus]:
      socketio.emit('info_event', {'type': '1', 'data': hosts_info[focus]['1']})
    if '2' in hosts_info[focus]:
      socketio.emit('info_event', {'type': '2', 'data': hosts_info[focus]['2']})
    if '3' in hosts_info[focus]:
      socketio.emit('info_event', {'type': '3', 'data': hosts_info[focus]['3']})

  emit_selecttabevent_byname(data)

def process_info_event(loaded_json):
  global focus
  global hosts_info
  ihost = loaded_json['data']['host']
  itype = loaded_json['data']['type']
  idata = loaded_json['data']['data']

  if ihost not in hosts_info:
    hosts_info[ihost] = {}
    hosts_info[ihost]['online'] = True
    hosts_info[ihost]['compromised'] = False
    socketio.emit('add_hosts_event', {'hosts': ihost, 'apearance': '1'})

  if hosts_info[ihost]['online'] == False:
    hosts_info[ihost]['online'] = True

  if hosts_info[ihost]['compromised'] == False:
    socketio.emit('update_hosts_event', {'hosts': ihost, 'apearance': '1'})
  else:
    socketio.emit('update_hosts_event', {'hosts': ihost, 'apearance': '2'})

  hosts_info[ihost]['last'] = time.time()
  hosts_info[ihost][itype] = idata
  if ihost==focus:
    socketio.emit('info_event', {'type': itype, 'data': idata})

def validate_flag(ihost,flag):
  #todo: find a way for custom level definitions: host, flag, win_msg, maybe from YML file?
  host = 'sheep3'
  win_flag = '0123456789'
  win_msg = 'Congratulations. The level has been solved!'
  print("checking")
  if ihost == host and flag == win_flag:
    socketio.emit('solved_event', {'win_msg': win_msg})
    print("solved!")

def worker():
  global focus
  global hosts_info
  socketio.sleep(tick)
  UDP_IP = "0.0.0.0"
  UDP_PORT = 10514
  sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
  sock.setblocking(False)
  sock.bind((UDP_IP, UDP_PORT))
  last_time = time.time()
  while True:
    socketio.sleep(tick)
    try:
      data, addr = sock.recvfrom(65356) # buffer size is 64k bytes
      if data:
        loaded_json = json.loads(data)
        if loaded_json['event']=='info_event':
          process_info_event(loaded_json)

        elif loaded_json['event']=='intruder_event':
          ihost = loaded_json['data']['host']
          hosts_info[ihost]['compromised'] = True

        elif loaded_json['event']=='flag_event':
          ihost = loaded_json['data']['host']
          flag = loaded_json['data']['flag']
          validate_flag(ihost,flag)

        elif loaded_json['event']=='connect_event':
          ihost = loaded_json['data']['host']
          dest = loaded_json['data']['dest']
          socketio.emit('update_hosts_event', {'hosts': ihost, 'edges': {'from':ihost, 'to': dest }})
        else:
          socketio.emit(loaded_json['event'], loaded_json['data'])
    except socket.error as msg:
      pass
    
    #timeout info event
    cur_time = time.time()
    if cur_time > (last_time + 1):                                                              #every second
      last_time = cur_time
      for host in hosts_info:                                                                   #check for every host in list
        if (time.time() - hosts_info[host]['last']) > 5 and hosts_info[host]['online'] == True: #if data is stale (+ 5 sec)
          hosts_info[host]['online'] = False
          socketio.emit('update_hosts_event', {'hosts': host, 'apearance': '3'})                #grey out icon


@socketio.on('connect', namespace='')
def test_connect():
  global thread
  if thread is None:
    thread = socketio.start_background_task(target=worker)

if __name__ == '__main__':
  socketio.run(app, debug=True)

