import csv
import os
import re
import random
import glob
from string import ascii_letters
from threading import Thread
import logging
import datetime
from socket import socket
from math import floor

from tkinter import *
from tkinter import scrolledtext
from functools import partial
from PIL import ImageTk,Image  

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import FTPServer

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Signature import pkcs1_15 
from Crypto.Hash import SHA256

class ftp_server:
  #https://stackoverflow.com/questions/24436287/pyftpdlib-how-to-add-a-user-while-still-running-server
  class MyHandler(TLS_FTPHandler):
    def on_file_received(self, file):
      # Decrypt
      #print(file) #/home/runner/Camera/source/server/data/camera1/1_2022_02_12_05_15_42.jpg
      with open(file, "rb") as f:
        encryptedMsg =  f.read()
        # Pickle alternative is possible
        sentImg = encryptedMsg[:-544]
        sentIV = encryptedMsg[-544:-528]
        sentAuthTag = encryptedMsg[-528:-512]
        enckey = encryptedMsg[-512:-256]
        signature = encryptedMsg[-256:]
        sentMsg = [sentImg, sentIV, sentAuthTag]
      #print(len(sentImg),len(sentIV),len(sentAuthTag),len(enckey),len(signature))

      key = open("server-private.pem", "rb").read()
      prvkey = RSA.import_key(key)
      cipher = Cipher_PKCS1_v1_5.new(prvkey)
      decipheredkey = cipher.decrypt(enckey, None)

      (ciphertext, nonce, authTag) = sentMsg
      aesCipher = AES.new(decipheredkey, AES.MODE_GCM, nonce)
      image = aesCipher.decrypt_and_verify(ciphertext, authTag)

      pubkeypath = re.findall(r"data.+", file)[0]
      pubkeypath = os.path.join('public', pubkeypath.split(os.sep)[-2], 'camera.pub')
      key = open(pubkeypath, "rb").read()
      pubkey = RSA.import_key(key)

      digest=SHA256.new(image)
      verifier = pkcs1_15.new(pubkey)
      try:
        verifier.verify(digest,signature)
        newFile = re.findall(r"data.+", file)[0]
        newFile = newFile.split(os.sep)
        newFile.insert(-1, ''.join((random.choice(ascii_letters)) for x in range(8)))
        newFile = "."+ os.sep + os.sep.join(newFile[:-2]) + os.sep + "_".join(newFile[-2:])
        os.rename(file, newFile)
        with open(newFile, 'wb') as f:
          f.write(image)
      except:
        with open(f".{os.sep}pyftpd.log", "a") as f:
          f.write(f"Potential Tampering warning {file}")
        pass
      

  def __init__(self):
    self.authorizer = DummyAuthorizer()
    self.load_user()

  def load_user(self):
    with open(f".{os.sep}credentials.csv", "r") as f:
      reader = csv.DictReader(f)
      reader = [line for line in reader]
      for credential in reader:
        if credential["block"] == "0":
          Thread(target=self.add_user,args=(credential["username"],credential["password"])).start()

  def run(self):
    self.handler = self.MyHandler
    self.handler.certfile = 'server-ftps.pem'
    self.handler.authorizer = self.authorizer
    self.address = ('127.0.0.1', 2121)
    self.server = FTPServer(self.address, self.handler)
    logging.basicConfig(filename='pyftpd.log', level=logging.INFO)
    self.server.serve_forever()

  def add_user(self,user,passwd):
    try:
      os.mkdir(f".{os.sep}data{os.sep}{user}")
    except FileExistsError:
      pass
    self.authorizer.add_user(str(user), str(passwd), f".{os.sep}data{os.sep}{user}", perm='w')

  def del_user(self,*user):
    self.authorizer.remove_user(''.join(user))

"""
https://chromium.googlesource.com/external/pyftpdlib/+/refs/heads/master/pyftpdlib/authorizers.py
Write permissions:
  - "a" = append data to an existing file (APPE command)
  - "d" = delete file or directory (DELE, RMD commands)
  - "f" = rename file or directory (RNFR, RNTO commands)
  - "m" = create directory (MKD command)
  - "w" = store a file to the server (STOR, STOU commands)
  - "M" = change file mode (SITE CHMOD command)
"""

class certificate:
    def run(self):
      host = '127.0.0.1'
      port = 7777
      ThreadCount = 0

      ServerSocket = socket()
      try:
        ServerSocket.bind((host, port))
      except:
        print("Unable to bind")
        exit()
      print('Waitiing for a Connection..')
      ServerSocket.listen(5)

      while True:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        newThread = Thread(target=self.threaded_client ,args=(Client,))
        newThread.start()
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    
    def threaded_client(self, connection):
      while 1:
        rec = connection.recv(20240).decode()
        if "[REQ-CERT]" in rec:
          connection.send(open('server-cert.crt','rb').read())
        if "[STOR-CERT]" in rec:
          rec = rec.split(" ")

          try:
            os.mkdir(f".{os.sep}public{os.sep}{rec[1]}")
          except FileExistsError:
            pass
          open(f'public{os.sep}{rec[1]}{os.sep}camera.pub','w').write(' '.join(rec[2:]))
          return

# Check for keys
ftp = ftp_server()
Thread(target=ftp.run,args=()).start()
Thread(target=certificate().run,args=()).start()
#Thread(target=ftp.add_user,args=('user','password')).start()

def registeration(frame):
  frame.destroy()
  frame1 = Frame(win)
  frame1.pack(side=TOP)
  button = Button(frame1, text="Register Camera", command=partial(registerMenu, frame1), width=40).pack(side=TOP, pady=10)
  button1 = Button(frame1, text="Unregister Camera",  command=partial(unregisterMenu, frame1), width=40).pack(side=TOP, pady=10)
  button2 = Button(frame1, text="Back", command=partial(mainmenu, frame1), width=10).pack(side=BOTTOM, pady=10)
  return

def registerMenu(frame1):
  frame1.destroy()
  frame2 = Frame(win)
  frame2.pack(side=TOP)

  new_camid = StringVar()
  new_username = StringVar()
  new_password = StringVar()
  #inputs
  label = Label(frame2, text = "Camera ID").pack(side=TOP, pady=(10,0))
  camid = Entry(frame2,width=40,textvariable=new_camid).pack(pady=5)
  label2 = Label(frame2, text = "Camera Username").pack(side=TOP, pady=10)
  username = Entry(frame2,width=40,textvariable=new_username).pack(pady=5)
  label3 = Label(frame2, text = "Camera Password").pack(side=TOP, pady=10)
  password = Entry(frame2,width=40,textvariable=new_password).pack(pady=5)
  #submit button
  submit = Button(frame2 ,text="Submit",width=10,command=partial(registerCamera,new_camid,new_username,new_password,frame2)).pack(side=LEFT, pady=(10,0), padx=(50,0))
  button = Button(frame2, text="Back", command=partial(registeration, frame2), width=10).pack(side=LEFT, pady=(10,0), padx=(10,0))
  return
#register into csv
def registerCamera(new_camid,new_username,new_password,frame2):
  csvlist=[]
  csvlist.append(new_camid.get())
  csvlist.append(new_username.get())
  csvlist.append(new_password.get())
  with open(f".{os.sep}credentials.csv", "a",newline='\n') as f: 
    csvwriter = csv.writer(f)
    csvwriter.writerow(csvlist)
  Thread(target=ftp.add_user,args=(new_username.get(),new_password.get())).start()
  mainmenu(frame2)

def unregisterMenu(frame1):
  frame1.destroy()
  frame2 = Frame(win)
  frame2.pack(side=TOP)

  reg_username = StringVar()
  #inputs
  text_area = scrolledtext.ScrolledText(frame2, wrap = WORD, width = 40, height = 5, font = ("Times New Roman", 12))
  text_area.pack(side=TOP, pady = 10, padx = 10)
  with open("credentials.csv", "r") as database:
    usernames = '\n'.join([line['username'] for line in csv.DictReader(database)])
    text_area.insert(INSERT, usernames)
  label2 = Label(frame2, text = "Camera Username").pack(side=TOP, pady=10)
  username = Entry(frame2,width=40,textvariable=reg_username).pack(pady=5)
  #submit button
  submit = Button(frame2 ,text="Submit",width=10,command=partial(unregisterCamera,reg_username,frame2)).pack(side=LEFT, pady=(10,0), padx=(100,0))
  button = Button(frame2, text="Back", command=partial(registeration, frame2), width=10).pack(side=LEFT, pady=(10,0), padx=(10,0))
  return
  
def unregisterCamera(reg_username, frame2):
  with open("credentials.csv", "r") as database:
    r = csv.DictReader(database)
    fieldnames = r.fieldnames
    database = [line for line in r]
  [database.pop(i) for i, line in enumerate(database) if line['username'] == reg_username.get()]
  with open("credentials.csv", "w") as updatedDatabase:
    writer = csv.DictWriter(updatedDatabase, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(database)
  mainmenu(frame2)
  return
  
def enableCamera(frame):
  frame.destroy()
  with open("credentials.csv", "r") as database:
    r = csv.DictReader(database)
    fieldnames = r.fieldnames
    database = [line for line in r]
  block = [line['block'] for line in database]
  username = [line['username'] for line in database]
  fourCameras = floor(len(username)/4)
  bottomCameras = len(username)%4
  button_dict = {}
  frames = {}
  for i in range(1,fourCameras+1):
    frames[f"frame{i}"] = Frame(win)
    frames[f"frame{i}"].pack(side=TOP)
    for j in range(1,5):
      camera = username[i*j-1]
      if block[i*j-1] == "0":
        color = "green"
      else:
        color = "red"
      button_dict[camera] = Button(frames[f"frame{i}"], text=camera, width=10, bg=color, command=partial(toggleCamera, database, fieldnames, camera, frames)).pack(side=LEFT)

  frames[f"frame{(fourCameras+1)}"] = Frame(win)
  frames[f"frame{(fourCameras+1)}"].pack(side=TOP)
  for i in range(bottomCameras):
    i = i+(fourCameras*4)
    camera = username[i]
    if block[i] == "0":
      color = "green"
    else:
      color = "red"
    button_dict[camera] = Button(frames[f"frame{fourCameras+1}"], text=camera, width=10, bg=color, command=partial(toggleCamera, database, fieldnames, camera, frames)).pack(side=LEFT)
  frames[f"frame{(fourCameras+2)}"] = Frame(win)
  frames[f"frame{(fourCameras+2)}"].pack(side=TOP)
  button = Button(frames[f"frame{fourCameras+2}"], text="Back", command=partial(mainmenu, frames), width=10).pack(side=TOP, pady=(10,0))
  return

def toggleCamera(database, fieldnames, camera, frames):
  updatedDatabase = []
  for line in database:
    if line['username'] == camera and line['block'] == "0":
      line['block'] = "1"
      Thread(target=ftp.del_user,args=(line['username'])).start()
    elif line['username'] == camera and line['block'] == "1":
      line['block'] = "0"
      Thread(target=ftp.add_user,args=(camera,line['password'])).start()
    updatedDatabase.append(line)
  with open("credentials.csv", "w") as database:
    writer = csv.DictWriter(database, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updatedDatabase)
  mainmenu(frames)

def selectCamera(frame):
  frame.destroy()
  with open("credentials.csv", "r") as database:
    r = csv.DictReader(database)
    fieldnames = r.fieldnames
    database = [line for line in r]
  username = [line['username'] for line in database]
  fourCameras = floor(len(username)/4)
  bottomCameras = len(username)%4
  button_dict = {}
  frames = {}
  for i in range(1,fourCameras+1):
    frames[f"frame{i}"] = Frame(win)
    frames[f"frame{i}"].pack(side=TOP)
    for j in range(1,5):
      camera = username[i*j-1]
      button_dict[camera] = Button(frames[f"frame{i}"], text=camera, width=10, command=partial(showFootage, camera, frames)).pack(side=LEFT)

  frames[f"frame{(fourCameras+1)}"] = Frame(win)
  frames[f"frame{(fourCameras+1)}"].pack(side=TOP)
  for i in range(bottomCameras):
    i = i+(fourCameras*4)
    camera = username[i]
    button_dict[camera] = Button(frames[f"frame{fourCameras+1}"], text=camera, width=10, command=partial(showFootage, camera, frames)).pack(side=LEFT)
  frames[f"frame{(fourCameras+2)}"] = Frame(win)
  frames[f"frame{(fourCameras+2)}"].pack(side=TOP)
  button = Button(frames[f"frame{fourCameras+2}"], text="Back", command=partial(mainmenu, frames), width=10).pack(side=TOP, pady=(10,0))
  return

def showFootage(camera, frames):
  for key in frames:
    frames[key].destroy()
  frame2 = Frame(win)
  frame2.pack(side=TOP)
  canvas = Canvas(frame2, width = 200, height = 200)  
  canvas.pack()
  footageList = glob.glob(f".{os.sep}data{os.sep}{camera}{os.sep}*")
  if len(footageList) != 0:
    footage = [img.split(os.sep)[-1][11:-4] for img in footageList]
    FixedDates = []
    for Date in footage:
      DateInfos = Date.split("_")
      FixDateInfos = []
      for DateInfo in DateInfos:
        DateInfo.lstrip('0')
        FixDateInfos.append(DateInfo)
      FixedDates.append(datetime.datetime(int(FixDateInfos[0]),int(FixDateInfos[1]),int(FixDateInfos[2]),int(FixDateInfos[3]),int(FixDateInfos[4]),int(FixDateInfos[5])))
    r = re.compile(f".+{max(FixedDates).strftime('%Y_%m_%d_%H_%M_%S.jpg')}")
    latestFootage = list(filter(r.match, footageList))
    img = Image.open(latestFootage[0])
    img = img.resize((200, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=NW, image=img)
    canvas.image = img
    button = Button(frame2, text="Back", command=partial(mainmenu, frame2), width=10).pack(side=BOTTOM, pady=10)
  else:
    mainmenu(frame2)

def getLogs(frame):
  frame.destroy()
  frame1 = Frame(win)
  frame1.pack(side=TOP)
  text_area = scrolledtext.ScrolledText(frame1, wrap = WORD, width = 40, height = 10, font = ("Times New Roman", 12))
  text_area.pack(side=TOP, pady = 10, padx = 10)
  with open("pyftpd.log", "r") as logs:
    text_area.insert(INSERT,logs.read())
  button = Button(frame1, text="Back", command=partial(mainmenu, frame1), width=10).pack(side=BOTTOM, pady=10)

def mainmenu(*frame):
  #Set the geometry of tkinter frame
  try:
    for f in frame:
      if isinstance(f, dict):
        for key in f:
          f[key].destroy()
      f.destroy()
  except:
    pass
  frame = Frame(win)
  frame.pack()
  #win.geometry("1366x768")
  button = Button(frame, text="Register/Unregister Camera", command=partial(registeration,frame), width=40).pack(side=TOP, pady=10)
  button1 = Button(frame, text="Enable/Disable Camera", command=partial(enableCamera,frame), width=40).pack(side=TOP, pady=10)
  button2 = Button(frame, text="Select Camera", command=partial(selectCamera,frame), width=40).pack(side=TOP, pady=10)
  #select camera, get logs or show images
  button3 = Button(frame, text="Get Logs", command=partial(getLogs,frame), width=40).pack(side=TOP, pady=10)
  

win=Tk()
win.title("server")
win.geometry("480x270")
mainmenu()
win.mainloop()