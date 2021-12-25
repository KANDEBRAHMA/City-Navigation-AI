#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name IU ID
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
import pandas as pd
import heapq as hq
import math

#This function idea is referred from https://python.plainenglish.io/calculating-great-circle-distances-in-python-cf98f64c1ea0
def heuristic_distance(lat1=0, lon1=0, lat2=0, lon2=0):
    del_Lon = (lon2-lon1)
    del_sigma = math.acos(math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(del_Lon))
    distance = 0.5*3959*del_sigma
    return math.sqrt(distance)

def successors(road_segments,start_city):
    successors_routes = []
    for i in road_segments:
        if i[1] == start_city:
            successors_routes.append(i)
    return successors_routes

def route_found(route,destination):
    if route[3] == destination:
        return True
    return False

def calculate_distances(city_gps,current_node,stop):
    city1_lat,city1_lon,city2_lat,city2_lon = 0,0,0,0
    for city in city_gps:
        if city[0] == current_node:
            city1_lat = city[1]
            city1_lon = city[2]
        if city[0] == stop:
            city2_lat = city[1]
            city2_lon = city[2]
    return heuristic_distance(city1_lat,city1_lon,city2_lat,city2_lon)

def path_taken(route):
    travelled_so_far=[]
    for i in range(0,len(route)-8,8):
        node = route[i:i+6]
        path = list()
        path.append(node[3])
        path.append("{} for {} miles".format(node[5],node[1]))
        travelled_so_far.insert(0,tuple(path))
    return travelled_so_far


def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    data = pd.read_csv("road-segments.txt", delimiter=r"\s+", names=['Starting_Point','Ending_point','distances','Speed_limit','Highway_number'])
    data1 = pd.read_csv("city-gps.txt", delimiter=r"\s+",names=['City','latitudes','longitudes'])
    data["time_taken"]=data.distances/data.Speed_limit
    data["delivery_time"] = 0
    for i in range(0,data.shape[0]):
        if data['Speed_limit'].iloc[i] >= 50:
            data["delivery_time"].iloc[i] = float(math.tanh((data['distances'].iloc[i]/1000)))
        else:
            data["delivery_time"].iloc[i] = float(0)
    columns_names = ['distances','Starting_Point','Ending_point','Speed_limit','Highway_number','time_taken','delivery_time']
    columns_names1 = ['distances','Ending_point','Starting_Point','Speed_limit','Highway_number','time_taken','delivery_time']
    goal_found = False
    city_gps = data1.to_numpy().tolist()
    data1 = data.reindex(columns=columns_names)
    data2 = data.reindex(columns=columns_names1)
    road_segments = data1.to_numpy().tolist()
    road_segments1 = data2.to_numpy().tolist()
    road_segments = road_segments+road_segments1
    max_dist = data1['Speed_limit'].max()
    explored_route = []
    frontier = [[0,0,start,start,'','',0,0]]
    hq.heapify(frontier)
    while frontier:
        route = hq.heappop(frontier)
        if route_found(route,end):
            goal_found = True
            break
        explored_route.append(route)
        for succ_route in successors(road_segments,route[3]):
            route_in_frontier = False
            if cost == 'distance':
                if calculate_distances(city_gps,succ_route[2],end) == 0:
                    distance_covered = route[0]+succ_route[0]
                else:
                    distance_covered = calculate_distances(city_gps,succ_route[2],end)+route[0]
            elif cost == 'segments':
                distance_covered = 1+route[0]
            elif cost == 'time':
                distance_covered = calculate_distances(city_gps,succ_route[2],end)/max_dist+route[0]
            elif cost == 'delivery':
                delivery = succ_route[5] + (2*succ_route[6]*succ_route[5])
                if calculate_distances(city_gps,succ_route[2],end) == 0:
                    distance_covered = route[0]+delivery
                else:
                    distance_covered = delivery + calculate_distances(city_gps,succ_route[2],end) + route[0]
            for step in frontier:
                if step[3] == succ_route[2] and step[2] == succ_route[1]:
                    route_in_frontier = True
                    break
            if succ_route not in explored_route and not route_in_frontier:
                succ_route.insert(0,distance_covered)
                hq.heappush(frontier,succ_route+route)

    total_miles,total_hours,delivery = 0.0,0,0
    if goal_found:
        route_taken = path_taken(route)
        for i in range(0,len(route)-8,8):
            node=route[i:i+8]
            total_miles = total_miles+node[1]
            total_hours = total_hours+node[6]
            delivery = delivery + node[6] + (2*node[7]*total_hours)
        return {"total-segments" : len(route_taken), 
            "total-miles" : total_miles, 
            "total-hours" : total_hours, 
            "total-delivery-hours" : delivery, 
            "route-taken" : route_taken}
    else:
        return {"total-segments" : len([]), 
            "total-miles" : total_miles, 
            "total-hours" : total_hours, 
            "total-delivery-hours" : delivery, 
            "route-taken" : []}

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


