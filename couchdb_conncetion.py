import couchdb
from couchdb.design import ViewDefinition
import sys
from uuid import uuid4

events_data_selector = '''function(doc) {
    if (doc.type == 'event')
        emit(doc.datetime, doc);
}'''

events_names_selector = '''function(doc) {
    if (doc.type == 'event')
        emit(doc.artist, null);
}'''

neighborhoods_shapes_selector = '''function(doc) {
    if (doc.type == 'neighborhood')
        emit(doc.name, doc);
}'''

traffic_events_selector = '''function(doc) {
    if (doc.type == 'taxi')
        emit(doc.pickup_datetime, doc);
}'''


class CouchDB_connection:
    event_skeleton = {
        '_id': '',
        'type': 'event',
        'datetime': '',
        'location_name': '',
        'artist_name': '',
        'artist_genre': '',
        'lat': '',
        'lng': '',
        'neighborhood': ''
    }

    def __init__(self):
        dbname = 'tass'
        url = 'http://127.0.0.1:5984/'
        self.server = couchdb.Server(url)
        if dbname in self.server:
            self.db = self.server[dbname]
        else:
            self.db = self.server.create(dbname)
        self.viewEventDoc = ViewDefinition('index', 'eventDocView', events_data_selector)
        self.viewEventDoc.sync(self.db)
        self.viewEventName = ViewDefinition('index', 'eventNameView', events_names_selector)
        self.viewEventName.sync(self.db)
        self.viewNeighborhoodShape = ViewDefinition('index', 'neighborhoodsShapesView', neighborhoods_shapes_selector)
        self.viewNeighborhoodShape.sync(self.db)
        self.viewTrafficEvents = ViewDefinition('index', 'trafficEventsView', traffic_events_selector)
        self.viewTrafficEvents.sync(self.db)

    def save_events(self, events):
        for e in events:
            self.db.save(self.create_event_document(e))

    def create_event_document(self, event):
        to_save = self.event_skeleton
        to_save['_id'] = uuid4().hex
        to_save['artist_name'] = event.artist.name
        to_save['artist_genre'] = event.artist.genre
        to_save['location_name'] = event.location.name
        to_save['lat'] = event.location.lat
        to_save['lng'] = event.location.lng
        to_save['datetime'] = event.date
        to_save['neighborhood'] = event.location.neighborhood
        return to_save

    def create_neighborhood_document(self, name, geometry):
        doc = {}
        doc['_id'] = uuid4().hex
        doc['type'] = 'neighborhood'
        doc['name'] = name
        doc['geometry'] = geometry
        return doc

    def save_neighborhoods_geometries(self, neighborhoods_dict):
        for el in neighborhoods_dict:
            doc = self.create_neighborhood_document(el, neighborhoods_dict[el])
            self.db.save(doc)

    def get_events_within_range(self, start_date, end_date):
        res = []
        for el in self.db.view('index/eventDocView', startkey=start_date, endkey=end_date):
            res.append(el)
        return res

    def get_all_events(self):
        res = []
        for el in self.db.view('index/eventNameView'):
            res.append(el)
        return res

    def get_neighborhoods(self):
        res = []
        for el in self.db.view('index/neighboroodsShapeView'):
            res.append(el)
        return res

    def save_traffic_events(self, events):
        for el in events:
            doc = vars(el)
            doc['_id'] = uuid4().hex
            doc['type'] = 'taxi'
            self.db.save(doc)