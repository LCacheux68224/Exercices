# -*- coding:utf-8 -*-
"""
Module de fonctions utilitaires pour QGIS 3.x+
Compatible Qt5 et Qt6 via qgis.PyQt

Nécessite d'être exécuté dans l'environnement QGIS
"""
import time  # pour le temps de calcul

# Imports Qt via qgis.PyQt (méthode recommandée QGIS 3.x)
# S'adapte automatiquement à Qt5 ou Qt6 selon la version de QGIS
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *


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
        tuple: (min, max, sum, zeroValues) or None if column index is invalid

    Usage:
        (max_val, min_val, sum_val, missing) = attributesSummary(layer, columnNumber)
    """
    # Vérifier que la couche a des champs
    fields = layer.fields()
    if columnNumber < 0 or columnNumber >= len(fields):
        print(f"Erreur: L'index de colonne {columnNumber} est invalide. La couche a {len(fields)} champs (0 à {len(fields)-1}).")
        return None, None, None, None

    features = layer.getFeatures()
    absoluteValuesList = []

    for element in features:
        attrs = element.attributes()
        # Vérifier que l'élément a assez d'attributs et que la valeur n'est pas nulle
        if len(attrs) > columnNumber and attrs[columnNumber] is not None:
            try:
                absoluteValuesList.append(abs(attrs[columnNumber]))
            except (TypeError, ValueError):
                # Ignorer les valeurs non numériques
                pass

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

    if coucheActive is None:
        print("Erreur: Aucune couche active sélectionnée")
    else:
        print(f"=== Analyse de la couche : {coucheActive.name()} ===\n")

        # Afficher les champs disponibles
        fields = coucheActive.fields()
        print(f"Nombre de champs : {len(fields)}")
        print("Champs disponibles :")
        for idx, field in enumerate(fields):
            print(f"  [{idx}] {field.name()} ({field.typeName()})")
        print()

        # Test de la fonction layerArea pour les couches de polygones
        if coucheActive.geometryType() == 2:  # 2 = Polygon
            temps = time.perf_counter()
            surfaceCoucheKm2 = layerArea(coucheActive) / 1000000
            print(f"Surface totale : {surfaceCoucheKm2:.2f} km²")
            print(f"Temps d'exécution : {time.perf_counter() - temps:.6f} seconde(s)\n")
        else:
            print("La couche n'est pas de type polygone, calcul de surface ignoré.\n")

        # Test de la fonction attributesSummary sur la première colonne numérique
        numeric_types = ['Integer', 'Integer64', 'Real', 'Double']
        for idx, field in enumerate(fields):
            if field.typeName() in numeric_types:
                temps = time.perf_counter()
                stats = attributesSummary(coucheActive, idx)
                print(f"Statistiques pour '{field.name()}' (colonne {idx}):")
                print(f"  Min: {stats[0]}, Max: {stats[1]}, Somme: {stats[2]}, Valeurs manquantes: {stats[3]}")
                print(f"  Temps d'exécution : {time.perf_counter() - temps:.6f} seconde(s)\n")
                break
        else:
            print("Aucune colonne numérique trouvée pour les statistiques.")
