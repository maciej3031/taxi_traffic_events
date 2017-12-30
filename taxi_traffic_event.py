class Taxi_traffic_event:
    def __init__(self, pickup_datetime, dropoff_datetime,
                 pickup_neighborhood, dropoff_neighborhood):
        self.pickup_datetime = pickup_datetime
        self.dropoff_datetime = dropoff_datetime
        self.pickup_neighborhood = pickup_neighborhood
        self.dropoff_neighborhood = dropoff_neighborhood