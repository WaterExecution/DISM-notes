from re import match
import getpass
from Crypto.PublicKey import RSA

print("*** Local-only Secure Administrator Registration ***")
username = str(input("Administrator Username (\"<\" - exit): "))
if username == "<": exit()
password = str(getpass.getpass("Private Key Password (\"<\" - exit): "))
if password == "<": exit()
password2 = str(getpass.getpass("Re-Enter Private Key Password (\"<\" - exit): "))
if password2 == "<": exit()
if (password != password2) or not match("^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%]).{4,20}$", password):
  print("Password not the same or not secure!")
  exit()
if match("^[a-zA-Z0-9_\.-]{4,30}$", username):
  with open("c:/PSEC/server/userid_passwd","r") as f:
    for line in (f.read().split("\n")[:-1]):
      user = line.split("$")[1]
      if user == username:
        print("Username is unavailable!")
        exit()
        
  with open("c:/PSEC/server/adminkey_database","r") as f:
    for line in (f.read().split("\n")[:-1]):
      user = line.split("$")[0]
      if user == username:
        print("Username is unavailable!")
        exit()

    key = RSA.generate(2048)
    encrypted_key = key.export_key(passphrase=password, pkcs=8,
                                  protection="scryptAndAES128-CBC")

    file_out = open(f"c:/PSEC/server/{username}.pem", "wb")
    file_out.write(encrypted_key)
    file_out.close()

    publickey = f"{username}.pub"
    public_key = key.publickey().export_key()
    file_out = open(f"c:/PSEC/server/publickey/{publickey}", "wb")
    file_out.write(public_key)
    file_out.close()

  with open("c:/PSEC/server/adminkey_database","a") as f:
    f.write(f"{username}${publickey}\n")

  print("Please download the pem key and use it to login.")

else:
  print("Username is not valid!")