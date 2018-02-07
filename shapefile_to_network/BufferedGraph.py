import geopandas as gpd
from GraphSimplify import *

def find_buffer_endpoints(geometry, to_crs):
    gdf = gpd.GeoDataFrame()
    gdf.crs = to_crs
    gdf['geometry'] = None
    gdf.loc[0, 'geometry'] = geometry
    reprojected_point = gdf.to_crs({'init':'epsg:4326'})
    geometry_proj = reprojected_point['geometry'].iloc[0]
    return geometry_proj, reprojected_point.crs

def project_point(geometry):
    gdf = gpd.GeoDataFrame()
    gdf.crs = {'init':'epsg:4326'}
    gdf['geometry'] = None
    gdf.loc[0, 'geometry'] = geometry

    utm_crs = {
               'ellps': 'WGS84',
               'proj': 'utm',
               'zone': '48N',
               'units': 'm'
                }
    reprojected_point = gdf.to_crs(utm_crs)
    geometry_proj = reprojected_point['geometry'].iloc[0]
    return geometry_proj, reprojected_point.crs

def create_buffer(bufferSize, geometry):
    geom, geo_proj = project_point(geometry)
    buffer_proj = geom.buffer(bufferSize)
    new_geo, new_proj =  find_buffer_endpoints(buffer_proj, geo_proj)
    print new_geo.bounds
    return new_geo.bounds

def combine_network_buffer(G, geometry, bufferSize):
    west, south, east, north = create_buffer(bufferSize, geometry)
    buffered_G = G.copy()
    external_node = []
    for node in buffered_G.nodes():
        node_long = node[1]
        node_lat = node[0]
        if node_lat > north or node_lat < south or node_long > east or node_long < west:
            immediate_neighbours = list(buffered_G.successors(node)) + list(buffered_G.predecessors(node))

            keep_node = False
            for neigh in immediate_neighbours:
                neigh_lat = neigh[0]
                neigh_long = neigh[1]

                if neigh_lat < east and neigh_lat > west and neigh_long < north and neigh_long > south:
                    keep_node = True

            if not keep_node:
                external_node.append(node)

    buffered_G.remove_nodes_from(external_node)
    return simplify_graph(buffered_G)

