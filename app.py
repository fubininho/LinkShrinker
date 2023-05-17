from flask import Flask, jsonify, request
import random
import string

app = Flask(__name__)

def generate_short_link():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/shorten', methods=['POST'])
def shorten_link():
    original_url = request.json['url']
    short_link = generate_short_link()
    return jsonify({'short_link': short_link})

if __name__ == '__main__':
    app.run()

