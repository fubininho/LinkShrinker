from flask import Flask, jsonify, request
import random
import string
from link import Link

app = Flask(__name__)
links = {}


def generate_short_link():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


@app.route('/shorten', methods=['POST'])
def shorten_link():
    original_url = request.json['url']
    short_link = generate_short_link()
    link = Link(original_url, short_link)
    links[short_link] = link
    return jsonify({'short_link': short_link})


@app.route('/links', methods=['GET'])
def get_links():
    links_data = {short_link: link.original_link for short_link, link in links.items()}
    return jsonify(links_data)


if __name__ == '__main__':
    app.run()

