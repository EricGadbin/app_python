from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json
import re
from datetime import datetime

class WebhookHandler(BaseHTTPRequestHandler):

    def do_POST(self): # Insérer les données dans la base de données
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)
        data = json.loads(content.decode('utf-8'))
        try:
            validated_data = self.validate_data(data)
            self.insert_data(validated_data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Données mises dans la DB\n".encode("utf-8"))
        except ValueError as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))

    def validate_data(self, data):  #verification des fields required et de leurs type
        try:
            data['resourceId'] = int(data['resourceId'])
        except ValueError:
            raise ValueError("resourceId n'est pas un int")
        try:
            data['triggeredAt'] = datetime.strptime(data['triggeredAt'], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            raise ValueError("triggeredAt doit etre au format YYYY-MM-DDTHH:MM:SSZ")
        if not re.match("^server-[0-9]{1,100}$", data['triggeredBy']):
            raise ValueError("triggeredBy ne respecte pas le pattern donné")
        return data

    def insert_data(self, data): #On insere les datas, optimalement, il faudrait verifier si la ressource existe déja pour l'update a la place d'en créer une nouvelle
        connection = sqlite3.connect("/db_server/db/events.db")
        c = connection.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS events (
                        resourceType TEXT NOT NULL,
                        resourceId INTEGER NOT NULL,
                        eventType TEXT NOT NULL,
                        triggeredAt TEXT NOT NULL,
                        triggeredBy TEXT NOT NULL)''')
        c.execute('INSERT INTO events (resourceType, resourceId, eventType, triggeredAt, triggeredBy) VALUES (?, ?, ?, ?, ?)',
                  (data['resourceType'], data['resourceId'], data['eventType'], data['triggeredAt'], data['triggeredBy']))
        connection.commit()
        connection.close()

def run(server_class=HTTPServer, handler_class=WebhookHandler):
    server_address = ('0.0.0.0', 8002)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()