import unittest
import os
import json
from sonLib.bioio import getTempFile, logger
from pysqg.sqg import jsonRead, jsonWrite, getPysqgIncludeDir

class TestCase(unittest.TestCase):  
    def setUp(self):
        self.tempFile = getTempFile(rootDir=os.getcwd())
        self.jsonFiles = ("graph", "mixedGraph", "multiGraph", "breakpointGraph", "adjacencyGraph", "segmentGraph", "phylogeneticTree", "dnaHistoryGraph")
    
    def tearDown(self):
        os.remove(self.tempFile)
    
    def testParseJsonFiles(self):
        for include in self.jsonFiles:
            logger.info("Going to parse %s" % include)
            fileHandle = open(os.path.join(getPysqgIncludeDir(), include + ".json"), 'r')
            json.load(fileHandle)
            fileHandle.close()
    
    def testJsonRead(self):
        for include in self.jsonFiles:
            logger.info("Going to use jsonRead to parse to SQG %s" % include)
            fileHandle = open(os.path.join(getPysqgIncludeDir(), include + ".json"), 'r')
            sqg = jsonRead(fileHandle)
            fileHandle.close()
    
    def testJsonWrite(self):
        for include in self.jsonFiles:
            logger.info("Going to use jsonRead to parse/write/parse SQG %s" % include)
            #First read
            fileHandle = open(os.path.join(getPysqgIncludeDir(), include + ".json"), 'r')
            sqg = jsonRead(fileHandle)
            fileHandle.close()
            #Then write
            fileHandle = open(self.tempFile, 'w')
            jsonWrite(sqg, fileHandle)
            fileHandle.close()
            
            #Now parse again
            fileHandle = open(self.tempFile, 'r')
            jsonRead(fileHandle)
            fileHandle.close()
            

def main():
    from sonLib.bioio import parseSuiteTestOptions
    import sys
    parseSuiteTestOptions()
    sys.argv = sys.argv[:1]
    unittest.main()
        
if __name__ == '__main__':
    main()