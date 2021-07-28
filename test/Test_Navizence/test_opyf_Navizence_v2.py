#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %%
# %matplotlib qt5
import matplotlib.pyplot as plt
import sys
import os
os.chdir("./")
# if opyf is not installed where is the opyf folder?
sys.path.append('../../')
sys.path.append('./')
# On ipython try the magic command "%matplotlib qt5" for external outputs or "%matplotlib inline" for inline outputs
import opyf


plt.close('all')

opyf.mkdir2('./export_Tracks/')

# Path toward the video file
# filePath='./2018.07.04_Station_fixe_30m_sample.mp4'
filePath = 'test/Test_Navizence/2018.07.04_Station_fixe_30m_sample.mp4'
# set the object information
video = opyf.videoAnalyzer(filePath)

video.set_vecTime(Ntot=10, shift=1, step=2, starting_frame=20)
print(video.vec, '\n', video.prev)
"""
#Use .set_vecTime vector to define the processing plan 
#This method define video.vec and video.prev, two vecotrs required for the image processing:

# (by default {.set_vecttTime(starting_frame=0, step=1, shift=1, Ntot=1)} 
to process the first two image of the video or the frame sequence and extract the velocities between these two images and produce:
#video.vec    =   [   0 ,  1 ]
#video.prev   =   [False,True]
#video.prev=False indicates that no previous image has been processed
#For video.prev=False the step consists to read the corresponding image index 
#in video.vec and extract Good Feature To Track, for True the flow will measure 
#with the pair {False+True} from the good features detected in the first image
# 
# [Ntot] specifies the total number of image pairs
# [shift] specifies the shift between two pairs
# [starting_frame] specifies the first image
# [step] specifies the number of image between 2 images of each pair. 
# WARNING: if the step increases, the displacements necessarily increase
# Note that, if the object is build from a video with videoAnalyzer, a lag is expected since each 
    required images for the process are loaded in the memory for efficiency reasons
# 
# This function also defines video.Time, that is the time vector at which the velocity measurements are performed
# =============================================================================
"""

video.set_vlim([0, 30])
video.set_filtersParams(wayBackGoodFlag=4, RadiusF=20, maxDevInRadius=1, CLAHE=True)

video.set_goodFeaturesToTrackParams(maxCorners=50000, qualityLevel=0.001)

video.set_filtersParams(wayBackGoodFlag=4, RadiusF=20, maxDevInRadius=1, CLAHE=True)
video.extractGoodFeaturesDisplacementsAccumulateAndInterpolate(display1='quiver', display2='field', displayColor=True, scale=200, saveImgPath='./export_Tracks/')

opyf.hdf5_Read(video.filename+'.hdf5')

# View tracker points and their velocity
video.showXV(video.X, video.V, display='points', displayColor=True)

# or the averaged velocity field
Field = opyf.Render.setField(video.UxTot[0], video.UyTot[0], 'norm')
video.opyfDisp.plotField(Field, vis=video.vis)


'''
for plotting only the resulting averaged field, usefull if Ntot is longer
'''
# video.set_vlim([0, 30])
# video.set_vecTime(Ntot=10, shift=1, step=1, starting_frame=20)
# video.extractGoodFeaturesDisplacementsAccumulateAndInterpolate(display2='field', displayColor=True, scale=200)


# video.set_trackingFeatures(Ntot=10, step=1, starting_frame=1, track_length=5, detection_interval=10)

video.scaleData(framesPerSecond=25, metersPerPx=0.02, unit=['m', 's'], origin=[0, video.Hvis])
video.showXV(video.X, video.V, display='points', displayColor=True)


