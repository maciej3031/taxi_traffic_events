from datetime import datetime, timedelta

import couchdb


class CouchDBConnection:
    def __init__(self):
        self.db_name = 'tass'
        self.url = 'http://127.0.0.1:5984/'
        self.server = couchdb.Server(self.url)
        self.db = self.server[self.db_name]

    def get_taxi_traffic_n_hours_after_event_start(self, event_time, event_neighbor, n):
        end_datetime = datetime.strptime(event_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=n)
        end_time = datetime.strftime(end_datetime, '%Y-%m-%d %H:%M:%S')
        res = []
        for taxi_course in self.db.view('index/trafficEventsView', startkey=event_time, endkey=end_time):
            pickup_neighbor = taxi_course.value['pickup_neighborhood']
            if pickup_neighbor == event_neighbor:
                res.append(taxi_course)
        print(res[-1])
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
