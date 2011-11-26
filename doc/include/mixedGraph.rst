mixedGraph.sqg
_________________________________

{
    "directedEdge": [
        {
            "variables": [
                "outNode", 
                "int", 
                "inNode", 
                "int"
            ]
        }
    ], 
    "directedSubgraph": [
        {
            "inherits": "subgraph", 
            "sharedVariables": {
                "edges": [
                    "directedEdge"
                ]
            }
        }
    ], 
    "include": [
        "graph"
    ], 
    "mixedSubgraph": [
        {
            "inherits": "subgraph", 
            "sharedVariables": {
                "edges": [
                    "edge", 
                    "directedEdge"
                ]
            }
        }
    ]
}
