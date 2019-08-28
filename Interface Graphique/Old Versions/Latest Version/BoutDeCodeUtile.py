#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 20:21:28 2018

@author: adrien
"""
import os.path as pt

chemin=pt.split(pt.abspath(""))
while chemin[1]!='PSC':
    chemin=pt.split(chemin[0])
chemin=chemin[0]+'/'+chemin[1]
print(chemin)