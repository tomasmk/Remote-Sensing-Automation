# -----------------------------------------------------------
# --------- Lab 2 - Mosaiking with Python  ------------------
# -----------------------------------------------------------
# Author: Tomas Milla-Koch
# Purpose: The following script is an automation script for
#         image mosaicking in PCI catalyst using Level 1
#         Landsat 8 imagery.
# Course: REMS 6023
# Date: 30/01/2022
# Disclaimer: This script is for educational purposes only.
# ----------------------------------------------------------

# -----------------------------------------------------------
# --------- Importing of required python libraries  ---------
# -----------------------------------------------------------

# import file management libraries
import os
import shutil
import fnmatch
# import exceptions module
from pci.exceptions import *
# import mosaicking module
from pci.automos import *
# import pci modules for atmospheric correction
from pci.atcor import atcor
from pci.hazerem import hazerem
from pci.masking import masking
# initializing script time
from datetime import datetime as dt
start = dt.now()

# -----------------------------------------------------------
# --------- File Management  --------------------------------
# -----------------------------------------------------------

# get root directory
root = os.getcwd()

# list containing paths where files of different outputs will go
files = ['mask', 'hazerem', 'atcor']

# iterate through files to remove existing data and create new empty folders
for i in files:
    if os.path.exists(root + '\\' + i):
        shutil.rmtree(root + '\\' + i)
    os.mkdir(root + '\\' + i)  # make new folders

# initialize metadata file list
input_files = []

# populate list with availible MTL.txt files
for r, d, f in os.walk(os.getcwd()):
    for inFile in fnmatch.filter(f, '*_MTL.txt'):
        input_files.append(os.path.join(r, inFile))


# -----------------------------------------------------------
# --------- Image Processing section --------------------------------
# -----------------------------------------------------------


# --------------------------------------------------------------
# -------------------Atmospheric Corrections-------------------
# ----------------------------------------------------------------
print("Masking, haze removal, and atmospheric corrections have started.")

# initialize counter variable
i = 1

# perform masking, haze removal, and atmospheric corrections iteratively
for image in input_files:

    try:  # Create cloud, water and haze masks
        masking(fili=image+'-MS',
                hazecov=[50], filo=root + '\\' + 'mask' + '\\' + 'mask'+str(i))  # .txt file names require a -MS for a multispectral image to be called

        # Remove the haze from both the multispectral and panchromatic bands
        hazerem(image+'-MS',  maskfili=root + '\\' + 'mask' + '\\' + 'mask'+str(i),
                hazecov=[50], filo=root + '\\' + 'hazerem' + '\\' + 'hazefree_ms'+str(i))

        # Calculate atmospheric correction for multispectral image.
        atcor(fili=root + '\\' + 'hazerem' + '\\' + 'hazefree_ms'+str(i), maskfili=root + '\\' + 'mask' + '\\' + 'mask' +
              str(i), atmcond="winter", outunits="Percent_Reflectance", filo=root + '\\' + 'atcor' + '\\' + 'atcor_ms'+str(i))  # atmospheric condition set to winter (when the imagery was taken)
    # iff an error occurs...print exception message
    except Exception as e:
        print(e)

    # add 1 to counter variable
    i += 1

print("Masking, haze removal, and atmospheric corrections have finished. Ready for mosaicking.")


# -----------------------------------------------------------
# --------- End of Script!  --------------------------------
# -----------------------------------------------------------
