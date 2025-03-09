from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import re

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Regular expression for validating domain names
DOMAIN_REGEX = r'^(?=.{1,253})(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$'

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/check-domain', methods=['POST'])
def check_domain():
    data = request.json
    domain = data.get('domain', '')

    # Validate domain format
    if not re.match(DOMAIN_REGEX, domain):
        return jsonify({'error': 'Invalid domain format'}), 400

    # Split domain into name and suffix
    name, suffix = domain.rsplit('.', 1)

    # Query WHOIS API (replace 'WHOIS_API_URL' with the actual API endpoint)
    whois_response = requests.get(f'WHOIS_API_URL?domain={domain}')
    
    if whois_response.status_code != 200:
        return jsonify({'error': 'Failed to retrieve WHOIS information'}), 500

    whois_data = whois_response.json()

    # Check if the domain is registered
    if whois_data.get('status') == 'registered':
        return jsonify({
            'registered': True,
            'registration_date': whois_data.get('creationDate'),
            'whois_info': whois_data
        })
    else:
        return jsonify({
            'registered': False,
            'whois_info': whois_data
        })

if __name__ == '__main__':
    app.run(debug=True)