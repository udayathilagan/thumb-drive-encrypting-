import os
import wmi
from cryptography.fernet import Fernet


my_key = 'KEY1'
# files = r'D:\\'
files = r''

c = wmi.WMI()


def check_for_key():
    for disk in c.Win32_LogicalDisk():
        if disk.VolumeName == my_key:
            return disk


def load_key(usbDisk):
    port = usbDisk.DeviceID
    try:
        print('Trying to find key...')
        with open(f'{port}\\encryptionKey.key', 'rb') as encryptKey:
            key = encryptKey.read()
            print('Key Found')
    except:
        print('Key not found... Creating a new key')
        key = Fernet.generate_key()
        with open(f'{port}\\encryptionKey.key', 'wb') as encryptKey:
            encryptKey.write(key)
    return key


def encryptFiles(key, directory):
    files = os.listdir(directory)
    cipher = Fernet(key)
    global state
    state = 'encrypted'
    for file in files:
        with open(f'{directory}\{file}', 'rb') as old:
            original = old.read()
        encrypted = cipher.encrypt(original)
        with open(f'{directory}\{file}', 'wb') as old:
            old.write(encrypted)


def decryptFiles(key, directory):
    files = os.listdir(directory)
    cipher = Fernet(key)
    global state
    state = 'decrypted'
    for file in files:
        with open(f'{directory}\{file}', 'rb') as old:
            encrypted = old.read()
        decrypted = cipher.decrypt(encrypted)
        with open(f'{directory}\{file}', 'wb') as old:
            old.write(decrypted)


state = 'decrypted'
if __name__ == '__main__':
    while True:
        disk = check_for_key()
        try:
            key = load_key(disk)
        except:
            print('No Key Available')
        if disk != None:
            current_state = 'decrypted'
            if current_state != state:
                decryptFiles(key, files)
            else:
                current_state = 'encrypted'
                if current_state != state:
                    encryptFiles(key, files)
