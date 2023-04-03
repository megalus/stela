from django.http import HttpResponse

from stela import env

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Stela Example</title>
</head>
<body>
    <h1>Hello World</h1>
    <li>Your current environment is: <b>{env}</b></li>
    <li>Your secret is: <b>{secret}</b></li>
</body>
</html>
"""


# Create your views here.
def home(request):
    # return a simple inline html here
    return HttpResponse(HTML.format(env=env.current_environment, secret=env.MY_SECRET))
