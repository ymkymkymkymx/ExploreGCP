from wsgiref.simple_server import make_server


def yingyong(environ, start_response):

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [b'<h1>Hello world! 3:31 am 9/8/2020</h1>']


httpd = make_server('', 80, yingyong)

httpd.serve_forever()
while(1):
    i=1