#!/usr/bin/env python3
"""
Setup skript pro kompilaci C modulu pro detekci okrajů
"""

from setuptools import setup, Extension
import numpy as np

# Definice C extension
edge_detection_extension = Extension(
    'edge_detection',
    sources=['edge_detection.c'],
    include_dirs=[np.get_include()],
    libraries=['m'],  # Matematická knihovna pro math.h
    # Dočasně odstraněny všechny extra přepínače pro debug
)

setup(
    name='edge_detection',
    version='0.0.1',
    description='Rychlá detekce okrajů v C pro BleedMakr',
    author='BleedMakr Team',
    ext_modules=[edge_detection_extension],
    install_requires=['numpy>=1.21.0'],
    python_requires='>=3.8',
) 