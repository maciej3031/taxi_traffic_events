import csv
from postGIS_connection import PostGIS_connection
from taxi_traffic_event import Taxi_traffic_event

class Traffic_event_loader():
    def __init__(self, filename):
        self.filename = filename
        self.db = PostGIS_connection()

    def load_data(self):
        result = []
        with open(self.filename, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader, None)
            for row in reader:
                pickup_datetime = row[1]
                dropoff_datetime = row[2]
                pickup_lng = row[5]
                pickup_lat = row[6]
                pickup_neighborhood = self.db.get_neighborhood_name(pickup_lng, pickup_lat)
                dropoff_lng = row[9]
                dropoff_lat = row[10]
                dropoff_neighborhood = self.db.get_neighborhood_name(dropoff_lng, dropoff_lat)
                if(pickup_neighborhood and dropoff_neighborhood):
                    result.append(Taxi_traffic_event(pickup_datetime, dropoff_datetime, pickup_neighborhood, dropoff_neighborhood))
        return result