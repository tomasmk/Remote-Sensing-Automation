# -----------------------------------------------------------

# --------- Assignment 4 - PCA analysis with Python  ------------------
# -----------------------------------------------------------
# Author: Tomas Milla-Koch
# Purpose: The following script is script for clipping a scene to vector boundary and performing a PCA analysis.
# Course: REMS 6023
# Date: 30/01/2022
# Disclaimer: This script is for educational purposes only.
# ----------------------------------------------------------

# -----------------------------------------------------------
# --------- Importing of required python libraries  ---------
# -----------------------------------------------------------
import os
import shutil
import fnmatch
# import exceptions module
from pci.exceptions import *
# import pci modules for project
from pci.clip import clip
from pci.pcimod import *
from pci.nspio import Report, enableDefaultReport
from pci.pca import pca
from pci.nspio import Report, enableDefaultReport
from pci.fexport import *
# initializing script time
from datetime import datetime as dt, time

# start time of script
start = dt.now()

# -----------------------------------------------------------
# --------- File Management  --------------------------------
# -----------------------------------------------------------
print('Obtaining necessary files.')
# get root directory
root = os.getcwd()

# list containing paths where files of different outputs will go
files = ['pca', 'reports']

# iterate through files to remove existing data and create new empty folders
for i in files:
    if os.path.exists(root + '\\' + i):
        shutil.rmtree(root + '\\' + i)
    os.mkdir(root + '\\' + i)  # make new folders

# initialize metadata file list
input_files = []

# populate list with availible MTL.txt files, in this case just one
for r, d, f in os.walk(os.getcwd()):
    for inFile in fnmatch.filter(f, '*_MTL.txt'):
        input_files.append(os.path.join(r, inFile))

# create a list of 1 for the vector file to be used as a boundary
vector_files = []
for r, d, f in os.walk(os.getcwd()):
    for inFile in fnmatch.filter(f, '*.shp'):
        vector_files.append(os.path.join(r, inFile))

print('Finished obtaining necessary files.')
# -----------------------------------------------------------
# --------- Clipping Image and Adding Bands to Image---------
# -----------------------------------------------------------
print('Clipping image.')

try:
    clip(fili=input_files[0]+'-MS',  # call MTL file from previously populated list of 1 element
         dbic=[1, 2, 3, 4, 5, 6, 7],  # which bands to clip
         sltype='vec',  # what kind of boundary file will image clip to
         # clip image to vector file provided ... any file name for other purposes is fine
         filo=root + '\\pca\\hal_clip.pix',
         clipfil=vector_files[0]
         )

    pcimod(file=root+'\\pca\\hal_clip.pix',
           pciop='ADD',  # add raster layers
           pcival=[0, 0, 3, 0]  # add 3 16bit unsigned layers to .pix file
           )

except Exception as e:
    print(e)

print('Finished clipping image.')
# -----------------------------------------------------------
# --------- PCA Image & Report Writing ----------------------
# -----------------------------------------------------------
print('Starting PCA analysis and report writing.')

try:
    # initialize report file and make sure none of it is already in memory
    Report.clear()
    enableDefaultReport(root+'\\reports\\PCA_report_1.txt')

    # pca analysis function
    pca(file=root + '\\pca\\hal_clip.pix',
        # which spectral bands to be analysed
        dbic=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        eign=[1, 2, 3],
        # what bands to occupy the newly created principal components
        # setting RGB color channels to 8,9,10 will give PC1,PC2,PC3 in focus
        dboc=[8, 9, 10],
        rtype='long')
finally:
    # close the report file
    enableDefaultReport('term')

print('Finished PCA analysis and report writing.')

# How long did the script take?
scp_time = dt.now() - start
print('The script took ' + str(scp_time) + ' to complete.')

# -----------------------------------------------------------
# --------- File Exporting ----------------------------------
# -----------------------------------------------------------

fexport(fili=root + '\\pca\\hal_clip.pix',
        filo=root + '\\pca\\MillaKoch_PCA.pix',
        dbic=[8, 9, 10])

print("File with PCs has been exported.")

# -----------------------------------------------------------
# --------- End of Script -----------------------------------
# -----------------------------------------------------------
