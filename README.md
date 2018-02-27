# Shapefile To Network
Construct network from shapefile and find number of shortest paths from origin to destination.

## Overview
This python module allow you to get information of number of delta shortest pahts from origin to destination where delta is some constant specified by the user. You can also do some analysis over the network like finding degree, centrality of the nodes in graph.

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
  python2.7 setup.py install
  ```
## Documentation
#### Core Scripts 

* _GraphConvertor.py_ - This module will take the input line shapefile and the path of output directory 
* _ShortestPath.py_ -   This module will calculate the number of *alpha* times shortest path from origin to destination in the graph

#### Other Scripts 

* _BufferedGraph.py_ - This module create the square (*buffer*) around the point geometry specified by user 
* _GraphSimplify.py_ - This module will clean and remove all the unusable edges from the graph 
* _MultiDiGraphConvertor.py_ - This module will convert the MultiDiGraph to SimpleGraph 


## How to use
* Create the line shapefile of the road network (if not available already)

  * Using QGIS
    - Open the shapefile in QGIS which need to be converted to line shapefile
    - Go to **_Vector_ -> _Geometry Tools_** and select **_Polygons to lines_** to convert shapefile into line shapefile
    
  * Using python
    - Need to be implemented
    
* Convert the created line shapefile into network using **_GraphConvertor.py_**

  * Create **_GraphConvertor_** object by passing the path of input shapefile and the output directory
    ```
    graph_convertor_obj = GraphConvertor(input_file, output_dir)
    ```
  * Call **_graph_convertor_** function to convert the input shapefile into road network and save the newly created shapefile into specifed **_output_dir_**
    ```
    network = graph_convertor_obj.graph_convertor()
    ```
  
* Find number of shortest paths from origin to destination in new network

  * Run **_alpha_times_shortestpath_** function in **_ShortestPath.py_** script to calculate number of paths which are alpha times the shortest path.
    
