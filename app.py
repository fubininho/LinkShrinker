from flask import Flask, jsonify, request, redirect
import random
import string
from library import Library
from link import Link
from logs import LogsLibrary

app = Flask(__name__)
library = Library()
logs_library = LogsLibrary()


def generate_short_link():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


@app.route('/shorten', methods=['POST'])
def shorten_link():
    original_url = request.json['url']
    url_without_http = original_url.replace('http://', '').replace('https://', '')
    short_link = generate_short_link()
    library.insert(Link(url_without_http, short_link))
    return jsonify({'short_link': short_link})


@app.route('/<string:short_id>', methods=['GET'])
def get_item(short_id):
    link = library.find_link(short_id)
    if link:
        print("🔥", link.original_link)
        logs_library.add_click(link)
        return redirect(f'http://{link.original_link}')
    else:
        return jsonify({'message': f'Link {short_id} not found.'}), 404


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


@app.route('/links', methods=["POST"])
def edit_link():
    shortened_link = request.args.get('shortened_link')
    if shortened_link:
        old_link = library.find_link(shortened_link)
        library.delete_link(shortened_link)
        old_link.shortened_link = generate_short_link() 
        library.insert(old_link)
        return jsonify({'message': f'Link changed to {old_link.shortened_link}.'}), 201
    else:
        return jsonify({'message': 'Missing shortened_link parameter.'}), 400


@app.route('/stats', methods=['GET'])
def get_stats():
    number_of_clicks = request.args.get('number_of_clicks')
    if number_of_clicks == "true":
        return jsonify(logs_library.get_total_clicks_as_pandas().to_dict()), 200
    elif number_of_clicks == "false":
        return jsonify(logs_library.get_clicks_as_pandas().to_dict()), 200
    else:
        return jsonify({'message': 'Missing number_of_clicks parameter.'}), 400


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


