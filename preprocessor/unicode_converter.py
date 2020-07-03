import json

with open('./sinhala_songs_corpus.json') as fp:
    data = json.load(fp)
    print("Number of documents: ", len(data))

with open('./final_sinhala_songs_corpus.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)
