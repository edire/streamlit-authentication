#%% Import Libraries

import os
import hashlib
from cryptography.fernet import Fernet


#%%

def hash_encrypt(input_string, secret_string=os.getenv('SECRET_STRING')):
    input_string = input_string + secret_string
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    hashed_string = sha256_hash.hexdigest()
    return hashed_string


def check_authorized_user(email, authorized_users):
    authorized_users = authorized_users.split(',')
    authorized_users = [x.strip() for x in authorized_users]
    if authorized_users == "*" or email in authorized_users or '*@' + email.split('@')[1] in authorized_users:
        email_secret = hash_encrypt(email)
        return email_secret
    else:
        return False
        

def symmetric_encrypt(input_string, secret_string=os.getenv('FERNET_KEY')):
    cipher_suite = Fernet(secret_string)
    encrypted_value = cipher_suite.encrypt(input_string.encode()).decode()
    return encrypted_value


def symmetric_decrypt(input_string, secret_string=os.getenv('FERNET_KEY')):
    cipher_suite = Fernet(secret_string)
    decrypted_value = cipher_suite.decrypt(input_string.encode()).decode()
    return decrypted_value


#%%