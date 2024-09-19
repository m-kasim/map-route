import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import networkx as nx
import osmnx as ox

def geocode_address(address):
    geolocator = Nominatim(user_agent="route_planner")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        raise ValueError(f"Address '{address}' not found.")

def get_shortest_route(start_lat_lon, end_lat_lon):

    # Set map region
    map_region    = input("Area of Map (Format: `Zurich, Switzerland`)")

    # Create a graph of the driving network around Sofia
    G = ox.graph_from_address( map_region, dist=10000, network_type='drive')

    # Find the nearest nodes to the start and end locations
    start_node = ox.nearest_nodes(G, start_lat_lon[1], start_lat_lon[0])
    end_node = ox.nearest_nodes(G, end_lat_lon[1], end_lat_lon[0])

    # Compute the shortest path between the start and end nodes
    shortest_route = nx.shortest_path(G, start_node, end_node, weight='length')

    return G, shortest_route

def plot_route_on_map(G, route):
    # Plot the graph and route using osmnx
    fig, ax = ox.plot_graph_route(G, route, route_linewidth=4, node_size=0, bgcolor='white')

if __name__ == "__main__":
    
    start_address = input("Enter the starting address: ")
    end_address = input("Enter the destination address: ")

    # Geocode addresses to get latitude and longitude
    start_lat_lon = geocode_address(start_address)
    end_lat_lon = geocode_address(end_address)

    # Get the shortest route between the two points
    G, shortest_route = get_shortest_route(start_lat_lon, end_lat_lon)

    # Plot the route on the map
    plot_route_on_map(G, shortest_route)
