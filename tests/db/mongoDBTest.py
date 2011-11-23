import unittest
import pymongo

from pysqg.dbs.mongoDB import mongoDBWrite, mongoDBRead

class TestCase(unittest.TestCase):
    def setup(self):
        pass
    
    def teardown(self):
        pass
    
    def testMongoDBWriteAndRead(self):
        """Writes an example graph into mongo DB, then extracts it back out.
        """
        

def main():
    from sonLib.bioio import parseSuiteTestOptions
    import sys
    parseSuiteTestOptions()
    sys.argv = sys.argv[:1]
    unittest.main()
        
if __name__ == '__main__':
    main()
    