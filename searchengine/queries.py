import json

aggregations = {
			"Sinhala Singer Filter": {
				"terms": {
					"field": "sn_singer.keyword",
					"size": 15
				}
			},
            "Sinhala Writer Filter": {
				"terms": {
					"field": "sn_writer.keyword",
					"size": 15
				}
			},
            "Sinhala Musician Filter": {
                "terms": {
                    "field": "sn_music_artist.keyword",
                    "size": 15
                }
            },
			"Sinhala Genre Filter": {
				"terms": {
					"field": "sn_genre.keyword",
					"size": 15
				}
			},
            "English Singer Filter": {
				"terms": {
					"field": "en_singer.keyword",
					"size": 15
				}
			},
            "English  Writer Filter": {
				"terms": {
					"field": "en_writer.keyword",
					"size": 15
				}
			},
            "English  Musician Filter": {
                "terms": {
                    "field": "en_music_artist.keyword",
                    "size": 15
                }
            },
			"English  Genre Filter": {
				"terms": {
					"field": "en_genre.keyword",
					"size": 15
				}
			}
}


def faceted_multi_match_query(phrase, fields):
    # queries are with weighted boosted fields
    query = {
        "size": 100,
        "query": {
            "multi_match": {
                "query": phrase,
                "fields": fields,
                "operator": 'or',
                "fuzziness": "AUTO"
            }
        },
        "aggs": aggregations
    }

    query = json.dumps(query)
    return query


def faceted_multi_match_range(phrase, results_count, fields):
    print("inside range: ",phrase)
    query = {
        "size": results_count,
        "sort": [
            {"views": {"order": "desc"}},
        ],
        "query": {
            "multi_match": {
                "query": phrase,
                "fields": fields,
                "operator": 'or'
            }
        },
        "aggs": aggregations
    }
    print(query)
    query = json.dumps(query)
    return query


