import unittest

class TestCase(unittest.TestCase):
    def setup(self):
        pass
    
    def teardown(self):
        pass
    
def main():
    from sonLib.bioio import parseSuiteTestOptions
    import sys
    parseSuiteTestOptions()
    sys.argv = sys.argv[:1]
    unittest.main()
        
if __name__ == '__main__':
    main()