import signal
import socket
import getpass
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode, b64encode
from os import name, system
from csv import reader, writer

# Stop Ctrl-C termination
# def handler(signum, frame):
#    return
# signal.signal(signal.SIGINT, handler)

# Clear screen
clear = lambda: system('cls' if name in ('nt', 'dos') else 'clear')

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 7777

try:
  ClientSocket.connect((host, port))
except socket.error as e:
  print(str(e))

while 1:
  action = ClientSocket.recv(20000).decode()

  if "clear" in action:
    clear()
    continue
      
  elif action == "exit":
    ClientSocket.close()
    exit()

  if "Transferring File" in action:
    with open("c:/PSEC/admin/report.csv", "wb") as f:
      while 1:
          bytes_read = ClientSocket.recv(1024)
          if "End Transfer Session" in bytes_read.decode():
              break
          f.write(bytes_read)
    with open("report.csv", "r") as f:
      report = [line for line in reader(f)]
      report = report[::2]
    with open("report.csv", "w", newline='') as f:
      fixReport = writer(f)
      [fixReport.writerow(line) for line in report]
    continue

  if [i for i in ["Please enter key password: "] if i in action]:
    while 1:
      password = getpass.getpass(action+"\n")
      if password == "":
        clear()
        continue
      break
    username = (action.split(" ")[-2])
    cipher_text = b64decode(action.split(" ")[-1][2:-1])
    key = open(f"c:/PSEC/admin/{username}.pem", "rb").read()
    try:
      prvkey = RSA.import_key(key, passphrase=password)
      cipher = Cipher_PKCS1_v1_5.new(prvkey)
      decrypt_text = cipher.decrypt(cipher_text, None)
      if decrypt_text == b'':
        raise ValueError
      decrypt_text = b64encode(decrypt_text)
      ClientSocket.sendall(decrypt_text)
    except ValueError:
      ClientSocket.sendall(" ".encode())
    continue

  if [i for i in ["Please enter your password","Please enter a password","Please re-enter the password:"] if i in action]:
    while 1:
      data = getpass.getpass(action)
      if data == "":
        clear()
        continue
      break
    ClientSocket.sendall(data.encode())
    continue
    
  if [i for i in [">>","(<] Exit):"] if i in action]:
    while 1:
      data = input(action)
      if data == "":
        clear()
        continue
      break
    ClientSocket.sendall(data.encode())
    continue
  
  if "[Enter to continue]" in action:
    input(action)
    ClientSocket.sendall("Done".encode())
    continue

  print(action)
