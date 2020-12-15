# -*- coding:utf-8 -*-

import numpy as np
import astropy.units as u
from astropy.io import fits
import astropy.coordinates
from astropy.coordinates import SkyCoord
from spectral_cube import SpectralCube

class FitsData:
    def __init__(self,file):
        self.cube = SpectralCube.read(file)

    def getcube(self):
        return self.cube

    def cutbycoord(self, xlo, xhi, ylo, yhi):
        self.c_min = SkyCoord(ra=xlo, dec=ylo, frame='icrs', unit=(u.hourangle, u.deg))
        self.c_max = SkyCoord(ra=xhi, dec=yhi, frame='icrs', unit=(u.hourangle, u.deg))

        self.dec_min = self.c_min.dec.degree*u.deg
        self.dec_max = self.c_max.dec.degree*u.deg
        self.ra_min = self.c_min.ra.degree*u.deg
        self.ra_max = self.c_max.ra.degree*u.deg

        self.cube = self.cube.subcube(xlo=self.ra_min, xhi=self.ra_max, ylo=self.dec_min, yhi=self.dec_max)
        #self.sub_cube = np.squeeze(self.sub_cube)

        return self.cube

    def getwcs(self):
        self.wcs = self.cube.moment(order=0).wcs

        return self.wcs
