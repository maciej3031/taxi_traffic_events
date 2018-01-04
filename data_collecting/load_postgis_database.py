import psycopg2
import json

# insert_query = 'INSERT INTO public.neighborhoods(Id, name, geom) VALUES ({}, {}, v)'
# insert_query = 'INSERT INTO public.neighborhoods("Id", name, geom) VALUES ({}, \'{}\', Null);'

insert_query = ''.join(('INSERT INTO public.neighborhoods ("id", "name", "geom") ',
                'VALUES ({}, \'{}\', ST_GeomFromGeoJSON(\'{}\'));'))
class PostGIS_connection:
    db_name = 'tass'
    user_name = 'postgres'
    user_password = 'postgres'
    host = 'localhost'
    table_name = 'public.neighborhoods'
    neighborhood_name_column = 'name'
    def __init__(self):
        self.db = psycopg2.connect(database=self.db_name, user=self.user_name, password=self.user_password, host=self.host)


# SRID for ths data is 4269 - and probbly will work fine
connection = PostGIS_connection()
data = json.load(open('geometry.json'))
for neighborhood in data['features']:
    name = neighborhood['properties']['NTAName'].replace('\'', '')
    id = neighborhood['properties']['OBJECTID']
    geom = str(neighborhood['geometry']).replace('\'', '"')
    cursor = connection.db.cursor()
    cursor.execute(insert_query.format(id, name, geom))
connection.db.commit()