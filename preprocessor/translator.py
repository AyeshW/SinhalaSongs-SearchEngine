import pandas as pd
from googletrans import Translator


def translate():
    translator = Translator()
    df = pd.read_json('../scraper/lyrics/song_lyrics.json')
    print(df.shape)

    cols_to_trans = ['en_singer', 'en_writer', 'en_genre', 'en_music_artist']
    new_cols = ['sn_singer', 'sn_writer', 'sn_genre', 'sn_music_artist']
    index = 0
    for col in cols_to_trans:
        temp = []
        print(col)
        for i in df[col]:
            translated = translator.translate(i, dest='sinhala').text
            while (1):
                if i == translated:
                    print(i, translated)
                    translated = translator.translate(i, dest='sinhala').text
                    print("translated again")
                    print(i, translated)
                else:
                    break
            temp.append(translated)
        df[new_cols[index]] = temp
        index += 1

    print(df.shape)
    print(df.head())

    df.to_json('sinhala_songs_corpus.json', orient='records')

    output = df.to_json(orient='records')[1:-1].replace('},{', '} {')

    with open('corpus_elastic_format.txt', 'w') as f:
        f.write(output)

if __name__ == '__main__':
    translate()
