#!usr/bin/env python
# -*- coding: utf-8 -*-

'''a shitty little a-z lyrics scraper for texty fun.
returns a json file of all the lyrics by a given artist by song.
azlyrics doesn't like scraping (eep) so use with caution!'''

from pattern.web import URL, DOM, abs, plaintext
import re, argparse, json

BASE_URL = 'http://www.azlyrics.com/'

def all_lyrics(artist):
	clean = re.sub(r"\s+|'", '', artist)
	url = URL(BASE_URL + artist[0] + '/' + clean + '.html')
	dom = DOM(url.download())
	titles = [a.content for a in dom('div#listAlbum a')]
	ew_amazon = [abs(link.attributes.get('href', ''), base=url.redirect or
		url.string) for link in dom('div#listAlbum a')]
	songlinks = [l for l in ew_amazon if 'amazon' not in l]
	lyrics = []
	for link in songlinks:
		song_url = URL(link)
		song_dom = DOM(song_url.download())
		lyrics.append(plaintext(song_dom('div#main div')[4:5][0].content))
	zippy_lyrics = zip(titles, lyrics)
	return json.dumps(zippy_lyrics, sort_keys=True)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('artist', type=str, help='artist to get lyrics from.')
	args = parser.parse_args()
	fname = args.artist + '-lyrics.json'
	with open(fname, 'w') as f:
		f.write(all_lyrics(args.artist))
