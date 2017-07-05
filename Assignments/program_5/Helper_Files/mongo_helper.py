import os,sys
import math
from pymongo import MongoClient

class MongoHelper(object):
    def __init__(self):
        self.client = MongoClient()

    def get_features_near_me(self,collection,point,radius,earth_radius=3963.2): #km = 6371
        """
        Finds "features" within some radius of a given point.
        Params:
            collection_name: e.g airports or meteors etc.
            point: e.g (-98.5034180, 33.9382331)
            radius: The radius in miles from the center of a sphere (defined by the point passed in)
        Usage:
            mh = mongoHelper()
            loc = (-98.5034180, 33.9382331)
            miles = 200
            feature_list = mh.get_features_near_me('airports', loc, miles)
        """
        x,y = point

        res = self.client['world_data'][collection].find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , radius/earth_radius ] } }} )
        
        return self._make_result_list(res)

    def get_doc_by_keyword(self,collection,field_name,search_key,like=True):
        """
        Finds "documents" with some keyword in some field.
        Params:
            collection_name: e.g airports or meteors etc.
            field_name: key name of the field to search. e.g. 'place_id' or 'magnitude' 
            search_key: The radius in miles from the center of a sphere (defined by the point passed in)
        Usage:
            mh = mongoHelper()
            feature_list = mh.get_doc_by_keyword('earthquakes','properties.type','shakemap')
            # Returns all earthquakes that have the word 'shakemap' somewhere in the 'type' field
        """
        if like:
            # This finds the records in which the field just "contains" the search_key
            res = self.client['world_data'][collection].find(({field_name : {'$regex' : ".*"+search_key+".*"}}))
        else:
            # This finds the records in which the field is equal to the search_key
            res = self.client['world_data'][collection].find({field_name : search_key})

        return self._make_result_list(res)


    def get_feature_in_poly(self,collection,poly):
        """
        Get features that are "in" a polygon
        Params:
            collection_name: e.g airports or meteors etc.
            poly: geojson polygon
        Usage:
            mh = mongoHelper()
            feature_list = mh.get_feature_in_poly('airports',country['coordinates'])
            # Returns all airports in the given country polygon.
        """
        res = self.client['world_data'][collection].find( { 'geometry' : { '$geoWithin' : { '$geometry' : {'type': "Polygon", 'coordinates': poly }} } })

        return self._make_result_list(res)

    def get_poly_by_point(self,collection,point):
        """
        Get a polygon that a point is within
        Params:
            collection_name: e.g airports or meteors etc.
            point: geojson point
        Usage:
            mh = mongoHelper()
            feature_list = mh.get_poly_by_point('countries',[44.2968750,24.6669864])
            # Returns the country that point([44.2968750,24.6669864]) is within (Saudi Arabia)
        """
        return self.client['world_data'][collection].find_one({'geometry':{'$geoIntersects':{'$geometry':{ "type" : "Point","coordinates" : point }}}})

    def _make_result_list(self,res):
        """
        private method to turn a pymongo result into a list
        """
        res_list = []
        for r in res:
            res_list.append(r)

        return res_list

    def get_state_poly(self,state):
        """
        Send in a state name (e.g. Texas) or code (e.g. tx) and it returns the geometry
        """
        state = state.lower()
        if len(state) == 2:
            field = 'properties.code'
        else:
            state = state.capitalize()
            field = 'properties.name'

        state_poly = self.client['world_data']['states'].find_one({field : state})
        return state_poly['geometry']

    def get_country_poly(self,key):
        """
        Send in a country name (e.g. Belarus) or code (e.g. BLR) and it returns the geometry
        """
        country_poly = None
        if len(key) == 3:
            country_poly = self.client['world_data']['countries'].find_one({'properties.SU_A3' : key})
        if country_poly is None:
            print("Error retrieving %s polygon." % key)
            return None
        return country_poly['geometry']

    def get_all(self,collection,filter={},projection={'_id':0}):
        res = self.client['world_data'][collection].find(filter,projection)
        return self._make_result_list(res)
    

    def _haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        r = 3956 # Radius of earth in kilometers. Use 6371 for km
        return c * r

def run_tests():
    """
    Ok, not really "tests" but mostly just exmaples....
    """
    mh = MongoHelper()

    print("Getting airports near within 200 miles of: (-98.5034180, 33.9382331)")
    res = mh.get_features_near_me('airports',(-98.5034180, 33.9382331),200)
    print("Found %d airports" % len(res))
    print("")

    print("Getting countries that have 'High income' in the INCOME_GRP field.")
    res = mh.get_doc_by_keyword('countries','properties.INCOME_GRP','High income')
    print("Found %d countries" % len(res))
    print("")

    print("Getting earthquakes that had a magnitude of 5.5 (not a partial match like above), and don't pass in 5.5 as a string!")
    res = mh.get_doc_by_keyword('earthquakes','properties.mag',5.5,False)
    print("Found %d earthquakes" % len(res))
    print("")

    print("Getting a state polygon.")
    state = mh.get_state_poly('co')
    print("Found %d polygon in the result." % len(state['coordinates']))
    print("")

    print("Getting all airports within the state poly from the previous query.")
    res = mh.get_feature_in_poly('airports',state['coordinates'])
    print("Found %d airports in the polygon." % len(res))
    print("")
   
    # Getting polygon data for Belgium
    country = mh.get_country_poly('BEL')

    # This query chokes on countries with type: MultiPolygon, but works on Polygon. 
    # I'm investigating ... (If we think about it, we probaly just need run one 
    # query per polygon within the "multi" polygon. 
    print("Getting all airports within the country poly from the previous query.")
    res = mh.get_feature_in_poly('airports',country['coordinates'])
    print("Found %d airports in the polygon." % len(res))
    print("")

    print("Getting the country that encompasses the point [44.2968750,24.6669864]")
    res = mh.get_poly_by_point('countries',[44.2968750,24.6669864])
    print("That country is: %s" % (res['properties']['NAME_LONG']))

    res = mh.get_all('airports')
    print(len(res))

if __name__=='__main__':

    run_tests()
