import socket
import os

if not os.path.isfile('server-cert.crt'):
  ClientSocket = socket.socket()
  host = '127.0.0.1'
  port = 7777

  try:
    ClientSocket.connect((host, port))
  except socket.error as e:
    print(str(e))

  ClientSocket.sendall("[REQ-CERT]".encode())
  certificate = ClientSocket.recv(10240)
  open('server-cert.crt','wb').write(certificate)
  ClientSocket.close()