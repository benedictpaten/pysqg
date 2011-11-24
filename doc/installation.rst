Installation
============

Getting the code
----------------

The following assumes that pysqg is being installed on a unix based system.

To install pysqg you will need to use git (http://git-scm.com/) to clone the repository.
Providing that git is installed, running the following command::

	git clone git@github.com:benedictpaten/pysqg.git

will download the latest stable (master) branch of pysqg, creating a ``pysqg`` directory in the 
current working directory.

Locating and testing pysqg
--------------------------

To use pysqg you will need Python (http://python.org/) installed. It will work with Python 2.7, but
will also probably work with earlier versions of python.

Currently pysqg does not have a ``setup.py`` to install the module. Hence currently you will need
to ensure that when using pysqg it is locatable by the python interpretor. This can probably
be most easily achieved by adding the directory containing the pysqg directory 
to the PYTHONPATH environment variable. 

For example::

	PYTHONPATH=${PYTHONPATH}:pathToDirectoryContainingPysqg
	
To test that the package is correctly being located in the python interpretor issue the command::

>>> import pysqg
>>>

No error should occur.

To test the installation issue the command::

	python allTests.py
	
in the pysqg base directory. You should get a report of no errors.

Building the documentation
--------------------------

To build this documentation you will need sphinx (http://sphinx.pocoo.org/). 
This is most easily acquired using ``easy install'' or ``pip''. For example the command::

	easy_install sphinx
	
will install the sphinx. Once installed issue the command::

	sphinx-build . doc

from the pysqg base directory to build the documentation as browseable html.

External tools
--------------

Pysqg also has tools for working with popular tools such as 
mongodb (http://www.mongodb.org/), numpy (http://numpy.scipy.org/) and 
networkX (http://networkx.lanl.gov/). To use pysqg with these external tools will require 
their separate installation.
