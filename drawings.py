# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 11:54:34 2021

@author: RGHS

Subordinate functions for sed log maker
"""

import pandas as pd
import numpy as np
import drawSvg as draw
import warnings

def greater(x,y):
    if(x>y):
        return x
    else:
        return y

def grainsize(sizes = None, width = None, wunit = 'mm'):
    if(wunit not in  ['mm','in','pt']):
        raise Exception('Width unit must be either "mm","in" or "pt".')
    if((sizes is None) and (width is not None)) or ((sizes is not None) and (width is None)):
        raise Exception('Both sizes and widths must be provided if custom categories are being used.')
    elif(sizes is None and width is None):
        grain = np.array(("NaN",
                          "cl","si",
                          "vf","f","m","c","vc",
                          "gr","pebb","cobb","boul"))
        widths = np.array((0.1,
                          0.2, 0.3,
                          0.4, 0.45, 0.5, 0.55, 0.6,
                          0.7, 0.8, 0.9, 1.0))
        widths *= 75
    elif((hasattr(sizes, '__len__') is False) or (hasattr(width, '__len__') is False)):
        warnings.warn('Either length or sizes has no length attribute. This means that you have provided only one category in either. This is likely to produce very strange behaviour and should be reconsidered.')
    else:
        if(len(sizes) != len(width)):
            raise Exception('Sizes and widths must be of identical length.')
        # Convert lists into arrays
        if(isinstance(sizes, np.ndarray) is False):
            sizes = np.array(sizes)
        if(isinstance(width, np.ndarray) is False):
            width = np.array(width)
        # Convert widths to pts
        if(wunit == 'mm'):
            widths = width * 2.8346456692913
        elif(wunit == 'in'):
            widths = width / 72
        else:
            widths = width
            
        grain = sizes
    
    grain = pd.Series(grain)
    widths = pd.Series(widths)    
    return grain, widths

def faciesList(codes = None, colors = None):
    if((codes is None) and (colors is not None)) or ((codes is not None) and (colors is None)):
        raise Exception('Both codes and colors must be provided if custom categories are being used.')
    elif(codes is None and colors is None):
        fcodes = np.array(("inaccessible","cov",
                           "fcm","fcl","fcr","fcrc","fcrw",
                           "fsm","fsl","fsr","fsrc","fsrw",
                           "sm","sh","sp","st","sr","src","srw",
                           "gmm","gmmi",
                           "gcm","gcmi","gcp","gct","gch"))
        fcolors = np.array(("#FFFFFF","#FFFFFF",
                            "#723F94","#723F94","#723F94","#723F94","#723F94",
                            "#7E6B71","#7E6B71","#7E6B71","#7E6B71","#7E6B71",
                            "#FED54A","#FED54A","#FED54A","#FED54A","#FED54A","#FED54A","#FED54A",
                            "#FEC77C","#FEC77C",
                            "#C9AC68","#C9AC68","#C9AC68","#C9AC68","#C9AC68"))
    elif((hasattr(codes, '__len__') is False) or (hasattr(colors, '__len__') is False)):
        warnings.warn('Either codes or colors has no length attribute. This means that you have provided only one category in either. This is likely to produce very strange behaviour and should be reconsidered.')
    else:
        if(len(codes) != len(colors)):
            raise Exception('Codes and colors must be of identical length.')
        # Convert lists into arrays
        if(isinstance(codes, np.ndarray) is False):
            fcodes = np.array(codes)
        if(isinstance(colors, np.ndarray) is False):
            fcolors = np.array(colors)
    
    fcodes = pd.Series(fcodes)
    fcolors = pd.Series(fcolors)
    return fcodes, fcolors

def elevs(thicknesses):
    if(hasattr(thicknesses, '__len__') is False):
        raise Exception('Thicknesses data has no length attribute, meaning only on thickness reading was provided.')
    if(isinstance(thicknesses, np.ndarray) is False):
        thicknesses = np.array(thicknesses)
    
    elevation = np.zeros(len(thicknesses)+1)
    x = 0.0
    for i in range(0,len(thicknesses)):
        x += thicknesses[i]
        elevation[i+1] = x
    
    elevation = pd.Series(elevation)
    return elevation

def canvas(width = 0, height = 0, standard = 'letter'):
    sheets = pd.Series(['letter', 'legal', 'tabloid',
                       'a3', 'a4', 'a5'])
    if((width == 0) and (height == 0) and (standard in sheets.values)):
        stdw = np.array([215.9, 215.9, 279.4,
                         297, 210, 148])
        stdh = np.array([279.4, 355.6, 431.8,
                         420, 297, 210])
        cw = stdw[sheets[sheets == standard].index[0]]
        ch = stdh[sheets[sheets == standard].index[0]]
    elif((width > 0) and (height > 0)):
        cw = width
        ch = height
    else:
        raise Exception('Incorrect width, height or standard size provided.')
    
    # Convert sizes from mm to pt
    cw *= 2.8346456692913
    ch *= 2.8346456692913
    
    # Construct drawSvg canvas
    canvas = draw.Drawing(cw, ch, origin = (0,0), displayInline = False)
    
    return canvas

def drawLog(elevations, grain_base, grain_top, facies, gs_codes, gs_widths,
            fcodes, fcolors, canv, orig = 30, pad = 5, lnwgt = 0.5, columns = 4,
            vscale = 100, debug = True):
    # Figure out page spacing
    colheight = canv.height-(orig + pad)
    t_len = (elevations[len(elevations)-1] * 1000 * 2.8346456692913)/vscale #vscale * 2.8346456692913 * elevations[len(elevations)-1]
    avail_len = pd.Series(np.array(list(range(1,columns + 1))) * colheight)
    if(pd.isna(avail_len[avail_len>t_len].index.min()) is True):
        error = (f'Not sufficient vertical space with {columns} columns and vertical scale of {vscale}:1.',
                        'Choose a smaller vscale or increase max columns.',
                        f'Available length: {max(avail_len)}, total length of column: {t_len}')
        raise Exception(error)
    else:
        cols = avail_len[avail_len>t_len].index.min() + 1
    
    # Draw scale
    d = canv
    for j in range(0,cols):
        for i in range(0,len(gs_codes)):
            x = (j * 30) + orig + (j * gs_widths[len(gs_widths)-1]) + gs_widths[i]
            if(i % 2 == 1):
                d.append(draw.Lines(x, orig,
                                    x, orig - 15,
                                    fill = 'none',
                                    stroke = 'black',
                                    stroke_width = 0.5))
                d.append(draw.Text(f'{gs_codes[i]}', 9,
                                   x, orig - 20))
            else:
               d.append(draw.Lines(x, orig,
                                   x, orig - 5,
                                   fill = 'none',
                                   stroke = 'black',
                                   stroke_width = 0.5))
               d.append(draw.Text(f'{gs_codes[i]}', 9,
                                  x, orig-10))
        
        x = (j * 30) + orig + (j * gs_widths[len(gs_widths)-1]) + gs_widths[len(gs_widths)-1]
        d.append(draw.Lines(x,orig,
                            x-gs_widths[len(gs_widths)-1],orig,
                            x-gs_widths[len(gs_widths)-1],colheight + orig,
                            fill = 'none',
                            stroke = 'black',
                            stroke_width = 0.5))
    # Draw log
    j = 0
    elevations = (elevations * 1000 * 2.8346456692913)/vscale
    for i in range(0,len(elevations)-1):
        if(elevations[i] > (j+1)*colheight):
            print('bugger')
            j += 1
        x1 = (j * 30) + orig + (j * gs_widths[len(gs_widths)-1])
        x2 = x1 + gs_widths[gs_codes[gs_codes == grain_base[i]].index[0]]
        if(grain_top[i] != 'NaN'):
            x3 = x1 + gs_widths[gs_codes[gs_codes == grain_top[i]].index[0]]
        else:
            x3 = x2
        y1 = elevations[i] - (j * colheight) + orig
        y2 = elevations[i+1] - (j * colheight) + orig
        
        if(y2 > (colheight+orig)):
            clip = draw.ClipPath()
            clip.append(draw.Lines(x1, y1,
                                   greater(x2,x3), y1,
                                   greater(x2,x3), y2 + ((colheight+orig) - y2),
                                   x1, y2 + ((colheight+orig) - y2)))
            d.append(draw.Lines(x1, y1,
                                x2, y1,
                                x3, y2,
                                x1, y2,
                                close = True,
                                fill = fcolors[fcodes[fcodes == facies[i]].index[0]],
                                stroke = 'black',
                                stroke_width = lnwgt,
                                clip_path = clip))
            
            x1b = ((j+1) * 30) + orig + ((j+1) * gs_widths[len(gs_widths)-1])
            x2b = x1b + gs_widths[gs_codes[gs_codes == grain_base[i]].index[0]]
            if(grain_top[i] != 'NaN'):
                x3b = x1b + gs_widths[gs_codes[gs_codes == grain_top[i]].index[0]]
            else:
                x3b = x2b
            y1b = elevations[i] - ((j+1) * colheight) + orig
            y2b = elevations[i+1] - ((j+1) * colheight) + orig
            
            clip = draw.ClipPath()
            clip.append(draw.Lines(x1b, orig,
                                   greater(x2b,x3b), orig,
                                   greater(x2b,x3b), y2b,
                                   x1b, y2b))
            d.append(draw.Lines(x1b, y1b,
                                x2b, y1b,
                                x3b, y2b,
                                x1b, y2b,
                                close = True,
                                fill = fcolors[fcodes[fcodes == facies[i]].index[0]],
                                stroke = 'black',
                                stroke_width = lnwgt,
                                clip_path = clip))
            
        else:
            d.append(draw.Lines(x1, y1,
                                x2, y1,
                                x3, y2,
                                x1, y2,
                                close = True,
                                fill = fcolors[fcodes[fcodes == facies[i]].index[0]],
                                stroke = 'black',
                                stroke_width = lnwgt))

        print(f'{j},{i},({x1:.3f},{y1:.3f}), ({x2:.3f},{y1:.3f}), ({x3:.3f},{y2:.3f}), ({x1:.3f},{y2:.3f}), {((colheight+orig) - y2):.3f}')
    
    if debug == True:
        print(f't_len: {t_len}',
              f'avail_len: {max(avail_len)}',
              f'cols: {cols}',
              f'gs_codes: {gs_codes}',
              f'gs_widths: {gs_widths}',
              f'colheight: {colheight}',
              sep = '\n')
    return d