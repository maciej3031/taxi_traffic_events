import psycopg2

class PostGIS_connection:
    db_name = 'tass'
    user_name = 'postgres'
    user_password = 'postgres'
    host = 'localhost'
    select_neighborhood = 'SELECT name from public.neighborhoods where ST_Contains(geom, ST_GeomFromText(\'POINT({} {})\'))'
    select_all_neighborhoods = 'SELECT name, ST_AsGeoJSON(geom) from public.neighborhoods'

    def __init__(self):
        self.db = psycopg2.connect(database=self.db_name, user=self.user_name, password=self.user_password, host=self.host)

    def get_neighborhood_name(self, lng, lat):
        cursor = self.db.cursor()
        query = self.select_neighborhood.format(lng, lat)
        cursor.execute(query);
        data = cursor.fetchone()
        if (data):
            for row in data:
                return row
        else:
            print('Cannot find neighborhood which contains given point lng: {}, lat: {}'.format(lng, lat))
            return None

    def get_all_neighborhoods_geometry_dict(self):
        cursor = self.db.cursor()
        cursor.execute(self.select_all_neighborhoods)
        data = cursor.fetchall()
        if(data):
            result = {}
            for row in data:
                result[row[0]] = row[1]
            return result
        else:
            print('Cannot get any negighborhoods with geometry')
            return None
