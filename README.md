# Path-Finding
Algorithms implemnetation for path search problems and random test case generator.

Files:
    1. path_finding_algorithms.py: contains implemnetation and execution of all algorithms.
    2. random_path_generator.py: generate random graphs for testing.
    3. graph_gui.py: draws the graphs or solutions on a GUI.
    4. utilis.py: contains all utility functions that can be useful.

How to run:
    1. Run random path generator: "py random_path_generator.py {i} -d" with:
        - i: number of graph needed to be generated.
        - -d: draw the graph, leave blank for not drawing.
    2. Run path search: "py path_finding_algorithms.py test_{i}.txt {algorithms}" with:
        - i: increment everytime new test was generated, started from 1. Can also be "-a" if all files needed to be tested.
        - algorithms: can be: DFS, BFS, GBFS, AS, CUS1, or CUS2. Can also be "-a" if all algorithms needed to be tested.