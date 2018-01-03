from scrap_music_events import MusicEventScraper
from music_events import EventContainer
from geolocation_resolver import GeolocationResolver
from artist_genre_resolver import ArtistGenreResolver
from couchDB_connection import CouchDB_connection 
from postGIS_connection import PostGIS_connection
from trafic_events_loader import Traffic_event_loader

traffic_event_loader = Traffic_event_loader('2015-10_100k.csv')
traffic_events = traffic_event_loader.load_data()

container = EventContainer()

music_events_scraper = MusicEventScraper('New York City', 'October', '2015', container)
music_events_scraper.find_all_events()

geolocation_resolver = GeolocationResolver(container)
geolocation_resolver.resolve_all()

artist_resolver = ArtistGenreResolver(container)
artist_resolver.resolve_all()

db = CouchDB_connection()
db.save_traffic_events(traffic_events)
db.save_events(container.get_complete_event_data())

# db.save_neighborhoods_geometries(PostGIS_connection().get_all_neighborhoods_geometry_dict())
