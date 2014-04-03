import http.client
import json
import logging


log = logging.getLogger(__name__)


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
            if response.status != 200:
                log.error("Incorrect response from %s", address)
                return
            decison = json.loads(response.read().decode('utf-8'))
        except Exception:
            # possible reasons: no connection, not UTF-8, not JSON
            log.exception("Couldn't get proper response from %s", address)
            return

        return decison

connector = Connector()
