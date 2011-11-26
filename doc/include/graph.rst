graph.sqg
_________________________________

>>>
{
    "edge": [
        {
            "variables": [
                "node1", 
                "int", 
                "node2", 
                "int"
            ]
        }
    ], 
    "include": [], 
    "node": [
        {
            "variables": [
                "nodeName", 
                "int"
            ]
        }
    ], 
    "subgraph": [
        {
            "sharedVariables": {
                "edges": [
                    "edge"
                ]
            }, 
            "variables": [
                "subgraphName", 
                "int", 
                "nodes", 
                "array"
            ]
        }
    ]
}
