import http.client
import json


class Connector:

    def __init__(self):
        self.scheme = 'http'
        self.content_type = 'application/json'

    def _get_response(self, address, data):
        conn = http.client.HTTPConnection(address, timeout=5)
        params = json.dumps(data)
        headers = {'Content-type': self.content_type}
        conn.request('POST', '/', params, headers)
        response = conn.getresponse()
        return response

    def ask_for_decision(self, address, data):
        try:
            response = self._get_response(address, data)
        except Exception:
            return 0
        if not response.status == 200:
            return 0
        decison = json.loads(response.read().decode('utf-8'))
        return decison

connector = Connector()
