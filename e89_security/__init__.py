# -*- coding: utf-8 -*-
from django.conf import settings
from RNCryptor import RNCryptor,BadData

def decrypt_message(msg, key):
    cryptor = RNCryptor()
    if type(msg) == type(u""):
        msg = msg.encode("UTF-8")
    msg = cryptor.decrypt(msg, key)
    msg = msg.decode("UTF-8")

    return msg

def encrypt_message(msg, key):
    cryptor = RNCryptor()
    if type(msg) == type(u""):
        msg = msg.encode("UTF-8")

    msg = cryptor.encrypt(msg, key)

    return msg