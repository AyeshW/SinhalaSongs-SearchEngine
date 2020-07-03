# SinhalaSongs-SearchEngine
This project is to build a search engine for searching sinhala songs

## Directory Structure
Important directory paths are mentioned here.
```bash
.
├── corpus
│   ├── raw_data.json
│   ├── sinhala_songs_corpus.json
│   └── unicode_converted_data.json
├── preprocessor : Source code for the translator
├── scraper : Source code for the website scraper
├── searchengine
    ├── app.py
    ├── index.py
    ├── queries.py
    └── search.py
```

## Corpus
Sinhala Songs Corpus contains 538 song lyrics with their meta data. The corpus is created by scraping this [website.](https://sinhalasongbook.com/)

The corpus consists of 12 fields.
- en_title        - Song title in English
- en_genre        - Genre of the song in English
- en_singer       - Name of the singer in English
- en_writer       - Name of the writer in English
- en_music_artist - Name of the music artist in English
- key             - Guitar key of the song
- lyrics          - Lyrics of the song in Sinhala
- views           - Number of views for the song on the website
- sn_title        - Song title in Sinhala
- sn_genre        - Genre of the song in Sinhala 
- sn_singer       - Name of the singer in Sinhala
- sn_writer       - Name of the writer in Sinhala
- sn_music_artist - Name of the music artist in Sinhala

## Main Functionalities of the System
- Rule-based text mining - Separate list of keywords are stored for several fields, and the search query is checked for those keywords in order to boost fields.
- Rule-based text classification - Based on the keywords in the search query, the query is classified as a range query or not.
  - eg: පණ්ඩිත් අමරදේව ගැයූ **හොඳම** ගීත / Best songs **sung** by Pandith Amaradewa
- Range Queries - Range queries are used to get most popular songs in a sorted order with specifying the number of search results or not
  - eg: රත්න ශ්‍රී ලියූ වටිනම සින්දු 10 / Best of Kalpana Kavindi
- Faceting - This gives meta-information about search results.
- Bilingual Support - The search engine can be used to search lyrics or metadata of songs in both Sinhala and English language.

## Getting Started
### Prerequisites
- Elastic Search 7.8+
- Python 3+ should be installed on your PC.

### Steps
- Clone the repository
- Install the requirements.txt using `pip install requirements.txt`
- Start an Elastic Search instance on your PC
- Move into the searchengine directory and run `python3 -m index.py` for indexing the corpus in Elastic Search
- For setting up a flask server at [http://127.0.0.1:5000/](http://127.0.0.1:5000/) run below commands 
    ```
        export FLASK_APP=app
        flask run
    ```
Now you can send POST requests to *http://127.0.0.1:5000/sinhala-songs/search/q=YOUR-SEARCH-STRING* using Postman tool or CLI.
