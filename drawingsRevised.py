# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 09:19:19 2023

@author: rghs
"""

import numpy as np
import pandas as pd
import drawSvg as d

def greater(x,y):
    '''
    Returns greater of two numbers entered. Accepts floats and ints.

    '''
    if(x>y):
        return x
    else:
        return y

class log:
    def __init__(self, pageheight=None, pagewidth=None, standard=None):
        if standard is not None:
            standard = standard.lower()
        
        standardSizes = [(279,216), # Letter
                         (432,279), # Tabloid
                         (356,216), # Legal
                         (420,297), # A3
                         (297,210), # A4
                         (210,148)] # A5
        standardNames = ['letter','tabloid','legal',
                        'a3','a4','a5']
        
        if standard in standardNames:
            self.pageheight = standardSizes[standardNames.index(standard)][0]
            self.pagewidth = standardSizes[standardNames.index(standard)][1]
        elif(isinstance(pageheight,(float,int)) and isinstance(pagewidth,(float,int))):
            self.pageheight = pageheight
            self.pagewidth = pagewidth
        elif((standard not in standardNames) and (pageheight is None) and (pagewidth is None)):
            raise ValueError(f'{standard} is inappropriate value for standard page size.')
        elif((isinstance(pageheight,(float,int)) is False) or (isinstance(pagewidth,(float,int))) is False):
            raise TypeError('Arguments for pageheight and pagewidth must be of type "int" or "float".')
        else:
            raise Exception('Unexpected input value.')
        
        
    def __str__(self):
        return f'Log page size:\nHeight: {self.pageheight} mm\nWidth: {self.pagewidth} mm'
    
    def drawCanvas(self):
        self.canvas = d.Drawing(self.pagewidth,
                                self.pageheight,
                                origin=(0,0),
                                displayInline=False)
    
    def assignGrainSizes(self, grainSizeCodes = 'default', grainSizeWidths = 'default', logWidth = 75):
        defaultGrainSizeCodes = pd.Series(['NaN',
                                           'cl','si',
                                           'vf','f','m','c','vc',
                                           'gr','pebb','cobb','boul'])
        defaultGrainSizeWidths = pd.Series([0.1,
                                            0.2, 0.3,
                                            0.4, 0.45, 0.5, 0.55, 0.6,
                                            0.7, 0.8, 0.9, 1.0])
        # Error handling clauses
        if((grainSizeCodes == 'default') and (grainSizeWidths != 'default')):
            if(len(defaultGrainSizeCodes) != len(grainSizeWidths)):
                raise ValueError(f'Length of grainSizeWidths must equal length of default grainSizeCodes array ({len(defaultGrainSizeCodes)})')
        
        if((grainSizeCodes != 'default') and (grainSizeWidths == 'default')):
            if(len(defaultGrainSizeWidths) != len(grainSizeCodes)):
                raise ValueError(f'Length of grainSizeCodes must equal length of default grainSizeWidths array ({len(defaultGrainSizeWidths)})')
        
        if(len(grainSizeCodes) != len(grainSizeWidths)):
            raise ValueError('grainSizeCodes and grainSizeWidths must be of identical length.')
        
        # Value assignment
        if(grainSizeCodes == 'default'):
            self.grainSizeCodes = defaultGrainSizeCodes
        else:
            self.grainSizeCodes = pd.Series(grainSizeCodes)
        
        if(grainSizeWidths == 'default'):
            self.grainSizeWidths = defaultGrainSizeWidths * logWidth
        else:
            self.grainSizeWidths = grainSizeWidths * logWidth
        
        if((grainSizeCodes == 'default') and (grainSizeWidths == 'default')):
            self.grainSizeCodes = pd.Series(['NaN',
                                             'cl','si',
                                             'vf','f','m','c','vc',
                                             'gr','pebb','cobb','boul'])
            self.grainSizeWidths = pd.Series([0.1,
                                              0.2, 0.3,
                                              0.4, 0.45, 0.5, 0.55, 0.6,
                                              0.7, 0.8, 0.9, 1.0])*logWidth
        if((grainSizeCodes == 'default') or (grainSizeWidths == 'default')):
            raise TypeError('Either both or neither of grainSizeCodes and grainSizeWidths should be "default".')
        elif(len(grainSizeCodes) != len(grainSizeWidths)):
            raise ValueError('grainSizeCodes and grainSizeWidths must be of identical length.')
        else:
            self.grainSizeCodes = pd.Series(grainSizeCodes)
            self.grainSizeWidths = pd.Series(grainSizeWidths)
            
    def assignFacies(self, faciesCodes = 'default', faciesColors = 'default'):
        if((faciesCodes == 'default') and (faciesColors == 'default')):
            self.faciesCodes = pd.Series(['inaccessible','cov',
                                           'fcm','fcl','fcr','fcrc','fcrw',
                                           'fsm','fsl','fsr','fsrc','fsrw',
                                           'sm','sh','sp','st','sr','src','srw',
                                           'gmm','gmmi',
                                           'gcm','gcmi','gcp','gct','gch'])
            self.faciesColors = pd.Series(['#FFFFFF','#FFFFFF',
                                            '#5A4854','#74576A','#8C627E','#A57093','#D998C1',
                                            '#666154','#807969','#99917D','#B3A993','#CCC1A7',
                                            '#E3AB4A','#DBB75C','#FDBB45','#FBB672','#FFCE6F','#EE9621','#F68C35',
                                            '#99834F','#E5C376',
                                            '#661714','#8D211D','#B22C26','#D93328','#EF4130'])
        elif((faciesCodes == 'default') or (faciesColors == 'default')):
            raise TypeError('Either both or neither of faciesCodes and faciesColors should be "default".')
        elif(len(faciesCodes) != len(faciesColors)):
            raise ValueError('faciesCodes and faciesColors must be of identical length.')
        else:
            self.faciesCodes = pd.Series(faciesCodes)
            self.faciesColors = pd.Series(faciesColors)
    
x = log(standard='A4')
print(x)