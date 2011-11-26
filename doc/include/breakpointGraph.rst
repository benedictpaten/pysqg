breakpointGraph.sqg
_________________________________

{
    "adjacency": [
        {
            "inherits": "edge"
        }
    ], 
    "group": [
        {
            "inherits": "subgraph", 
            "sharedVariables": {
                "edges": [
                    "adjacency", 
                    "multiAdjacency"
                ]
            }
        }
    ], 
    "include": [
        "multigraph"
    ], 
    "multiAdjacency": [
        {
            "inherits": "multiEdge"
        }
    ]
}
