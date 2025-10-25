import http.server, ssl, socketserver, os

PORT = 8443
web_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(web_dir)

handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)

keyfile = os.path.join(web_dir, "..", "cert", "localhost.key")
certfile = os.path.join(web_dir, "..", "cert", "localhost.crt")

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=certfile, keyfile=keyfile)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"Serving HTTPS on https://127.0.0.1:{PORT}")
httpd.serve_forever()
