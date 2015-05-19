# -*- coding: utf-8 -*-
from django.conf import settings
from RNCryptor import RNCryptor,BadData

def decrypt_message(msg, key):
    cryptor = RNCryptor()
    if type(msg) == type(u""):
        msg = msg.encode("ISO-8859-1")
    msg = cryptor.decrypt(msg, key)
    msg = msg.decode("ISO-8859-1")

    return msg

def encrypt_message(msg, key):
    cryptor = RNCryptor()
    if type(msg) != type(u""):
        msg = msg.decode("UTF-8")

    msg = msg.encode("ISO-8859-1")
    msg = cryptor.encrypt(msg, key)

    return msg