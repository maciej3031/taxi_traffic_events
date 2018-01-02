from wtforms import Form, SubmitField, SelectField

from taxi_traffic.couchdb_utils import CouchDBConnection

conn = CouchDBConnection()
events = [(e.id, "{}/{}".format(e.value['artist_name'], e.value['datetime'])) for e in conn.get_all_events()]


class EventForm(Form):
    event = SelectField('Artist Name', choices=events)
    submit = SubmitField('Show graph!')

    def validate(self):
        return True
