import os
import socket

class TCPServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def start(self):
        # create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # associate socket with host and port
        s.bind((self.host, self.port))
        # listen for connections on the socket
        s.listen(5)

        print("Listening at", s.getsockname())

        while True:
            # accept connection to client (localhost), return new socket for communication
            conn, addr = s.accept()
            print("Connected by", addr)
            # receive request data from client (1024 bytes)
            data = conn.recv(1024)
            response = self.handle_request(data)
            # send HTTP response
            conn.sendall(response)
            # when data has been sent close the connection
            conn.close()

    def handle_request(self, data):
        """Handles incoming data and returns a response.
        Override this in subclass.
        """
        return data

class HTTPServer(TCPServer):
    headers = {
        'Server': 'BasicServer',
        'Content-Type': 'text/html',
    }

    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented',
    }

    def handle_request(self, data):
        request = HTTPRequest(data)
        try:
            handler = getattr(self, 'handle_%s' % request.method)
            print(self)
        except AttributeError:
            handler = self.HTTP_501_handler

        response = handler(request)
        return response
    
    def HTTP_501_handler(self, request):
        response_line = self.response_line(status_code=501)

        response_headers = self.response_headers()

        blank_line = b"\r\n"

        response_body = b"<h1>501 Not Implemented</h1>"

        return b"".join([response_line, response_headers, blank_line, response_body])

    def response_line(self, status_code):
        """Returns response line"""
        reason = self.status_codes[status_code]
        line = "HTTP/1.1 %s %s\r\n" % (status_code, reason)

        return line.encode() # call encode to convert str to bytes

    def response_headers(self, extra_headers=None):
        """Returns headers
        The `extra_headers` can be a dict for sending 
        extra headers for the current response
        """
        headers_copy = self.headers.copy() # make a local copy of headers

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for h in headers_copy:
            headers += "%s: %s\r\n" % (h, headers_copy[h])

        return headers.encode() # call encode to convert str to bytes
    
    def handle_GET(self, request):
        filename = request.uri.strip('/') # remove the slash from the request URI

        if os.path.exists(filename):
            response_line = self.response_line(status_code=200)

            response_headers = self.response_headers()

            with open(filename, 'rb') as f:
                response_body = f.read()
        else:
            response_line = self.response_line(status_code=404)
            response_headers = self.response_headers()
            response_body = b"<h1>404 Not Found</h1>"

        blank_line = b"\r\n"

        return b"".join([response_line, response_headers, blank_line, response_body])

class HTTPRequest:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = "1.1" # default to HTTP/1.1 if request doesn't provide a version

        # call self.parse() method to parse the request data
        self.parse(data)

    def parse(self, data):
        lines = data.split(b"\r\n")

        request_line = lines[0]

        words = request_line.split(b" ")

        self.method = words[0].decode() # call decode to convert bytes to str
        if len(words) > 1:
            # we put this in an if-block because sometimes 
            # browsers don't send uri for homepage
            self.uri = words[1].decode() # call decode to convert bytes to str

        if len(words) > 2:
            self.http_version = words[2]
            

if __name__ == '__main__':
    server = HTTPServer()
    server.start()