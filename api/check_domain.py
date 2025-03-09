from http.server import BaseHTTPRequestHandler
import json
import re
import requests

DOMAIN_REGEX = r'^(?=.{1,253})(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$'

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        domain = data.get('domain', '')

        if not re.match(DOMAIN_REGEX, domain):
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid domain format'}).encode())
            return

        name, suffix = domain.rsplit('.', 1)
        whois_response = requests.get(f'WHOIS_API_URL?domain={domain}')

        if whois_response.status_code != 200:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Failed to retrieve WHOIS information'}).encode())
            return

        whois_data = whois_response.json()
        if whois_data.get('status') == 'registered':
            response = {
                'registered': True,
                'registration_date': whois_data.get('creationDate'),
                'whois_info': whois_data
            }
        else:
            response = {
                'registered': False,
                'whois_info': whois_data
            }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())