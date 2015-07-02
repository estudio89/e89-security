from django.http import HttpResponse, Http404
from data_parser import RawPostParser
from e89_security import decrypt_message, encrypt_message
import RNCryptor
import json
from io import BytesIO

def _get_user_data(request, key, encryption_active):
    body = request.body
    # Parsing raw content
    rpp = RawPostParser(request.META, BytesIO(body), [])
    raw_POST = rpp.parse()

    try:
        if raw_POST.has_key("json"):
            message = raw_POST['json']
        else:
            message = body

        if encryption_active:
            data = json.loads(decrypt_message(message, key))
        else:
            data = json.loads(message)

    except RNCryptor.BadData:
        raise Http404

    return data

def _generate_user_response(data, key, encryption_active):
    data = json.dumps(data, ensure_ascii=False)
    if encryption_active:
        data = encrypt_message(data, key)

    return HttpResponse(data,content_type="application/octet-stream")