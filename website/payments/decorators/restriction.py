import functools
import socket
from django.http.response import HttpResponseForbidden



def private_view(func):
    """
    Accept only localhost requests
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]

        remote_address = socket.gethostbyaddr(request.META['REMOTE_ADDR'])
        localhost = socket.gethostbyaddr("127.0.0.1")

        print("REMOTE:", remote_address)
        print("LOCALHOST:", localhost)
        
        if remote_address != localhost:
            return HttpResponseForbidden("access denied")

        value = func(*args, **kwargs)

        return value
    return wrapper