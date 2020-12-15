# -*- coding:utf-8 -*- 

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os 
import time

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import ticker
import astropy.coordinates
from astropy.coordinates import SkyCoord

import astropy.units as u
from spectral_cube import SpectralCube


def get_levels(min_lv, list):
    lvs = []
    for i in list:
        result = min_lv * i
        lvs.append(result)
    return lvs


def get_cube(f):
    cube = SpectralCube.read(f)
    return cube

def cutbycoord(cube, xlo, xhi, ylo, yhi):
    c_min = SkyCoord(ra=xlo, dec=ylo, frame='icrs', unit=(u.hourangle, u.deg))
    c_max = SkyCoord(ra=xhi, dec=yhi, frame='icrs', unit=(u.hourangle, u.deg))
    dec_min = c_min.dec.degree*u.deg
    dec_max = c_max.dec.degree*u.deg
    ra_min = c_min.ra.degree*u.deg
    ra_max = c_max.ra.degree*u.deg

    cube = cube.subcube(xlo=ra_min, xhi=ra_max, ylo=dec_min, yhi=dec_max)
    #sub_cube = np.squeeze(self.sub_cube)

    return cube

def get_wcs(cube):
    wcs = cube.moment(order=0).wcs
    return wcs

def index(request):
    d = np.array([[[2,3,2],[2,2,2]],[[4,3,2],[5,7,1]]])
    context = {
        'd':d,
        'answer' : time.time()
        }
    return render(request, 'graph/index.html', context)

def calc(request):
    FILE1 = os.path.join(os.getcwd(), 'graph/static/graph/c_1.fits')
    FILE2 = os.path.join(os.getcwd(), 'graph/static/graph/c_moment2.fits')

    #RA_MIN = '03h19m48.20s'
    #RA_MAX = '03h19m48.13s'
    #DEC_MIN = '41d30m42.5s'
    #DEC_MAX = '41d30m41.7s
    #MIN_LV = 0.005157
    #NSEQ = [-1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512]


    RA_MIN = request.POST['ra_min1']+'h'+request.POST['ra_min2']+'m'+request.POST['ra_min3']+'.'+request.POST['ra_min4']+'s'
    RA_MAX = request.POST['ra_max1']+'h'+request.POST['ra_max2']+'m'+request.POST['ra_max3']+'.'+request.POST['ra_max4']+'s'
    DEC_MIN = request.POST['dec_min1']+'d'+request.POST['dec_min2']+'m'+request.POST['dec_min3']+'.'+request.POST['dec_min4']+'s'
    DEC_MAX = request.POST['dec_max1']+'d'+request.POST['dec_max2']+'m'+request.POST['dec_max3']+'.'+request.POST['dec_max4']+'s'


    MIN_LV = float(request.POST['min_lv'])
    nseq = request.POST['nseq']
    nseq = nseq.split(',')
    NSEQ = [int(str) for str in nseq]

    cmap = request.POST['cmap']
    if cmap == "default":
        cmap = "rainbow"
    CMAP = cmap
    XLABEL = request.POST['xlabel']
    YLABEL = request.POST['ylabel']
    TITLE = cmap
    SIZE = 11


    cube1 = get_cube(FILE1)
    cube2 = get_cube(FILE2)

    cube1 = cutbycoord(cube1,xlo=RA_MIN, xhi=RA_MAX, ylo=DEC_MIN, yhi=DEC_MAX)
    cube2 = cutbycoord(cube2,xlo=RA_MIN, xhi=RA_MAX, ylo=DEC_MIN, yhi=DEC_MAX)

    wcs = get_wcs(cube1)

    cube1 = np.squeeze(cube1)
    cube2 = np.squeeze(cube2)

    lvs = get_levels(MIN_LV, NSEQ)

    fig = plt.figure(figsize=(SIZE, SIZE))
    ax = fig.add_subplot(111, title=TITLE,projection=wcs)
    im = ax.imshow(cube2, cmap=CMAP)
    plt.colorbar(im)
    ax.contour(cube1,cmap='gray', levels=lvs)
    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)

    lon = ax.coords['dec']
    lat = ax.coords['ra']
    lon.set_ticks(number=9)
    lat.set_ticks(number=8)

    SAVE_FILENAME = os.path.join(os.getcwd(), 'graph/static/graph/a.png')
    if os.path.exists(SAVE_FILENAME):
        os.remove(SAVE_FILENAME)
    plt.savefig(SAVE_FILENAME)
    

    context = {
        'answer': str(time.time())
    }
    return render(request,'graph/calc.html', context)


def del_file(request):
    FILENAME = os.path.join(os.getcwd(), 'graph/static/graph/a.png')
    if os.path.exists(FILENAME):
        os.remove(FILENAME)

    answer = ''

    context = {
        'answer': str(time.time()),
    }
    return render(request,'graph/del_file.html', context)

    
