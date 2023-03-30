from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Signature import pkcs1_15 
from Crypto.Hash import SHA256

def decrypt_AES_GCM(encryptedMsg, secretKey):
    (ciphertext, nonce, authTag) = encryptedMsg
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

with open("encimage.png", "rb") as f:
  encryptedMsg =  f.read()
  sentImg = encryptedMsg[:-416]
  sentIV = encryptedMsg[-416:-400]
  sentAuthTag = encryptedMsg[-400:-384]
  enckey = encryptedMsg[-384:-256]
  signature = encryptedMsg[-256:]
  sentMsg = [sentImg, sentIV, sentAuthTag]


key = open("id_rsa", "rb").read()
prvkey = RSA.import_key(key)
cipher = Cipher_PKCS1_v1_5.new(prvkey)
decipheredkey = cipher.decrypt(enckey, None)

image = decrypt_AES_GCM(sentMsg, decipheredkey)

key = open("public.pem", "rb").read()
pubkey = RSA.import_key(key)

digest=SHA256.new(image)

verifier = pkcs1_15.new(pubkey)
try:
  verifier.verify(digest,signature)
  print("test")
  with open("image.png", "wb") as f:
    f.write(image)
except:
  # Potential Tampering warning
  pass
