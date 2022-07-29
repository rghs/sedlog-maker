# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 11:54:34 2021

@author: RGHS

Functions for sed log maker
"""

import pandas as pd
import numpy as np
import drawSvg as draw
import warnings

#%% Basic supporting functions

def greater(x,y):
    '''
    Returns greater of two numbers entered. Accepts floats and ints.

    '''
    if(x>y):
        return x
    else:
        return y

#%% Setup functions

def grainsize(sizes = None, width = None, wunit = 'mm'):
    '''
    Converts grainsize inputs to values accepted by drawLog. If left as default,
    will generate a standard lookup for siliciclastic grainsizes and graphical
    widths.

    Parameters
    ----------
    sizes : arraylike, optional
        Array containing custom codes for grain size. The default is None.
    width : arraylike, optional
        Array containing custom widths for grain sizes. The default is None.
    wunit : str, optional
        String specifying width unit provided in width variable. Must be either 'mm','in' or 'pt'. The default is 'mm'.

    Returns
    -------
    grain : pandas Series
        Series containing codes for grain sizes.
    widths : pandas Series
        Series containing widths for grain sizes in pt.

    '''
    # Errors for bad input
    if(wunit not in  ['mm','in','pt']):
        raise Exception('Width unit must be either "mm","in" or "pt".')
    if((sizes is None) and (width is not None)) or ((sizes is not None) and (width is None)):
        raise Exception('Both sizes and widths must be provided if custom categories are being used.')
    
    # Default lookup
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
        
    # Here be dragons if you only give 1 grainsize
    elif((hasattr(sizes, '__len__') is False) or (hasattr(width, '__len__') is False)):
        warnings.warn('Either length or sizes has no length attribute. This means that you have provided only one category in either. This is likely to produce very strange behaviour and should be reconsidered.')
    
    # Unit conversion for custom grainsize arrays
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
    '''
    Converts provided facies and colors to values accepted by drawLog.

    Parameters
    ----------
    codes : array-like, optional
        Contains facies codes you want to use as strings. The default is None.
    colors : array-like, optional
        Contains hex. The default is None.
        
    Leaving both parameters as the default value of None will return the built
    in array of facies and colors.
        
    Returns
    -------
    fcodes : np.ndarray
        Array containing codes used for facies.
    fcolors : np.ndarray
        Array containing hex codes for facies colors.

    '''
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
                            "#5A4854","#74576A","#8C627E","#A57093","#D998C1",
                            "#666154","#807969","#99917D","#B3A993","#CCC1A7",
                            "#E3AB4A","#DBB75C","#FDBB45","#FBB672","#FFCE6F","#EE9621","#F68C35",
                            "#99834F","#E5C376",
                            "#661714","#8D211D","#B22C26","#D93328","#EF4130"))
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
    '''
    Converts unit thicknesses into absolute elevations from base of log.

    Parameters
    ----------
    thicknesses : array-like
        Array containing thicknesses of units in log.

    Returns
    -------
    elevation : pd.Series
        Pandas Series containing elevation values for each unit.

    '''
    if(hasattr(thicknesses, '__len__') is False):
        ex = '\n'.join(('Thicknesses data has no length attribute, meaning only one thickness reading was provided.',
              f'Provided thicknesses: {thicknesses}'))
        warnings.warn(ex)
    if(isinstance(thicknesses, np.ndarray) is False):
        thicknesses = np.array(thicknesses)
    
    elevation = np.zeros(len(thicknesses)+1)
    x = 0.0
    for i in range(0,len(thicknesses)):
        x += thicknesses[i]
        elevation[i+1] = x
    
    elevation = pd.Series(elevation)
    return elevation

def canvas(width = None, height = None, standard = 'letter'):
    '''
    Creates a canvas for the drawing, with options for several standard paper
    sizes in both American and European flavours.
    
    Function will prioritise values manually entered over the standard string,
    unless both are left as default, in which case a standard size will be
    selected.

    Parameters
    ----------
    width : float, optional
        Width of canvas in mm. The default is None.
    height : float, optional
        Height of canvas in mm. The default is None.
    standard : string, optional
        String specifying standard paper size. The default is 'letter'.
        Available options are as follows:
            - letter
            - legal
            - tabloid
            - a3
            - a4
            - a5

    Returns
    -------
    canvas : drawSvg object
        drawSvg canvas for log to be drawn onto.

    '''
    sheets = pd.Series(['letter', 'legal', 'tabloid',
                       'a3', 'a4', 'a5'])
    if((width is None) and (height is None) and (standard in sheets.values)):
        stdw = np.array([215.9, 215.9, 279.4,
                         297, 210, 148])
        stdh = np.array([279.4, 355.6, 431.8,
                         420, 297, 210])
        cw = stdw[sheets[sheets == standard].index[0]]
        ch = stdh[sheets[sheets == standard].index[0]]
    elif(isinstance(width,(float,int)) and isinstance(height,(float,int))):
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

#%% Drawing functions

def drawKey(fcodes, fcolors,
            box_size = 40, custom_rows = None,
            padding = 5):
    if custom_rows == 'default':
        custom_rows = [2,5,5,7,2,5]
    if custom_rows is None:
        cw = box_size * 2 + padding * 2
        ch = box_size * len(fcodes) + padding * (len(fcodes)+1)
    else:
        # Check that custom rows matches length of fcodes
        if(len(fcodes) != sum(custom_rows)):
            raise Exception(f'Custom rows must sum to length of fcodes. len(fcodes) = {len(fcodes)}, sum(custom_rows) = {sum(custom_rows)}')
        cw = max(custom_rows) * box_size + max(custom_rows) * padding + box_size*2
        ch = len(custom_rows) * box_size + (len(custom_rows)+1) * padding
        
    d = draw.Drawing(cw, ch, origin = (0,0), displayInline = False)
    
    if custom_rows is None:
        for i in range(0,len(fcodes)):
            d.append(draw.Rectangle(padding, ch-padding*(i+1)-box_size*(i+1),
                                    box_size, box_size,
                                    fill=fcolors[fcodes[fcodes == fcodes[i]].index[0]],
                                    stroke_width = 1, stroke='black'))
            d.append(draw.Text(fcodes[i], 10,
                               x = 2*padding + box_size,
                               y = ch-padding*(i+1)-box_size*(i+1) + box_size/2))
    else:
        box = 0
        for j in range(0,len(custom_rows)):
            for i in range(0,custom_rows[j]):
                d.append(draw.Rectangle(padding*(i+1) + box_size*(i),
                                        ch-padding*(j+1)-box_size*(j+1),
                                        box_size, box_size,
                                        fill=fcolors[fcodes[fcodes == fcodes[box]].index[0]],
                                        stroke_width = 1, stroke='black'))
                box += 1
            row_label = ', '.join(fcodes[sum(custom_rows[0:j]):sum(custom_rows[0:j])+custom_rows[j]])
            d.append(draw.Text(row_label, 10,
                               x = padding*(i+1) + box_size*(i+1) + padding,
                               y = ch-padding*(j+1)-box_size*(j+1) + box_size/2))
    return d
    

def drawLog(elevations, vscale,
            grain_base, grain_top, facies,
            gs_codes, gs_widths, fcodes, fcolors, canv,
            orig = 40, pad = 5, colspc = 40, lnwgt = 0.5,
            man_colheight = None, columns = None, ticks = 20,
            labels = None, label_strat = 'polite',
            nachar = 'NaN', debug = False):
    '''
    

    Parameters
    ----------
    elevations : pd.Series
        Elevations of the base and top of each unit. Can be created from thickness
        data using the elevs() function.
    vscale : int
        Scale at which to draw log in form X:1.
    grain_base : pd.Series
        Series containing the grain size at the base of the units.
    grain_top : pd.Series
        Series containing the grain size at the top of the units. Can contain blank
        cells for units with constant grain sizes.
    facies : pd.Series
        Series containing the facies code for each unit.
    gs_codes : pd.Series
        Series containing the grain size codes used in the log.
        Can be created with the grainsize() function.
    gs_widths : pd.Series
        Series containing widths to draw each grain size in the log.
        Can be created with the grainsize() function.
    fcodes : pd.Series
        Series containing facies codes used in the log.
        Can be created with the faciesList() function.
    fcolors : pd.Series
        Series containing colors corresponding to the facies codes provided.
        Can be created with the faciesList() function.
    canv : drawSvg object
        drawSvg.Drawing created with drawSvg.
        Can be created with the canvas() function.
    orig : int, optional
        Coordinates (in pt) to start drawing from in form (x,x). The default is 40.
    pad : int, optional
        Padding (in pt) used around the edge of the page. The default is 5.
    colspc : int, optional
        Spacing (in pt) between the columns. The default is 40.
    lnwgt : float, optional
        Weight of lines (in pt) to draw around the log boxes. The default is 0.5.
    man_colheight : float, optional
        Manually set the height (in m) of each column drawn. The default is None.
        If set to default, columns will be drawn to the full height of the canvas.
    columns : int, optional
        How many columns to draw. The default is None.
        If left as default, the minimum number of columns necessary to accommodate
        the log at the given vscale will be drawn.
    ticks : float, optional
        How often (in m) to draw ticks on the vertical axis of the log. The default is 20.
    labels : str or pd.Series, optional
        What to label the units with. Accepts any of the following:
            - An array the same length as the number of units, with blank cells where units should not be labelled
            - 'facies': labels each unit with the facies code
            - 'number': labels each unit with its number, starting from 1 at the base
        The default is None.
    label_strat : str, optional
        Chooses whether to skip drawing labels that would write over
        units in the log ('polite') or whether to just label everything,
        consequences be damned. The default is 'polite'.
    nachar : str, optional
        String specifying what blank cells contain. The default is 'NaN'.
    debug : bool, optional
        Provides addtional information during log construction. The default is False.

    Returns
    -------
    d : drawSvg object
        Completed log, ready for exporting.

    '''
    # Check labels are something that makes sense
    laberr = 'labels accepts either an array-like, "numbers" or "facies". None of these were detected so no labels are being printed.'
    if isinstance(labels, (str, type(None))) is False:
        if(hasattr(labels, '__len__')):
            if(len(labels) != len(facies)):
                warnings.warn('labels must be of same length as facies. Setting labels to None.')
            else:
                if(isinstance(labels, np.ndarray) is False):
                    labels = np.asarray(labels)
        else:
            warnings.warn(laberr)
            labels = None
    elif(isinstance(labels, str)) and (labels not in ['facies', 'numbers']):
        warnings.warn(laberr)
        labels = None
    # else:
    #     warnings.warn(laberr)
    #     labels = None
    
    # Figure out page spacing
    if man_colheight is None:
        colheight = canv.height-(orig + pad)
    elif(isinstance(man_colheight, (int, float))):
        colheight = (man_colheight * 1000 * 2.8346456692913)/vscale
        if(colheight > canv.height-(orig + pad)):
            err = '\n'.join(('Column height exceeds page height. Produced log will hang off page.',
                             f'Current page height (pt) = {canv.height-(orig + pad)}',
                             f'Current column height (pt) = {(man_colheight * 1000 * 2.8346456692913)/vscale}',
                             f'Current excess height (pt) = {((man_colheight * 1000 * 2.8346456692913)/vscale) - (canv.height-(orig + pad))}'))
            warnings.warn(err)
    else:
        raise Exception('Manual column height must be provided as "int" or "float" dtype.')
    
    t_len = (elevations[len(elevations)-1] * 1000 * 2.8346456692913)/vscale #vscale * 2.8346456692913 * elevations[len(elevations)-1]
    if(columns is None):
        # Calculate the minimum number of columns needed to fit log if no value is passed
        columns = int(np.ceil(t_len/colheight))
    avail_len = pd.Series(np.array(list(range(1,columns + 1))) * colheight)
    if(pd.isna(avail_len[avail_len>t_len].index.min()) is True):
        error = '\n'.join((f'Not sufficient vertical space with {columns} columns and vertical scale of {vscale}:1.',
                        'Choose a smaller vscale or increase max columns.',
                        f'Available length (pt) = {max(avail_len)}',
                        f'Total length of log (pt) = {t_len}',
                        f'Individual column height (pt) = {colheight}',
                        f'Excess height (pt) = {t_len - max(avail_len)}',
                        f'Minimum columns needed = {int(np.ceil(t_len/colheight))}'))
        raise Exception(error)
    else:
        # Reduce provided number of columns to minimum needed
        cols = avail_len[avail_len>t_len].index.min() + 1
    
    d = canv
    
    # Draw log
    j = 0
    elevations = (elevations * 1000 * 2.8346456692913)/vscale
    for i in range(0,len(elevations)-1):
        if(elevations[i] > (j+1)*colheight):
            if debug is True: print('Split unit.')
            j += 1
        x1 = (j * colspc) + orig + (j * gs_widths[len(gs_widths)-1])
        x2 = x1 + gs_widths[gs_codes[gs_codes == grain_base[i]].index[0]]
        if(grain_top[i] != 'NaN'):
            x3 = x1 + gs_widths[gs_codes[gs_codes == grain_top[i]].index[0]]
        else:
            x3 = x2
        y1 = elevations[i] - (j * colheight) + orig
        y2 = elevations[i+1] - (j * colheight) + orig
        
        # Draw boxes split across 2 columns
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
            
            x1b = ((j+1) * colspc) + orig + ((j+1) * gs_widths[len(gs_widths)-1])
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
            # Draw labels on whichever section of split boxes is biggest
            if labels is not None:
                if(((y2 + ((colheight+orig) - y2)) - y1) > y2b-orig):
                    lx = greater(x2, x3) + 5
                    ly = (y1 + (y2 + ((colheight+orig) - y2)))/2
                    ldelta = (y2 + ((colheight+orig) - y2)) - y1
                else:
                    lx = greater(x2b, x3b) + 5
                    ly = (y2b+(orig))/2
                    ldelta = y2b - orig
            # Draw labels on boxes that are big enough
                if((label_strat == 'polite') and (ldelta >= 9)):
                    p = draw.Line(lx, ly,
                                  lx+100, ly,
                                  stroke_width = 0, fill = 'none')
                    if(isinstance(labels, str) and (labels == 'facies')):
                        d.append(draw.Text(f'{facies[i]}', 9,
                                           path = p, valign='middle', text_anchor = 'start'))
                    elif(isinstance(labels, str) and (labels == 'numbers')):
                        d.append(draw.Text(f'{i}', 9,
                                           path = p, valign='middle', text_anchor = 'start'))
                    elif(labels[i] is not nachar):
                        d.append(draw.Text(f'{labels[i]}', 9,
                                       path = p, valign='middle', text_anchor = 'start'))
            # Just label everything
                else:
                    p = draw.Line(lx, ly,
                                  lx+100, ly,
                                  stroke_width = 0, fill = 'none')
                    if(isinstance(labels, str) and (labels == 'facies')):
                        d.append(draw.Text(f'{facies[i]}', 9,
                                           path = p, valign='middle', text_anchor = 'start'))
                    elif(isinstance(labels, str) and (labels == 'numbers')):
                        d.append(draw.Text(f'{i}', 9,
                                           path = p, valign='middle', text_anchor = 'start'))
                    elif(labels[i] is not nachar):
                        d.append(draw.Text(f'{labels[i]}', 9,
                                           path = p, valign='middle', text_anchor = 'start'))
            
        # Draw boxes that aren't split
        else:
            d.append(draw.Lines(x1, y1,
                                x2, y1,
                                x3, y2,
                                x1, y2,
                                close = True,
                                fill = fcolors[fcodes[fcodes == facies[i]].index[0]],
                                stroke = 'black',
                                stroke_width = lnwgt))
            
            # Label units
            if labels is not None:
            # Make labels appear only on units that are thick enough
                if((label_strat == 'polite') and ((y2 - y1) >= 9)):
                    if debug is True:
                        print(f'Politely labelling unit {i}...')
                    p = draw.Line(greater(x2,x3)+5, (y2+y1)/2,
                                  greater(x2,x3)+100, (y2+y1)/2,
                                  stroke_width = 0, fill = 'none')
                    if(isinstance(labels, str) and (labels == 'facies')):
                        d.append(draw.Text(f'{facies[i]}', 9,
                                           path = p, valign='middle', text_anchor = 'start'))
                    elif(isinstance(labels, str) and (labels == 'numbers')):
                        d.append(draw.Text(f'{i}', 9,
                                           path = p, valign='middle', text_anchor = 'start'))
                    elif(labels[i] is not nachar):
                        d.append(draw.Text(f'{labels[i]}', 9,
                                           path = p, valign='middle', text_anchor = 'start'))
                # Just label everything
                else:
                    p = draw.Line(greater(x2,x3)+5, (y2+y1)/2,
                                  greater(x2,x3)+100, (y2+y1)/2,
                                  stroke_width = 0, fill = 'none')
                    if(isinstance(labels, str) and (labels == 'facies')):
                        d.append(draw.Text(f'{facies[i]}', 9,
                                           path = p, valign='middle', text_anchor = 'start'))
                    elif(isinstance(labels, str) and (labels == 'numbers')):
                        d.append(draw.Text(f'{i}', 9,
                                           path = p, valign='middle', text_anchor = 'start'))
                    elif(labels[i] is not nachar):
                        d.append(draw.Text(f'{labels[i]}', 9,
                                           path = p, valign='middle', text_anchor = 'start'))
            
        if debug is True:
            print(f'{j},{i},({x1:.3f},{y1:.3f}), ({x2:.3f},{y1:.3f}), ({x3:.3f},{y2:.3f}), ({x1:.3f},{y2:.3f}), {((colheight+orig) - y2):.3f}')
        
    # Draw scale
    nticks = int(np.floor((cols * colheight)/((ticks * 1000 * 2.8346456692913)/vscale) + 1))
    t_heights = np.array(range(0,nticks)) * ((ticks * 1000 * 2.8346456692913)/vscale)
    
    j = 0
    x = orig
    for i in range(0,nticks):
        if(t_heights[i] >= (j+1)*colheight):
            j += 1
            x = (j * colspc) + orig + (j * gs_widths[len(gs_widths)-1])
        d.append(draw.Lines(x, orig + t_heights[i] - (j*colheight),
                            x - 5, orig + t_heights[i] - (j*colheight),
                            fill = 'none',
                            stroke = 'black',
                            stroke_width = 0.5))
        d.append(draw.Text(f'{i * ticks}', 9,
                           x - 6, orig + t_heights[i] - (j*colheight),
                           text_anchor = 'end'))
    
    # Write grain size bars and label with codes at bottom of scale
    for j in range(0,cols):
        for i in range(0,len(gs_codes)):
            x = (j * colspc) + orig + (j * gs_widths[len(gs_widths)-1]) + gs_widths[i]
            if(i % 2 == 1):
                d.append(draw.Lines(x, orig,
                                    x, orig - 15,
                                    fill = 'none',
                                    stroke = 'black',
                                    stroke_width = 0.5))
                # Create vertical path to run text on
                p = draw.Line(x+0.5, orig-16.5, x+1, orig-100,
                               stroke_width = 0, fill='none')
                d.append(draw.Text(f'{gs_codes[i]}', 9,
                                   path=p,
                                   text_anchor = 'start',
                                   valign = 'middle'))
            else:
               d.append(draw.Lines(x, orig,
                                   x, orig - 5,
                                   fill = 'none',
                                   stroke = 'black',
                                   stroke_width = 0.5))
               p = draw.Line(x+0.5, orig-6.5, x+1, orig-100,
                               stroke_width = 0, fill='none')
               d.append(draw.Text(f'{gs_codes[i]}', 9,
                                  path=p,
                                  text_anchor = 'start',
                                  valign = 'middle'))
        
        x = (j * colspc) + orig + (j * gs_widths[len(gs_widths)-1]) + gs_widths[len(gs_widths)-1]
        d.append(draw.Lines(x,orig,
                            x-gs_widths[len(gs_widths)-1],orig,
                            x-gs_widths[len(gs_widths)-1],colheight + orig,
                            fill = 'none',
                            stroke = 'black',
                            stroke_width = 0.5))
    
    if debug is True:
        print(f't_len: {t_len}',
              f'avail_len: {max(avail_len)}',
              f'cols: {cols}',
              f'gs_codes: {gs_codes}',
              f'gs_widths: {gs_widths}',
              f'colheight: {colheight}',
              sep = '\n')
    return d