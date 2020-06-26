from scrapy.spiders import SitemapSpider
from datetime import datetime


class SinhalaLyricsSpider(SitemapSpider):
    name = "sinhala_lyrics"
    allowed_domains = ['sinhalasongbook.com']
    sitemap_urls = [
        'https://sinhalasongbook.com/post-sitemap1.xml'
    ]

    def sitemap_filter(self, entries):
        for entry in entries:
            #date_time = datetime.strptime(entry['lastmod'], '%Y-%m-%d')
            year = entry['lastmod'].split('-')[0]
            if year >= '2017':
                yield entry

    song_count = 0

    def parse(self, response):
        song_lines = response.xpath('//*[@class="su-column-inner su-u-clearfix su-u-trim"]/pre/text()').getall()
        # guitar = response.xpath('//*[@class="entry-content"]/h3/text()').get()
        en_title = response.xpath('//*[@class="entry-content"]/h2/text()').get()
        sn_title = response.xpath('//*[@class="entry-content"]/h2/span[@class="sinTitle"]/text()').get()
        genre = response.xpath('//*[@class="entry-tags"]/a/text()').get()
        singer = response.xpath('//*[@class="entry-categories"]/a/text()').get()
        writer = response.xpath('//*[@class="lyrics"]/a/text()').get()
        music = response.xpath('//*[@class="music"]/a/text()').get()
        views = response.xpath('//*[@class="tptn_counter"]/text()').get()

        song = ''
        if song_lines and song_lines != [] and en_title and genre and singer and writer and music and views:
            en_title = en_title.split(' | ')[0]
            if not sn_title:
                sn_title = en_title

            # if guitar:
            #     key = guitar.split(' | ')[0].split(': ')[1]
            #     beat = guitar.split(' | ')[1].split(': ')[1]
            # else:
            #     key = None
            #     beat = None

            for line in song_lines:
                song = song + " " + line.replace("\n", " ").replace("\t", " ")

            yield {
                'en_title': en_title,
                'sn_title': sn_title,
                'genre': genre,
                'singer': singer,
                'writer': writer,
                'music_artist': music,
                # 'key': key,
                # 'beat': beat,
                'lyrics': song,
                'views': int((views.split('- ')[1].split('V')[0]).
                             replace(',', ''))
            }

            self.song_count += 1
            print(self.song_count)
