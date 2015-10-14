# -*- coding: utf-8 -*-
from django.conf import settings
from RNCryptor import RNCryptor,BadData
import StringIO
import gzip

__VERSION__ = "1.0.3"

def decrypt_message(msg, key, decode=True):
    cryptor = RNCryptor()
    if type(msg) == type(u""):
        msg = msg.encode("UTF-8")
    msg = cryptor.decrypt(msg, key)

    if decode:
        msg = msg.decode("UTF-8")

    return msg

def encrypt_message(msg, key):
    cryptor = RNCryptor()
    if type(msg) == type(u""):
        msg = msg.encode("UTF-8")

    msg = cryptor.encrypt(msg, key)

    return msg

def _gzip_string(msg):
    if type(msg) == type(u""):
        msg = msg.encode("UTF-8")
    out = StringIO.StringIO()
    with gzip.GzipFile(fileobj=out, mode="w") as f:
        f.write(msg)
    return out.getvalue()

def _ungzip_string(msg):
    if type(msg) == type(u""):
        msg = msg.encode("UTF-8")
    out = StringIO.StringIO(msg)
    with gzip.GzipFile(fileobj=out, mode="rb") as f:
        content = f.read()
    return content