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


@app.route('/links', methods=['DELETE'])
def delete_link():
    shortened_link = request.args.get('shortened_link')
    if shortened_link:
        if library.delete_link(shortened_link):
            return jsonify({'message': f'Link {shortened_link} deleted.'}), 200
        else:
            return jsonify({'message': f'Link {shortened_link} not found.'}), 404
    else:
        return jsonify({'message': 'Missing shortened_link parameter.'}), 400


if __name__ == '__main__':
    app.run()

