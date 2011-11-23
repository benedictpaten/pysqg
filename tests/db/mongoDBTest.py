import unittest
import os
from pymongo import Connection
from pysqg.bioio import getTempFile
from pysqg.dbs.mongoDB import mongoDBWrite, mongoDBRead
from pysqg.arrayList import InMemoryArrayList
from pysqg.tests.abstractTests import AbstractTestCase

class TestCase(AbstractTestCase):
    def setUp(self):
        """Constructs a simple graph to writes it into mongodb then reads it back out.
        """
        AbstractTestCase.setUp(self)
        sqg, graph = self.makeGraph(InMemoryArrayList)
        connection = Connection()
        database = connection["sqg"]
        mongoDBWrite(sqg, database)
        def fn():
            tempFile = getTempFile(rootDir=os.getcwd())
            self.tempFiles.append(tempFile)
            return tempFile
        self.graphs = ((mongoDBRead(database), graph), (mongoDBRead(database, tempFileGenerator=fn), graph))

def main():
    from pysqg.bioio import parseSuiteTestOptions
    import sys
    parseSuiteTestOptions()
    sys.argv = sys.argv[:1]
    unittest.main()
        
if __name__ == '__main__':
    main()