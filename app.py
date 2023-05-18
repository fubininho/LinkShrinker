from flask import Flask, jsonify, request
import random
import string
from library import Library
from link import Link

app = Flask(__name__)
library = Library()


def generate_short_link():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


@app.route('/shorten', methods=['POST'])
def shorten_link():
    original_url = request.json['url']
    short_link = generate_short_link()
    library.insert(Link(original_url, short_link))
    return jsonify({'short_link': short_link})


@app.route('/links', methods=['GET'])
def get_links():
    links_data = {link.shortened_link: link.original_link for link in library.list()}
    return jsonify(links_data)


if __name__ == '__main__':
    app.run()

