segmentGraph.sqg
_________________________________

>>>
{
    "include": [
        "multigraph"
    ], 
    "labelledSegment": [
        {
            "inherits": "segment", 
            "variables": [
                "sequence", 
                "string"
            ]
        }
    ], 
    "multiLabelledSegment": [
        {
            "inherits": "multiSegment", 
            "variables": [
                "sequence", 
                "string"
            ]
        }
    ], 
    "multiSegment": [
        {
            "inherits": "multiDirectedEdge", 
            "variables": [
                "length", 
                "int"
            ]
        }
    ], 
    "segment": [
        {
            "inherits": "directedEdge", 
            "variables": [
                "length", 
                "int"
            ]
        }
    ]
}
