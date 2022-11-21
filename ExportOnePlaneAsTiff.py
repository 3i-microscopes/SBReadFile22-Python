__copyright__  = "Copyright (c) 2022, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."

"""Read and write TIFF files.
Exports one plane for each timepoint and channel as a tiff file

There are two basic ways to use it:
python ExportOnePlaneAsTiff.py -i input_file.sldy -l
    This execution will list all the captures in the file

python ExportOnePlaneAsTiff.py -i input_file.sldy -o output_tiff_file_without_suffix -n capture_number -p plane_number
example:
python ExportOnePlaneAsTiff.py -i c:\Datat|Slides\Slide1 -o c:\Data\Tiffs\Slide1 -n 1 -p 20
    This exports plane 21 (0 is the first plane) for capture 1 (0 is the first capture) 
    tiff files will be created for each channel and timepoint

tifffile package
-----------------
Add it like so:
from Start menu, open Anaconda3(64-bit)/Anaconda Prompt (miniconda 3), then type:
conda activate Slidebook
conda install -n SlideBook python=3.8.5 tifffile
"""

from SBReadFile import *
from matplotlib import pyplot as plt
import numpy as np
import sys, getopt
import tifffile as tiff

def usage():
    print ('usage: python ExportOnePlaneAsTiff.py -i <sldy input_file> -l')
    print ('       lists all the captures in the slides')
    print ('')
    print ('usage: python ExportOnePlaneAsTiff.py -i <sldy input_file> -o <output_tiff_file_prefix> -n capture_number -p plane_number')
    print ('       extract the plane specified with -p from the capture number specified with -n. Plane and capture number are base 0')


def list(inSBFileReader,inCapture):
    theChannel = 0
    print(" ")
    print("***********************************************")
    print(" ")
    print ("*** properties for capture number: ",inCapture)
    theImageName = inSBFileReader.GetImageName(inCapture)
    print ("*** the image name: ",theImageName)

    theImageComments = inSBFileReader.GetImageComments(inCapture)
    print ("*** the image comments: ",theImageComments)

    theNumRows = inSBFileReader.GetNumYRows(inCapture)
    print ("*** the image number of rows: ",theNumRows)

    theNumColumns = inSBFileReader.GetNumXColumns(inCapture)
    print ("*** the image number of columns: ",theNumColumns)

    theNumPlanes = inSBFileReader.GetNumZPlanes(inCapture)
    print ("*** the image number of planes: ",theNumPlanes)

    theNumChannels = inSBFileReader.GetNumChannels(inCapture)
    print ("*** the image num channels: ",theNumChannels)

    theNumTimepoints = inSBFileReader.GetNumTimepoints(inCapture)
    print ("*** the image num timepoints: ",theNumTimepoints)

    theNumPositions = inSBFileReader.GetNumPositions(inCapture)
    print ("*** the image num positions: ",theNumPositions)

    theX,theY,theZ = inSBFileReader.GetVoxelSize(inCapture)
    print ("*** the voxel x,y,z sizes in um are: ",theX,theY,theZ)

    theY,theM,theD,theH,theMn,theS = inSBFileReader.GetCaptureDate(inCapture)
    print ("*** the capture date yr/mn/day/hr/min/sec is: ",theY,theM,theD,theH,theMn,theS)

    theXmlDescriptor = inSBFileReader.GetAuxDataXMLDescriptor(inCapture,theChannel)
    print ("*** theXmlDescriptor is " ,theXmlDescriptor)

    #theLen,theType = inSBFileReader.GetAuxDataNumElements(inCapture,theChannel)
    #print ("*** theLen,theType ",theLen,theType)

    theXmlData =   inSBFileReader.GetAuxSerializedData(inCapture,theChannel,0)
    #print ("*** theXmlData is " ,theXmlData)

def main(argv):
    theSBFileReader = SBReadFile()

    # change it to use your file
    #theSBFileReader.Open("/media/sf_E_DRI VE/Data/Slides/Format 7/SlideBook BCG test data/Slide1.sld")
    if len(sys.argv) < 3:
        usage()
        sys.exit(2)

    theFileName = ''
    theListMode = False
    thePlane = -1;
    theCapture = -1;
    try:
        opts, args = getopt.getopt(argv,'hln:p:i:o:',['ifile=','list','plane','ofile='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-l':
            theListMode = True
        elif opt == '-n':
            theCapture = int(arg)
        elif opt == '-p':
            thePlane = int(arg)
        elif opt in ("-i", "--ifile"):
            theFileName = arg
        elif opt in ("-o", "--ofile"):
            theTiffFileName = arg
    print ('Input file is ', theFileName)
    #print ('Output file is ', theTiffFileName)

    theRes = theSBFileReader.Open(theFileName)
    if not theRes:
        #print ('Cannot open the file: ', theFileName)
        sys.exit()

    theChannel = 0
    theNumCaptures = theSBFileReader.GetNumCaptures();
    if theListMode == True:
        for theCapture in range(theNumCaptures):
            list(theSBFileReader,theCapture)
        sys.exit()

    if theCapture == -1:
        print ("Capture number must be specified as: -n capture_number");
        sys.exit()

    if thePlane == -1:
        print ("Plane number must be specified as: -p plane_number");
        sys.exit()

    theNumRows = theSBFileReader.GetNumYRows(theCapture)
    theNumColumns = theSBFileReader.GetNumXColumns(theCapture)
    theNumPlanes = theSBFileReader.GetNumZPlanes(theCapture)
    theNumChannels = theSBFileReader.GetNumChannels(theCapture)
    theNumTimepoints = theSBFileReader.GetNumTimepoints(theCapture)

    for theTimepoint in range(theNumTimepoints):
        for theChannel in range(theNumChannels):

            image = theSBFileReader.ReadImagePlaneBuf(theCapture,0,theTimepoint,thePlane,theChannel,True) #captureid,position,timepoint,zplane,channel,as 2d
            print ("*** The read buffer len is: " , len(image))

            theOutFile = "{0}C{1:d}Z{2:04d}T{3:04d}.tiff".format(theTiffFileName,theChannel,thePlane,theTimepoint)
            print('The output file is: ',theOutFile)

            tif = tiff.TiffWriter(theOutFile)
            tif.write(image)
            tif.close()

    data = input("Please hit Enter to exit:\n")
    print("Done")


if __name__ == "__main__":
    main(sys.argv[1:])
    


