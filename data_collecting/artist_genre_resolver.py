from music_events import EventContainer
from bs4 import BeautifulSoup
import requests
import time
import random

class ArtistGenreResolver:
    base_url='https://www.allmusic.com/search/all/'
    def __init__(self, container):
        self.container = container

    def resolve_artist_genre(self, artist):
        url = '{}{}'.format(ArtistGenreResolver.base_url,
                            artist.replace(' ', '+'))
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        results = soup.find('ul', {'class' : 'search-results'})
        if(results):
            artist_soup = results.find('li', {'class' : 'artist'})
            if(artist_soup):
                try:
                    genre = artist_soup.find('div', {'class' : 'genres'}).text.strip()
                    self.update_artist(artist, genre)
                except:
                    print("Cannot resolve artist genre - unknown error")
            else:
                print('Cannot get artist form results for {}\turl:{}'.format(artist,url))
        else:
            print('Cannot get any results for {}\turl:{}'.format(artist,url))

    def resolve_all(self):
        for artist in self.container.artists:
            self.resolve_artist_genre(artist)
            time.sleep(random.uniform(0,2))
    
    def update_artist(self, artist, genre):
        self.container.artists[artist].set_genre(genre)