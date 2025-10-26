# -*- coding:utf-8 -*-
"""
Module de fonctions utilitaires pour QGIS 3.x+
Compatible Qt5 et Qt6
"""
import time  # pour le temps de calcul

# Import compatible Qt5/Qt6 via qgis
try:
    from qgis.PyQt.QtWidgets import *
    from qgis.PyQt.QtGui import *
    from qgis.PyQt.QtCore import *
except ImportError:
    # Fallback pour anciennes versions
    try:
        from PyQt5.QtWidgets import *
        from PyQt5.QtGui import *
        from PyQt5.QtCore import *
    except ImportError:
        from PyQt6.QtWidgets import *
        from PyQt6.QtGui import *
        from PyQt6.QtCore import *


def layerArea(polygonLayer):
    """
    Area of a polygon layer

    Args:
        polygonLayer: QGIS polygon layer

    Returns:
        float: Total area of all features in the layer

    Usage:
        area = layerArea(polygonLayer)
    """
    features = polygonLayer.getFeatures()
    surface = sum([element.geometry().area() for element in features])
    return surface


def attributesSummary(layer, columnNumber):
    """
    Absolute max, min, sum and missing values of a column

    Args:
        layer: QGIS layer
        columnNumber: Column index to analyze

    Returns:
        tuple: (min, max, sum, zeroValues)

    Usage:
        (max_val, min_val, sum_val, missing) = attributesSummary(layer, columnNumber)
    """
    features = layer.getFeatures()
    absoluteValuesList = [abs(element.attributes()[columnNumber])
                          for element in features if element.attributes()[columnNumber]]
    lenList = len(absoluteValuesList)

    if lenList > 0:
        minimumAbsoluteValue = min(absoluteValuesList)
        maximumAbsoluteValue = max(absoluteValuesList)
        sumAbsoluteValues = sum(absoluteValuesList)
    else:
        maximumAbsoluteValue = None
        minimumAbsoluteValue = None
        sumAbsoluteValues = None

    zeroValues = int(layer.featureCount()) - lenList
    return minimumAbsoluteValue, maximumAbsoluteValue, sumAbsoluteValues, zeroValues


if __name__ == "__main__":
    # Récupération de la couche active du canevas
    import qgis.utils
    coucheActive = qgis.utils.iface.mapCanvas().currentLayer()

    temps = time.perf_counter()
    surfaceCoucheKm2 = layerArea(coucheActive) / 1000000
    print(f"La surface de {coucheActive.name()} est de {surfaceCoucheKm2:.2f} km2")
    print(f"Temps d'exécution : {time.perf_counter() - temps:.6f} seconde(s)\n")

    temps = time.perf_counter()
    stats = attributesSummary(coucheActive, 11)
    print(f"Statistiques colonne 11: {stats}")
    print(f"Temps d'exécution : {time.perf_counter() - temps:.6f} seconde(s)\n")
