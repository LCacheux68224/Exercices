# -*- coding:utf-8 -*-
import time    # pour le temps de calcul
from PyQt4.QtGui import *

def layerArea(polygonLayer):
    """
        Area of a polygon layer
        Usage : area = totalLayerArea(polygonLayer)
        """
    features = polygonLayer.getFeatures()
    surface = sum([element.geometry().area() for element in features])
    return surface
    
def attributesSummary(layer, columnNumber):
    """
        Absolute max, min, sum and missing values of a column
        Usage : (max, min, sum, zeroValues)  = attributesSummary(layer, columnNumber)
    """
    features = layer.getFeatures()
    absoluteValuesList = [abs(element.attributes()[columnNumber]) \
        for element in features if element.attributes()[columnNumber]]
    lenList = len(absoluteValuesList)
    if lenList > 0 :
        minimumAbsoluteValue = min(absoluteValuesList)
        maximumAbsoluteValue = max(absoluteValuesList)
        sumAbsoluteValues = sum(absoluteValuesList)
    else :
        maximumAbsoluteValue = NULL
        minimumAbsoluteValue = NULL
        sumAbsoluteValues = NULL        
    zeroValues = int(layer.featureCount()) - lenList
    return minimumAbsoluteValue , maximumAbsoluteValue , sumAbsoluteValues , zeroValues
    
if __name__ == "__main__":
    # récupèration de la couche active du canevas
    coucheActive = qgis.utils.iface.mapCanvas().currentLayer() 

    temps = time.clock()
    surfaceCoucheKm2 = layerArea(coucheActive)/1000000
    print "La surface de %s est de %f km2" % (coucheActive.name(), \
       surfaceCoucheKm2 )
    print 'Temps d''éxécution : %f seconde(s)\n' % (time.clock() - temps)
    temps = time.clock()
    print attributesSummary(coucheActive, 11)
    print 'Temps d''éxécution : %f seconde(s)\n' % (time.clock() - temps)
