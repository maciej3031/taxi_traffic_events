from datetime import datetime, timedelta
from config import DB_NAME, DB_URL

import couchdb


class CouchDBConnection:
    def __init__(self):
        self.db_name = DB_NAME
        self.url = DB_URL
        self.server = couchdb.Server(self.url)
        self.db = self.server[self.db_name]

    def get_taxi_traffic_n_hours_after_event(self, event_time, event_neighbor, n):
        end_datetime = datetime.strptime(event_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=n)
        end_time = datetime.strftime(end_datetime, '%Y-%m-%d %H:%M:%S')
        res = []
        for taxi_course in self.db.view('index/trafficEventsView', startkey=event_time, endkey=end_time):
            if taxi_course.value['pickup_neighborhood'] == event_neighbor:
                res.append(taxi_course)
        return res

    def get_all_events(self):
        res = []
        for event in self.db.view('index/eventDocView'):
            res.append(event)
        return res

    def get_event_by_id(self, id):
        for event in self.db.view('index/eventDocView'):
            if event.id == id:
                return event

    def get_events_by_genre(self, genre):
        res = []
        for event in self.db.view('index/eventDocView'):
            if genre in event.value['artist_genre']:
                res.append(event)
        return res

    def get_events_by_artist(self, artist):
        res = []
        for event in self.db.view('index/eventDocView'):
            if event.value['artist_name'] == artist:
                res.append(event)
        return res
