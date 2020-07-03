from elasticsearch import Elasticsearch
import json
from searchengine.queries import faceted_multi_match_query, faceted_multi_match_range
import re

genre_keywords = ['පැරණි', 'පොප්', 'ක්ලැසික්', 'දේවානුභාවයෙන්', 'පොප්ස්', 'ඩුවට්ස්', 'ක්ලැසික්', 'යුගල', 'යුග', 'ඕල්ඩීස්',
                'කැලිප්සෝ', 'ළමා', 'අලුත්', 'නව', 'සම්භාව්ය', 'වත්මන්', 'චිත්‍රපට', 'රන්වන්', 'තේමාව']
singer_keywords = ['ගෙ', 'ගයන', 'ගැයූ', 'කියන', 'කියූ', 'ගායනා']
writer_keywords = ['ගෙ', 'ලියූ', 'ලියන', 'ලිව්ව', 'රචනා', 'රචිත']
music_keywords = ['සංගීත', 'ගෙ', 'තනු', 'සංගීතවත්']
rating_keywords = ['ප්‍රසිද්ධ', 'ප්‍රසිද්ද', 'හොඳ', 'හොද', 'ජනප්‍රිය', 'ප්‍රචලිත', 'හොඳම', 'හොදම', 'ජනප්‍රියම', 'වටින', 'වටිනා']
en_genre_keywords = ['Old', 'Pop', 'Classics', 'Inspirational', 'Pops', 'Duets', 'Oldies', 'Calypso', 'Child',
                     'New', 'Golden', 'Current', 'Movie', 'Theme', 'Group']
en_singer_keywords = ['sing', 'sang', 'sung', 'voice', 'artist']
en_writer_keywords = ['written', 'write', 'wrote', 'lyrics']
en_music_keywords = ['music', 'melody', 'sounds', 'musics']
en_rating_keywords = ['famous', 'wow', 'best', 'super', 'rating', 'top']
guitar_keywords = ['major', 'minor', 'Minor', 'Major', 'Flat', 'F#minor']


def get_boosted_fields(dict):

    en_title = "en_title^{}".format(dict["en_title"])
    sn_title = "sn_title^{}".format(dict["sn_title"])
    en_singer = "en_singer^{}".format(dict["en_singer"])
    sn_singer = "sn_singer^{}".format(dict["sn_singer"])
    en_writer = "en_writer^{}".format(dict["en_writer"])
    sn_writer = "sn_writer^{}".format(dict["sn_writer"])
    en_music_artist = "en_music_artist^{}".format(dict["en_music_artist"])
    sn_music_artist = "sn_music_artist^{}".format(dict["sn_music_artist"])
    en_genre = "en_genre^{}".format(dict["en_genre"])
    sn_genre = "sn_genre^{}".format(dict["sn_genre"])
    lyrics = "lyrics^{}".format(dict["lyrics"])
    key = "key^{}".format(dict["key"])

    field_params = [en_title, sn_title, en_singer, sn_singer, en_writer, sn_writer, en_music_artist, sn_music_artist,
            en_genre, sn_genre, lyrics, key]
    return field_params


def is_english(s):
    return re.search('[a-zA-Z]', s)


def search(phrase, index):
    range_flag = False
    result_count = 10

    boosting_dict = {
        "en_title": 2,
        "sn_title": 2,
        "en_singer": 1,
        "sn_singer": 1,
        "en_writer": 1,
        "sn_writer": 1,
        "en_music_artist": 1,
        "sn_music_artist": 1,
        "en_genre": 1,
        "sn_genre": 1,
        "lyrics": 2,
        "key": 1
    }

    if is_english(phrase):
        print("Phrase: ", phrase)
        print("Boosting for english")
        boosting_dict["en_title"] = 3
        boosting_dict["en_singer"] = 2
        boosting_dict["en_writer"] = 2
        boosting_dict["en_music_artist"] = 2
        boosting_dict["en_genre"] = 2
        boosting_dict["key"] = 4

    else:
        print("Phrase: ", phrase)
        print("Boosting for sinhala")
        boosting_dict["sn_title"] = 3
        boosting_dict["sn_singer"] = 2
        boosting_dict["sn_writer"] = 2
        boosting_dict["sn_music_artist"] = 2
        boosting_dict["sn_genre"] = 2
        boosting_dict["lyrics"] = 3

    words = phrase.split()

    for word in words:
        if word.isdigit():
            range_flag = True
            result_count = int(float(word))

        if word in genre_keywords:
            print("Boosting for sn_genre")
            boosting_dict["sn_genre"] = 6

        elif word in singer_keywords:
            print("Boosting for sn_singer")
            boosting_dict["sn_singer"] = 4

        if word in en_genre_keywords:
            print("Boosting for en_genre")
            boosting_dict["en_genre"] = 6

        elif word in en_singer_keywords:
            print("Boosting for en_singer")
            boosting_dict["en_singer"] = 4

        if word in writer_keywords:
            print("Boosting for sn_singer")
            boosting_dict["sn_singer"] = 4

        elif word in en_writer_keywords:
            print("Boosting for en_writer")
            boosting_dict["en_writer"] = 4

        if word in music_keywords:
            print("Boosting for sn_genre")
            boosting_dict["sn_music_artist"] = 5

        elif word in en_music_keywords:
            print("Boosting for en_music_artist")
            boosting_dict["en_music_artist"] = 5

        if word in guitar_keywords:
            print("Boosting for key")
            boosting_dict["key"] = 7

        if word in rating_keywords or word in en_rating_keywords:
            if not range_flag:
                range_flag = True
                result_count = 50

    boosted_fields = get_boosted_fields(boosting_dict)

    if not range_flag:
        query = faceted_multi_match_query(phrase, boosted_fields)

    else:
        query = faceted_multi_match_range(phrase, result_count, boosted_fields)

    print("Query: ", query)
    client = Elasticsearch("localhost:9200")
    respond = client.search(index=index, body=query)

    return respond

