from django.http import HttpResponse
from e89_security import decrypt_message, encrypt_message
import RNCryptor
import json

def _get_user_data(request, key, encryption_active):
    body = request.body
    request._encoding="ISO-8859-1"
    try:
        if request.POST.has_key("json"):
            message = request.POST['json']
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

    return HttpResponse(data,content_type="application/json; charset=ISO-8859-1")