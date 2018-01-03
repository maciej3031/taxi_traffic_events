from wtforms import Form, SubmitField, SelectField

from taxi_traffic.couchdb_utils import CouchDBConnection

conn = CouchDBConnection()
events = list(set([(e.value['artist_name'], e.value['artist_name']) for e in conn.get_all_events()]))
genres = list(set([(e.value['artist_genre'], e.value['artist_genre']) for e in conn.get_all_events()]))

events.append(('', ' - '))
genres.append(('', ' - '))


class EventForm(Form):
    artist = SelectField('Artist Name', choices=sorted(events), default='')
    genre = SelectField('Genre', choices=sorted(genres), default='')
    submit = SubmitField('Show graph!')

    def validate(self):
        return True
