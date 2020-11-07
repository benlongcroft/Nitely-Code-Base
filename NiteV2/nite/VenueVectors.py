import datetime
import sqlite3
from geopy.distance import geodesic
import pandas as pd

class GetVenueVectors:
    def __init__(self, smartness, paid, date, TwentyOnePlus, location, location_distance):
        self.paid = paid
        self.TwentyOnePlus = TwentyOnePlus

        self.location = {'lat':location.split(",")[0], 'lng':location.split(",")[1]}
        if location_distance > 50:
            print("Distance is too far to accurately represent club_data")
        try:
            self.LocationCoordinates = location.split(',')
        except Exception as e:
            print('Error splitting coordinates')
            print(e)
        if (smartness <= 5) or (smartness >= 1):
            self.smartness = smartness
        else:
            print('Smartness value is not within valid range')
        try:
            format_str = '%d%m%Y'
            #should be in format DDMMYYYY
            date_str = date
            datetime_obj = datetime.datetime.strptime(date_str, format_str) #converts date into datetime object
            self.date = datetime_obj.date() 
        except Exception as e:
            print('Error when transferring into datetime object')
            print(e)

    @staticmethod
    def GetDistanceBetweenAddress(current_location, y_coordinates):
        #use geopy geodesic module to get distance in miles and return it to function call
        return geodesic((y_coordinates['lat'], y_coordinates['lng']), (current_location['lat'], current_location['lng'])).miles



    def GetValidVenues(self):
        db_obj = sqlite3.connect('./ClubDataDB.db') #connect to database
        cursor_obj = db_obj.cursor()
        command = '''SELECT * FROM venues WHERE dress_rating <= ?''' #generate base command

        if self.TwentyOnePlus == True:
            command = command + ''' AND age_restriction = "over 21s"'''
        if self.paid == False:
            command = command + ''' AND entry_price = no door charge'''
        print(command)
        cursor_obj.execute(command, (self.smartness,)) #execute command

        fields = ["venue_id", "name", "description", "venue_type",
                "age_restriction", "entry_price", "dress_code",
                "dress_rating", "address", "distance"]

        valid_venues_df = pd.DataFrame(columns=fields) #create pandas dataframe

        for record in cursor_obj.fetchall():
            record = list(record) #turn record from tuple to list
            record_coordinates = {'lat':record[-1].split(",")[0], 'lng':record[-1].split(",")[1]} #get coordinates and split them into a dictionary
            distance = self.GetDistanceBetweenAddress(self.location, record_coordinates) #get distance between address and venues
            record.append(distance)
            record = pd.DataFrame([record], columns = fields) #turn record into df so it can be appended
            valid_venues_df = valid_venues_df.append(record, ignore_index=True) #add series to pandas df

        pd.set_option('display.max_columns', None)
        valid_venues_df.sort_values(by=['distance'], inplace=True) #sort by distance from current location
        print(valid_venues_df)



