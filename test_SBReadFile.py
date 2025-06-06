__copyright__  = "Copyright (c) 2022-2025, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."

from SBReadFile import *
from matplotlib import pyplot as plt
import numpy as np
import sys, getopt

def main(argv):
    theSBFileReader = SBReadFile()

    # change it to use your file
    #theSBFileReader.Open("/media/sf_E_DRI VE/Data/Slides/Format 7/SlideBook BCG test data/Slide1.sld")
    if len(sys.argv) < 3:
        print ('usage: python test_SBReadFile.py -i <inputfile>')
        sys.exit(2)

    theFileName = ''
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print ('usage: python test_SBReadFile.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('usage: python test_SBReadFile.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            theFileName = arg
    print ('Input file is ', theFileName)

    theRes = theSBFileReader.Open(theFileName)
    if not theRes:
        #print ('Cannot open the file: ', theFileName)
        sys.exit()

    theCapture = 0
    theChannel = 0
    theThumbnail = theSBFileReader.GetThumbnail(theCapture)
    
    theImageName = theSBFileReader.GetImageName(theCapture)
    print ("*** the image name: ",theImageName)

    theImageComments = theSBFileReader.GetImageComments(theCapture)
    print ("*** the image comments: ",theImageComments)

    theNumPositions = theSBFileReader.GetNumPositions(theCapture)
    print ("*** the image num positions: ",theNumPositions)

    theNumTimepoints = theSBFileReader.GetNumTimepoints(theCapture)
    print ("*** the image num timepoints: ",theNumTimepoints)

    theNumChannels = theSBFileReader.GetNumChannels(theCapture)
    print ("*** the image num channels: ",theNumChannels)

    theNumAnnotations = theSBFileReader.GetNumROIAnnotations(theCapture)
    print ("*** the image num ROI annotations: ",theNumAnnotations)
    for theAnnoIndex in range (0,theNumAnnotations):
        theShape,theVertexes = theSBFileReader.GetROIAnnotation(theCapture,theAnnoIndex)
        print ("theShape: ",theShape)
        for theVertex in theVertexes:
            print(" x: ",theVertex.mX," y: ",theVertex.mY)

    for theTimepoint in range(0,theNumTimepoints):
        theNumRegions = theSBFileReader.GetNumFRAPRegions(theCapture,theTimepoint)
        if(theNumRegions == 0):
            continue
        print ("*** the image num FRAP Regions ",theNumRegions, " for timepoint: ",theTimepoint)
        theShape,theVertexes = theSBFileReader.GetFRAPAnnotation(theCapture,theTimepoint)
        print ("the FRAPP Annotation shape : ",theShape)
        for theVertex in theVertexes:
            print(" x: ",theVertex.mX," y: ",theVertex.mY)
        for theRegionIndex in range (0,theNumRegions):
            theShape,theVertexes = theSBFileReader.GetFRAPRegion(theCapture,theTimepoint,theRegionIndex)
            print ("the Frap Region shape: ",theShape)
            for theVertex in theVertexes:
                print(" x: ",theVertex.mX," y: ",theVertex.mY)

    theX,theY,theZ = theSBFileReader.GetVoxelSize(theCapture)
    print ("*** the the voxel x,y,z size is: ",theX,theY,theZ)

    theY,theM,theD,theH,theMn,theS = theSBFileReader.GetCaptureDate(theCapture)
    print ("*** the the date yr/mn/day/hr/min/sec is: ",theY,theM,theD,theH,theMn,theS)

    theXmlDescriptor = theSBFileReader.GetAuxDataXMLDescriptor(theCapture,theChannel)
    print ("*** theXmlDescriptor is " ,theXmlDescriptor)

    theLen,theType = theSBFileReader.GetAuxDataNumElements(theCapture,theChannel)
    print ("*** theLen,theType ",theLen,theType)

    theXmlData =   theSBFileReader.GetAuxSerializedData(theCapture,theChannel,0)
    print ("*** theXmlData is " ,theXmlData)

    theNumRows = theSBFileReader.GetNumYRows(theCapture)
    theNumColumns = theSBFileReader.GetNumXColumns(theCapture)
    theNumPlanes = theSBFileReader.GetNumZPlanes(theCapture)
    theZplane = int(theNumPlanes/2)
    for theTimepoint in range(0,theNumTimepoints):
        image = theSBFileReader.ReadImagePlaneBuf(theCapture,0,theTimepoint,theZplane,0,True) #captureid,position,timepoint,zplane,channel,as 2d
        print ("*** The read buffer len is: " , len(image))

        #plot the slice

        plt.figure(theTimepoint+1)
        plt.imshow(image)

    plt.pause(100)
    data = input("Please hit Enter to exit:\n")
    print("Done")


if __name__ == "__main__":
    main(sys.argv[1:])
    


