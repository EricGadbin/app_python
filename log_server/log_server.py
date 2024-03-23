from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

#Configuration du logger en mode "INFO"
logging.basicConfig(filename='events.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s - %(message)s')

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)
        logging.info(content.decode('utf-8'))
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Données sauvergardées dans le logfile".encode('utf-8'))


def run(server_class=HTTPServer, handler_class=WebhookHandler):
    server_address = ('0.0.0.0', 8001)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()