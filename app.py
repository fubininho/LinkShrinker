from flask import Flask, jsonify, request
import random
import string

app = Flask(__name__)
links = {}

def generate_short_link():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/shorten', methods=['POST'])
def shorten_link():
    original_url = request.json['url']
    short_link = generate_short_link()
    links[short_link] = original_url
    return jsonify({'short_link': short_link})

@app.route('/links', methods=['GET'])
def get_links():
    return jsonify(links)

if __name__ == '__main__':
    app.run()

