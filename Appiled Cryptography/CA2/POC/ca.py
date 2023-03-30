# https://www.digitalocean.com/community/tutorials/openssl-essentials-working-with-ssl-certificates-private-keys-and-csrs
#CA
#3 CA generates CRT using CSR, the CA cert and private key
#4 CA sends CRT back to server


#SERVER
#1 generate public and private key
#2 generate CSR from public and send to CA
#5 server sends CRT to camera

#CAMERA
# camera verifies CRT using CA cart
# extract public key from CRT
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15 
capubkey = open("ca-cert.crt", "rb").read()
#capubkey = RSA.import_key(key)
import OpenSSL
from six import u, b, binary_type, PY3
pubkey = open("server-cert.crt", "rb").read() #pubkey = open("certificate.crt", "rb").read()
#pubkey = RSA.import_key(key)
ca_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, capubkey)
untrusted_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, pubkey)
store = OpenSSL.crypto.X509Store()
store.add_cert(ca_cert)
store_ctx = OpenSSL.crypto.X509StoreContext(store, untrusted_cert)
try:
    store_ctx.verify_certificate()
    print("Verify - OK")
except OpenSSL.crypto.X509StoreContextError:
    print("Verify failed - bad")


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
key = open("server-cert.crt", "rb").read()
pubkey = RSA.import_key(key)
cipher = Cipher_PKCS1_v1_5.new(pubkey)
enckey = cipher.encrypt(b"test")


key = open("server-private.pem", "rb").read()
prikey = RSA.import_key(key)
cipher = Cipher_PKCS1_v1_5.new(prikey)
print(cipher.decrypt(enckey, None))