import unittest
from db_server.db_server import WebhookHandler


#Je ne test que la validation des datas pour l'exemple
class TestValidateData(unittest.TestCase):

    def test_validate_data_correct(self):
        # Données correctes
        data = {
            "resourceType": "customer",
            "resourceId": 123,
            "eventType": "resourceHasBeenCreated",
            "triggeredAt": "2024-03-21T10:00:00Z",
            "triggeredBy": "server-1"
        }
        self.assertTrue(WebhookHandler.validate_data(data))

    def test_validate_data_missing_field(self):
        data = {
            "resourceType": "customer",
            "resourceId": 123,
            # eventType n'est pas la
            "triggeredAt": "2024-03-21T10:00:00Z",
            "triggeredBy": "server-1"
        }
        self.assertFalse(WebhookHandler.validate_data(data))

    def test_validate_data_incorrect_type(self):
        data = {
            "resourceType": "customer",
            "resourceId": "je ne suis pas un int", # Type incorrect pour resourceId
            "eventType": "resourceHasBeenCreated",
            "triggeredAt": "2024-03-21T10:00:00Z",
            "triggeredBy": "server-1"
        }
        self.assertFalse(WebhookHandler.validate_data(data))

    def test_validate_data_incorrect_date_format(self):
        data = {
            "resourceType": "customer",
            "resourceId": 123,
            "eventType": "resourceHasBeenCreated",
            "triggeredAt": "ceci n'est pas une date", # Format de date incorrect
            "triggeredBy": "server-1"
        }
        self.assertFalse(WebhookHandler.validate_data(data))

    def test_validate_data_incorrect_pattern(self):
        data = {
            "resourceType": "customer",
            "resourceId": 123,
            "eventType": "resourceHasBeenCreated",
            "triggeredAt": "2024-03-21T10:00:00Z",
            "triggeredBy": "ne respecte pas le patttern" # Pattern incorrect pour triggeredBy
        }
        self.assertFalse(WebhookHandler.validate_data(data))

if __name__ == '__main__':
    unittest.main()