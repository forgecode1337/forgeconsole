from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os

def main():
    if not os.path.isfile('public.pem') or not os.path.isfile('private.pem'):
        # Generate RSA keys
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        # Save RSA keys to files
        with open('private.pem', 'wb') as f:
            f.write(private_key)
        with open('public.pem', 'wb') as f:
            f.write(public_key)

    # Generate a 32-byte AES key
    aes_key = os.urandom(32)
    encoded_aes_key = base64.b64encode(aes_key).decode('utf-8')
    print(f"Base64-encoded AES Key: {encoded_aes_key}")

    # Encrypt AES key with RSA public key
    public_key = RSA.import_key(open('public.pem').read())
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    encoded_encrypted_aes_key = base64.b64encode(encrypted_aes_key).decode('utf-8')
    print(f"Base64-encoded Encrypted AES Key: {encoded_encrypted_aes_key}")

if __name__ == "__main__":
    main()
