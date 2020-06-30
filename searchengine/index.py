import json
from elasticsearch import Elasticsearch, helpers


def create_index(source_path):
    with open('../corpus/sinhala_songs_corpus.json') as fp:
        docs = json.load(fp)

    print("Dict docs length:", len(docs))

    client = Elasticsearch("localhost:9200")

    resp = helpers.bulk(
        client,
        docs,
        index="test2music"
    )


if __name__ == '__main__':
    source = '../corpus/sinhala_songs_corpus.json'
    create_index(source)
