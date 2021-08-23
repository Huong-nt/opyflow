#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %matplotlib qt5
import matplotlib.pyplot as plt
import sys
import os
import cv2
import numpy as np

from utils import parsePIVlabTextFile
os.chdir("./")
# if opyf is not installed where is the opyf folder?
sys.path.append('../../')
sys.path.append('./')
# On ipython try the magic command "%matplotlib qt5" for external outputs or "%matplotlib inline" for inline outputs
import opyf
from opyf import MeshesAndTime, Render, Interpolate

def interpolate(X, V, image, img_h, img_w, **args):
    interp_params = dict(Radius=30, Sharpness=8, kernel='Gaussian')
    grid_y, grid_x, gridVx, gridVy, Hgrid, Lgrid = MeshesAndTime.set_gridToInterpolateOn(pixLeft=0, pixRight=img_w, stepHor=2, pixUp=0, pixDown=img_h, stepVert=2)
    XT = Interpolate.npGrid2TargetPoint2D(grid_x, grid_y)
    interpolatedVelocities, Ux, Uy = interpolateOnGrid(X, V, XT, interp_params, Lgrid, Hgrid)
    Field = Render.setField(Ux, Uy, Type='norm')
    Field[np.where(Field == 0)] = np.nan

    # Plot field
    vecX = grid_x[0, :]
    vecY = grid_y[:, 0]
    # self.opyfDisp.paramPlot['vecX'] = self.vecX
    # self.opyfDisp.paramPlot['vecY'] = self.vecY
    paramPlot = {
        'ScaleVectors': 0.1,
        'vecX': vecX, 'vecY': vecY,
        'extentFrame': [0, img_w, img_h, 0],
        'unit': ['px', 'deltaT'],
        'Hfig': 8,
        'grid': True,
        'vlim': [0, 15]
    }
    opyfDisp = Render.opyfDisplayer(**paramPlot, num='opyfPlot')
    opyfDisp.plotField(Field, vis=image, **args)
    opyfDisp.fig.savefig(os.path.join(CURR_DIR, 'export_Tracks', 'average_piv.png'))


def interpolateOnGrid(X, V, XT, interp_params, Lgrid, Hgrid):
    print('[I] ' + str(len(X)) + ' vectors to interpolate')
    interpolatedVelocities = Interpolate.npInterpolateVTK2D(X, V, XT, ParametreInterpolatorVTK=interp_params)

    Ux = Interpolate.npTargetPoints2Grid2D(interpolatedVelocities[:, 0], Lgrid, Hgrid) 
    Uy = Interpolate.npTargetPoints2Grid2D(interpolatedVelocities[:, 1], Lgrid, Hgrid)

    return interpolatedVelocities, Ux, Uy


plt.close('all')

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
imgInput = cv2.imread(os.path.join(CURR_DIR, 'sample.png'))
img_h, img_w, _ = imgInput.shape

vec_x, vec_y, vec_u, vec_v, _ = parsePIVlabTextFile(os.path.join(CURR_DIR, 'PIVlab_0100.txt'))


X, V = [], []
for x, y, u, v in zip(vec_x, vec_y, vec_u, vec_v):
    X.append([x, y])
    V.append([u, v])
X = np.array(X)
V = np.array(V)

interpolate(X, V, imgInput, img_h, img_w, displayColor=True, scale=200,  num='opyfPlot')

