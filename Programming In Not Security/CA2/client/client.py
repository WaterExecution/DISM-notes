import signal
import socket
import getpass
from os import name, system

# Stop Ctrl-C termination
def handler(signum, frame):
   return
signal.signal(signal.SIGINT, handler)

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
  action = ClientSocket.recv(10240).decode()

  if "clear" in action:
    clear()
    continue
      
  elif action == "exit":
    ClientSocket.close()
    exit()

  if "Please enter key password:" in action:
    ClientSocket.sendall("Client".encode())
    continue

  if [i for i in ["Please enter your password","Please enter a password","Please re-enter the password"] if i in action]:
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

