from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
import os


class WebhookHandler(BaseHTTPRequestHandler): #Override de la classe handler du serveur pour faire nos actions
    def do_GET(self):
        self.send_response(300)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write("Vous n'êtes pas autorisé a utiliser GET sur ce serveur \n".encode('utf-8'))

    def do_POST(self):
        if (self.path == "/event"): #On envoie les données aux serveurs seulement sur la route "/eventx"
            if self.headers['Content-Type'] != "application/json" : 
                self.wfile.write("Mauvais format de donnees, je ne peux lire que du JSON\n".encode('utf-8'))
                return
            length = int(self.headers['Content-Length'])
            content = self.rfile.read(length)
            self.send_to_backend("log_server", os.environ["LOG_SERVER_PORT"], content)
            self.send_to_backend("db_server", os.environ["DB_SERVER_PORT"], content)
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Les données ont bien finies d'être envoyées aux serveurs !\n".encode('utf-8'))

    def send_to_backend(self, host, port, content): #Envoie de données sur un hôte
        headers = {'Content-Type': 'application/json'}
        try:
            connection = http.client.HTTPConnection(host, port)
            connection.request('POST', '/', body=content, headers=headers)
            response = connection.getresponse()
            if response.status != 200:
                print(f"Le serveur {host} à repondu avec une erreur: {response.status}")
            else: 
                print("données envoyées au serveur: {host}...")
        except Exception as e:
                print(f"Connexion au serveur {host} impossible: {str(e)}")
        finally:
            connection.close()

def run(server_class=HTTPServer, handler_class=WebhookHandler): #Méthode pour run le serveur
    server_address = ('0.0.0.0', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__": #Main
    run()