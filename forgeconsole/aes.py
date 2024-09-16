import argparse
import base64
import os
import shutil
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def load_key(key_file):
    with open(key_file, 'rb') as f:
        return RSA.import_key(f.read())

def decrypt_aes_key(encrypted_aes_key, rsa_private_key):
    rsa_key = load_key(rsa_private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_aes_key = base64.b64decode(encrypted_aes_key)
    return cipher_rsa.decrypt(encrypted_aes_key)

def encrypt_file(file_path, output_path, aes_key):
    cipher = AES.new(aes_key, AES.MODE_EAX)
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    with open(output_path, 'wb') as f:
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ciphertext)

def decrypt_file(file_path, output_path, aes_key):
    with open(file_path, 'rb') as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()
    cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    with open(output_path, 'wb') as f:
        f.write(plaintext)

def remove_directory(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory)

def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt files with AES and RSA.")
    parser.add_argument("operation", choices=["encrypt", "decrypt"], help="Operation to perform.")
    parser.add_argument("input_path", help="Input file or directory path.")
    parser.add_argument("output_path", help="Output file or directory path.")
    parser.add_argument("--key", required=True, help="Base64-encoded AES key or base64-encoded encrypted AES key.")
    parser.add_argument("--delete", action="store_true", help="Delete original files or directories after processing.")
    parser.add_argument("--private-key", help="Path to RSA private key (for decryption).")

    args = parser.parse_args()

    if args.operation == "encrypt":
        aes_key = base64.b64decode(args.key)
    elif args.operation == "decrypt":
        if not args.private_key:
            raise ValueError("RSA private key file is required for decryption.")
        aes_key = decrypt_aes_key(args.key, args.private_key)
    
    if args.operation == "encrypt":
        if os.path.isfile(args.input_path):
            encrypt_file(args.input_path, args.output_path, aes_key)
            if args.delete:
                os.remove(args.input_path)
        else:
            for root, _, files in os.walk(args.input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, args.input_path)
                    output_file_path = os.path.join(args.output_path, f"{relative_path}.enc")
                    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                    encrypt_file(file_path, output_file_path, aes_key)
                    if args.delete:
                        os.remove(file_path)
            if args.delete:
                remove_directory(args.input_path)
    
    elif args.operation == "decrypt":
        if os.path.isfile(args.input_path):
            decrypt_file(args.input_path, args.output_path, aes_key)
            if args.delete:
                os.remove(args.input_path)
        else:
            for root, _, files in os.walk(args.input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path.endswith(".enc"):
                        relative_path = os.path.relpath(file_path, args.input_path)
                        output_file_path = os.path.join(args.output_path, relative_path[:-4])
                        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                        decrypt_file(file_path, output_file_path, aes_key)
                        if args.delete:
                            os.remove(file_path)
            if args.delete:
                remove_directory(args.input_path)

if __name__ == "__main__":
    main()
