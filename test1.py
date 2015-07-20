import sys
sys.path.append("/home/lionel/Documents/Python")

from fonctionsCarto import *
coucheActive = qgis.utils.iface.mapCanvas().currentLayer()
attributesSummary(coucheActive, 11)
