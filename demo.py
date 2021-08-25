# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 14:49:39 2021

@author: RGHS
"""

import sys
sys.path.append('.')#('D:/code/git/sedlog-maker')
import pandas as pd
import numpy as np
import drawSvg as draw
import drawings as dr

export = False

src = pd.read_csv('D:/code/git/sedlog-maker/testdata.csv')
src = src.fillna('NaN')

gs_codes, gs_widths = dr.grainsize()
f_codes, f_colors = dr.faciesList()
el = dr.elevs(src.thickness)
can = dr.canvas()

x = dr.drawLog(el, src.gs_base, src.gs_top, src.code,
               gs_codes, gs_widths,
               f_codes, f_colors, can,
               vscale = 500, debug = False)

if export is True:
    x.saveSvg('D:/code/git/sedlog-maker/test.svg')