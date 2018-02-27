import geopandas as gpd

from shapefile_to_network.main.convertor.GraphSimplify import GraphSimplify

'''
    @input:     point geometry and the crs geometry crs
    @output:    reprojected geometry and the crd of the geometry

    This function a new geometry with given crs ann return it
'''


def find_buffer_endpoints(geometry, to_crs):
    gdf = gpd.GeoDataFrame()
    gdf.crs = to_crs
    gdf['geometry'] = None
    gdf.loc[0, 'geometry'] = geometry
    reprojected_point = gdf.to_crs({'init': 'epsg:4326'})
    geometry_proj = reprojected_point['geometry'].iloc[0]
    return geometry_proj, reprojected_point.crs

'''
    @input:     point geometry
    @output:    reprojected geometry and the crd of the geometry

    This function create a new geometry with given crs ann return it
'''


def project_point(geometry):
    gdf = gpd.GeoDataFrame()
    gdf.crs = {'init': 'epsg:4326'}
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

'''
    @input:     Buffersize and the point geometry
    @output:    bounds of new graph

    This function create the buffer around point geometry and then return the north, south, east, west cooordunate of
    bound
'''


def create_buffer(buffer_size, geometry):
    geom, geo_proj = project_point(geometry)
    buffer_proj = geom.buffer(buffer_size)
    new_geo, new_proj = find_buffer_endpoints(buffer_proj, geo_proj)
    return new_geo.bounds

'''
    @input:     MultiDigraph, point geometry to create buffer, size of buffer
    @output:    Simplified MultiDiGraph

    This function returns the simplified subgraph of given buffer around the point geometry.
'''


def combine_network_buffer(g, geometry, buffer_size):
    west, south, east, north = create_buffer(buffer_size, geometry)
    buffered_g = g.copy()
    external_node = []
    for node in buffered_g.nodes():
        node_long = node[1]
        node_lat = node[0]
        if node_lat > north or node_lat < south or node_long > east or node_long < west:
            immediate_neighbours = list(buffered_g.successors(node)) + list(buffered_g.predecessors(node))

            keep_node = False
            for neigh in immediate_neighbours:
                neigh_lat = neigh[0]
                neigh_long = neigh[1]

                if west < neigh_lat < east and south < neigh_long < north:
                    keep_node = True

            if not keep_node:
                external_node.append(node)

        buffered_g.remove_nodes_from(external_node)

    simplify_graph = GraphSimplify(buffered_g)
    return simplify_graph.simplify_graph()

