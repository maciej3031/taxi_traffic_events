import requests
from bs4 import BeautifulSoup
import time
import random
from music_events import EventContainer

#url = 'https://www.songkick.com/search?page=21&query=New+York+12+September+2015&utf8=%E2%9C%93'
#myURL = https://maps.googleapis.com/maps/api/geocode/json?address=City+Winery,+New+York,%20NY,%20US&key=AIzaSyCU26Bi3YTeiwPLFs3fv0KL8FdlMFC4Q-4

class MusicEventScraper:
    base_url = 'https://www.songkick.com'
    first_page = '/search?utf8=%E2%9C%93&query='
    def __init__(self, city, month, year, container):
        city = city.replace(' ', '+')
        self.current_page = 1
        self.current_soup = None
        self.container = container
        self.url = '{}{}{}+{}+{}'.format(MusicEventScraper.base_url,
                                         MusicEventScraper.first_page, city, month, year)

    def get_soup(self):
        r = requests.get(self.url)
        print('status code {}'.format(r.status_code))
        if(r.status_code == 200):
            self.current_soup = BeautifulSoup(r.text, 'lxml')
            return r.status_code
        else:
            print('Error while getting html content from url')
            return r.status_code

    def find_next_page_in_soup(self):
        navigation_div = self.current_soup.find('div', {'class' : 'pagination'})
        next_page = navigation_div.find('a', {'class' : 'next_page'})
        if(next_page):
            self.url = MusicEventScraper.base_url + next_page['href']
            return 0
        else:
            print('Cannot find next page link')
            return -1

    def find_events_in_soup(self): 
        print('Checking for all events on this page, we\'re skipping festival events')
        found_events = self.current_soup.findAll('li', {'class' : 'concert event'})
        print('Found {} events on page!'.format(len(found_events)))
        for event_soup in found_events:
            date = event_soup.find('time')['datetime']
            location = event_soup.find('p', {'class' : 'location'}).text.strip()
            artist = event_soup.find('p', {'class' : 'summary'}).find('strong').text
            self.container.add_event(date, location, artist)

    def find_all_events(self):
        while(True):
            if(200 == self.get_soup()):
                self.find_events_in_soup()
                if(0 == self.find_next_page_in_soup()):
                    time.sleep(random.uniform(0,2))
                else:
                    print('Cannot collect more music events')
                    return 0
            else:
                print('Error while getting soup from url')
                return -1
