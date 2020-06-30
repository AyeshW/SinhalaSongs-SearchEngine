from flask import Flask, request
from searchengine.search import search
app = Flask(__name__)

INDEX = "test2music"


@app.route('/sinhala-songs/search')
def search_songs():
    phrase = request.args.get('q')
    response = search(phrase, INDEX)

    return response


if __name__ == '__main__':
    app.run(host='localhost')