"""Pretty prints the various sqg files in the include hierarchy
"""

import os
from pysqg.bioio import system
from pysqg.shared import getPysqgIncludeDir, getPysqgBaseDir

for file in os.listdir(getPysqgIncludeDir()):
    if ".json" in file:
        include = file[:-5]
        absFile = os.path.join(getPysqgIncludeDir(), file)
        outFile = os.path.join(getPysqgBaseDir(), "doc", "include", include + ".rst")
        outFileHandle = open(outFile, 'w')
        outFileHandle.write("%s.sqg\n_________________________________\n\n>>>\n" % include)
        outFileHandle.close()
        system("cat %s | python -mjson.tool >> %s" % (absFile, outFile))
    