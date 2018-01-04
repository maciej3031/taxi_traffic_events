class Location:
    def __init__(self, name):
        self.name = name
        self.lng = None
        self.lat = None
        self.neighborhood = None

    def set_lat(self, lat):
        self.lat = lat

    def set_lng(self, lng):
        self.lng = lng
    
    def set_neighborhood(self, neighborhood):
        self.neighborhood = neighborhood

    def __str__(self):
        return('name: {}, lat: {}, lng: {}, neighborhood: {}'.format(self.name, self.lat, self.lng, self.neighborhood))

class Artist:
    def __init__(self, name):
        self.name = name
        self.genre = None

    def set_genre(self, genre):
        self.genre = genre

    def __str__(self):
        return('Name: {}, genre: {}'.format(self.name, self.genre))

class Event:
    def __init__(self, date, location, artist):
        self.date = date
        self.location_key = location
        self.artist_key = artist
        self.location = None
        self.artist = None

    def __str__(self):
        return ('date: {}\nlocation: {}\nartist: {}'.format(self.date, self.location_key, self.artist_key))
    
    def set_location(self, location):
        self.location = location

    def set_artist(self, artist):
        self.artist = artist

class EventContainer:
    def __init__(self):
        self.events = []
        self.locations = {}
        self.artists = {}

    def add_event(self, name, location_key, artist_key):
        event = Event(name, location_key, artist_key)
        print(event)
        self.events.append(event)
        if (location_key not in self.locations):
            self.locations[location_key] = Location(location_key)
        if (artist_key not in self.artists):
            self.artists[artist_key] = Artist(artist_key)

    def print_locations(self):
        for l in self.locations:
            print(self.locations[l])

    def print_artists(self):
        for a in self.artists:
            print(self.artists[a])

    def get_complete_event_data(self):
        complete_events = []
        for e in self.events:
            e.set_location(self.locations[e.location_key])
            e.set_artist(self.artists[e.artist_key])
            print(e.location)
            if(e.artist.genre and e.location.neighborhood):
                complete_events.append(e)
            else:
                print("Skipping event because of incomplete data")
        return complete_events