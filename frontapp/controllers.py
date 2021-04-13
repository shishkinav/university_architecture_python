import datetime as dt

# front controller
def secret_front(request):
    request['data'] = dt.date.today()


def other_front(request):
    request['key'] = 'key'


controllers = [secret_front, other_front]