#cam_path = '/mnt/cam/TeslaCam'
cam_path = '/mnt/cam'
music_path = '/mnt/music'
audio_path = '/root/audio'


import os
from flask import Flask
from flask import send_from_directory
import commands

app = Flask(__name__)

@app.route('/file/<filename>')
def send_file(filename):
    return send_from_directory(cam_path, filename)


@app.route('/files')
def send_files():
    a,b = commands.getstatusoutput('umount /mnt/cam')
    c,d = commands.getstatusoutput('sync')
    e,f = commands.getstatusoutput('mount /mnt/cam')
    if e != 0 :
        raise Exception(f)
    ret = get_files(cam_path)
    print(ret)
    return str(ret)


def get_http_path():
    return 'http://192.168.219.183:5000'

def get_files(path):
    folders = []
    for root, dirs, files in os.walk(path):
        ret_files = {}
        dir = root.split(path)[1]
        for file in files:
            if file.endswith('mp4'):
               ret_files[dir + '/' + file] = get_http_path() + '/file' + dir + '/' + file
        if len(ret_files) > 0:
            folders.append([dir, ret_files])
        
    return folders

def get_http_stream(path):
    pass

if '__main__' == __name__:
    files = get_files(cam_path)
    print(files)    
    app.run(host='192.168.219.183')
