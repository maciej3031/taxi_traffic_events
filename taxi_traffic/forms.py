import itertools

from wtforms import Form, SubmitField, SelectField

from taxi_traffic.couchdb_utils import CouchDBConnection

conn = CouchDBConnection()
artists = list(set([(e.value['artist_name'], e.value['artist_name']) for e in conn.get_all_events()]))
genres = list(set(itertools.chain.from_iterable([e.value['artist_genre'].split(', ') for e in conn.get_all_events()])))
genres = [(e, e) for e in genres]

artists.append(('', ' - '))
genres.append(('', ' - '))


class EventForm(Form):
    artist = SelectField('Artist Name', choices=sorted(artists), default='')
    genre = SelectField('Genre', choices=sorted(genres), default='')
    submit = SubmitField('Show graph!')

    def validate(self):
        return True
