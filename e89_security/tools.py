from django.http import HttpResponse, Http404
from data_parser import RawPostParser
from e89_security import decrypt_message, encrypt_message, _gzip_string, _ungzip_string
import RNCryptor
import json
from io import BytesIO
import StringIO

def _get_user_data(request, key, encryption_active, gzip_active=False, multipart=True):
    body = request.body
    # Parsing raw content
    if multipart:
        rpp = RawPostParser(request.META, BytesIO(body), [])
        raw_POST = rpp.parse()
    else:
        raw_POST = request.POST

    try:
        if raw_POST.has_key("json"):
            message = raw_POST['json']
        else:
            message = body

        if encryption_active:
            decrypted = decrypt_message(message, key, decode=(not gzip_active))

            if gzip_active:
                decrypted = _ungzip_string(decrypted)
            data = json.loads(decrypted)
        else:
            if gzip_active:
                message = _ungzip_string(message)
            data = json.loads(message)

    except RNCryptor.BadData:
        raise Http404

    return data

def _generate_user_response(data, key, encryption_active, gzip_active=False):
    data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    if gzip_active:
        data = _gzip_string(data)

    if encryption_active:
        data = encrypt_message(data, key)

    return HttpResponse(data,content_type="application/octet-stream")

def secure_view(encryption_key, encryption_active):
    ''' Decorator that secures a view.
        The view that is decorated will receive as arguments the request, a dictionary containing
        data received and whatever keyword arguments it received. It must return a dictionary containing data to be sent back.

        Example:

        @secure_view(encryption_key="password", encryption_active=True)
        def my_view(request, data):
            ...
            return {}
    '''

    def wrapper(wrapped_view):

        def decorator(request, *args, **kwargs):
            if request.method != 'POST':
                raise Http404

            gzip_active = request.META.get('HTTP_X_SECURITY_GZIP', 'false') == 'true'

            if not request.user.is_authenticated():
                data = _get_user_data(request, encryption_key, encryption_active, gzip_active)
            else:
                data = _get_user_data(request, encryption_key, False, gzip_active, multipart=False)

            ret = wrapped_view(request, data, *args, **kwargs)

            if not request.user.is_authenticated():
                response = _generate_user_response(ret, encryption_key, encryption_active, gzip_active)
            else:
                response = _generate_user_response(ret, encryption_key, False, gzip_active)

            return response

        return decorator

    return wrapper
