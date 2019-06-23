#!/usr/bin/env python

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

async_mode = None

app = Flask(__name__, template_folder='templates', static_folder='static')
socketio = SocketIO(app, async_mode=async_mode)


def emit_infoevent():
    emit('info_event', {'type': 'aaa', 'data': 1})

def emit_logevent():
    emit('log_event', {'host': 'aaa', 'data': 1, 'clear': 0})

def emit_selecttabevent(index):
    emit('select_tab_event', {'host_index': index})

def emit_addhostsevent():
    emit('add_hosts_event', {'hosts': 'aaa', 'edges': 'bbb', 'apearance': 'static/img/pc.png'})

def emit_updatehostsevent():
    emit('update_hosts_event', {'hosts': 'aaa', 'edges': 'bbb', 'apearance': 'static/img/pc.png'})

def emit_removehostsevent():
    emit('remove_hosts_event', {'hosts': 'aaa'})


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('get_page_data', namespace='')
def get_page_data(data):
    print "get_page_data" #emit('my_response', {'data': 'aaa', 'count': 1})
    emit_selecttabevent(0)

@socketio.on('get_hosts', namespace='')
def get_page_data(data):
    print "get_hotst" #emit('my_response', {'data': 'aaa', 'count': 1})
    emit_selecttabevent(1)

@socketio.on('get_logging_data', namespace='')
def get_page_data(data):
    print "get_logging_data" #emit('my_response', {'data': 'aaa', 'count': 1})
    emit_selecttabevent(2)

@socketio.on('get_info_data', namespace='')
def get_page_data(data):
    print "get_info_data" #emit('my_response', {'data': 'aaa', 'count': 1})

@socketio.on('set_focus', namespace='')
def get_page_data(data):
    print "set_focus" #emit('my_response', {'data': 'aaa', 'count': 1})

if __name__ == '__main__':
    socketio.run(app, debug=True)
