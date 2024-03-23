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

        is_valid = self.validate_data(data)
        if not is_valid:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("le format des données est invalide".encode("utf-8"))
        else:
            self.insert_data(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Données mises dans la DB\n".encode("utf-8"))           

    def validate_data(self, data):
        requirements = { # Types des champs
            "resourceType": str,
            "resourceId": int,
            "eventType": str,
            "triggeredAt": "datetime",
            "triggeredBy": "pattern"
        }
        for field, expected_type in requirements.items(): # On verifie si le champ existe et son type
            #si le champ existe
            if field not in data:
                return False
            
            #son type
            if expected_type == str and not isinstance(data[field], str):
                return False
            elif expected_type == int and not isinstance(data[field], int):
                return False
            elif expected_type == "datetime":
                try:
                    datetime.strptime(data['triggeredAt'], "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    return False
            elif expected_type == "pattern":
                if not re.match("^server-[0-9]{1,100}$", data['triggeredBy']):
                    return False

        # et a la fin, verification de si eventType est une des valeurs autorisées
        if data["eventType"] not in ["resourceHasBeenCreated", "resourceHasBeenUpdated", "resourceHasBeenDeleted"]:
            return False
        return True

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