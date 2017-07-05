from pymongo import MongoClient
import pprint as pp

class mongoHelper(object):
    def __init__(self):
        self.client = MongoClient()

        self.db_airports = self.client.world_data.airports
        self.db_cities = self.client.world_data.cities
        self.db_countries = self.client.world_data.countries
        self.db_earthquakes = self.client.world_data.earthquakes
        self.db_meteorites = self.client.world_data.meteorties
        self.db_states = self.client.world_data.states
        self.db_terrorism = self.client.world_data.terrorism
        self.db_volcanos = self.client.world_data.volcanos

    def count_collections(self,col_name):
        if col_name == 'airports':
            res = self.db_airports.count()
            return res
        elif col_name == 'cities':
            res = self.db_cities.count()
            return res
        elif col_name == 'countries':
            res = self.db_countries.count()
            return res
        elif col_name == 'earthquakes':
            res = self.db_earthquakes.count()
            return res
        elif col_name == 'states':
            res = self.db_states.count()
            return res
        elif col_name == 'volcanos':
            res = self.db_volcanos.count()
            return res
        else:
            pass

    def get_doc_by_keyword(self,col_name,field,key):
        if col_name == 'airports':
            res = self.db_airports.find({field : {'$regex' : ".*"+key+".*"}})
        
        res_list = []
        for r in res:
            res_list.append(r)

        return res_list

mc = mongoHelper()
num_airports = mc.count_collections('airports')
print("The number of airports is: ",num_airports)
num_states = mc.count_collections('states')
print("The number of states is: ",num_states)


