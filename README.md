# Shapefile To Network
Construct a network from shapefile and do analytics such as finding number of shortest paths from origin to destination, calculating centrality, degree of the nodes in network.

## Overview
This python module allow you to get number of alpha times shortest paths from origin to destination where alpha is some constant specified by the user. You can also do some analysis over the network like finding degree, centrality of the nodes in graph.

#### Original Network

<br/><img src = "https://github.com/Garvit244/Shapefile_to_Network/blob/master/shapefile_to_network/Images/Original_Network.png" height="450" width ="450" alight="left"> 

#### New Simplified Network

<br/> <img src = "https://github.com/Garvit244/Shapefile_to_Network/blob/master/shapefile_to_network/Images/New_Network.png" height="450" width ="450"> 


## Installation

* Install python >= 2.7 
  * Ubuntu
    ```
    $ sudo apt-get install python-2.7
    ```
    
  * Mac
    ```
    $ brew install python
    ```
* Run **_setup.py_** for installing required packages

  ```
  $ python2.7 setup.py install
  ```
## Documentation
#### Core Scripts 

* _GraphConvertor.py_  - This module will take the input line shapefile and the path of output directory 
* _ShortestPath.py_    - This module will calculate the number of _alpha_ times shortest path from origin to destination in the graph

#### Other Scripts 

* _BufferedGraph.py_ - This module create the square (_buffer_) of given size around the point geometry 
* _GraphSimplify.py_ - This module will clean and remove all the redundant edges and extra/ uninformative nodes from the graph 
* _MultiDiGraphConvertor.py_ - This module will convert the MultiDiGraph to SimpleGraph 


## How to use
* Create the line shapefile of the road network (if not available)

  * Using QGIS
    - Open the shapefile in QGIS which need to be converted to line shapefile
    - Go to **_Vector_ -> _Geometry Tools_** and select **_Polygons to lines_** to convert shapefile into line shapefile
    
  * Using python
    - Need to be implemented
    
* Convert the created line shapefile into network using **_GraphConvertor.py_**

  * Create **_GraphConvertor_** object by passing the path of input shapefile and the output directory
  
    ```python
    input_file  =  'path of the line shapefile'
    output_dir  =  'path of directory to save new shapefiles'
    
    graph_convertor_obj = GraphConvertor(input_file, output_dir)
    ```
  * Call **_graph_convertor_** function to convert the input shapefile into road network and save the newly created shapefile into specifed **_output_dir_** along with list of nodes and edges in _.csv_ files
  
    ```python
    network = graph_convertor_obj.graph_convertor()
    ```
  
* Find number of shortest paths from origin to destination in new simplified network

  * Create **_ShortestPath_**  object by passing all required parameters listed below
  
     ```python
     g            =  network
     alpha        =  0.1
     graph_buffer =  100
     point_buffer =  50
     break_point  =  200         # Upper limit to save computation time

     shortest_path_obj   =  ShortestPath(g, alpha, graph_buffer, point_buffer, break_point)
     ```
     
   * Run **_alpha_times_shortestpath_** function to calculate number of paths which are alpha times the shortest path
  
     ```python
     start_tuple  =  (lat,lon)
     end_tuple    =  (lat,lon)

     total_path   =  shortest_path_obj.alpha_time_shortestpath(start_tuple, end_tuple)
     ```
* Find metrics like degree centrality, closeness centrality, communicability and load centrality for doing analysis over created network.
 
  * Create **_Centrality_** object by passing the network and the weight attribute of the network
   
    ```python
    centrality = Centrality(g, weight='distance')
    ```

  * Get all the metrics of the network by calling **_metrics_** function of centrality class

    ```python
    degree_centrality, closeness_centrality, communicability, load_centrality = centrality.metrics()
    ```
    
