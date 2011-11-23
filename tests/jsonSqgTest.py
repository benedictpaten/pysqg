import unittest
import os
import json
from sonLib.bioio import logger, getTempFile
from pysqg.sqg import readJsonSqgFile, writeJsonSqgFile, makeJsonSqgFromSqg, makeSqgFromJsonSqg, getPysqgIncludeDir

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
    
    def testMakeSqgFromJsonSqg(self):
        for include in self.jsonFiles:
            logger.info("Going to use json.load to parse to json sqg %s" % include)
            fileHandle = open(os.path.join(getPysqgIncludeDir(), include + ".json"), 'r')
            jsonSqg = json.load(fileHandle)
            sqg = makeSqgFromJsonSqg(jsonSqg)
            fileHandle.close()
    
    def testMakeJsonSqgFromSqg(self):
        for include in self.jsonFiles:
            logger.info("Going to use json.load to parse to json sqg %s" % include)
            fileHandle = open(os.path.join(getPysqgIncludeDir(), include + ".json"), 'r')
            jsonSqg = json.load(fileHandle)
            sqg = makeSqgFromJsonSqg(jsonSqg)
            fileHandle.close()
            jsonSqg2 = makeJsonSqgFromSqg(sqg)
    
    def testJsonReadAndWriteSqg(self):
        for include in self.jsonFiles:
            logger.info("Going to use jsonRead to parse/write/parse SQG %s" % include)
            #First read
            file = os.path.join(getPysqgIncludeDir(), include + ".json")
            sqg = readJsonSqgFile(file)
            #Then write
            writeJsonSqgFile(sqg, self.tempFile)
            #Now parse again
            readJsonSqgFile(self.tempFile)
        
def main():
    from sonLib.bioio import parseSuiteTestOptions
    import sys
    parseSuiteTestOptions()
    sys.argv = sys.argv[:1]
    unittest.main()
        
if __name__ == '__main__':
    main()