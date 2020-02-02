XML file Handler
========================================================

A Python script ```main.py``` in which the following input could be specified:
- path to the .xml file (directly, .xml path is hard code);
- path to the .xsd file (an .xml file should be generated according to this scheme) (directly, .xsd path is hard code);
- path to the .xsl file and the name of the resulting file (also .xml) (directly, .xsl path is hard code).

The script takes the .xml file along the path, checks it in accordance with the .xsd, then performs the xslt conversion in accordance with xslt, then checks the result in accordance with the xsd scheme and saves the resulting XML file to a file (resulting.xml).

Preparation:

* pip install requirements.txt

* python3 main.py

* Open the ```log.txt``` to see the result of the script main.py

NOTE!
For the code to work, you must use the python interpreter version 3.6 or latter, because in code uses
LSI. 
[PEP 498 - Literal String Interpolation](https://www.python.org/dev/peps/pep-0498/)
