from SBReadFile import *
from matplotlib import pyplot as plt
import numpy as np
import sys, getopt

def main(argv):
    theSBFileReader = SBReadFile()

    # change it to use your file
    #theSBFileReader.Open("/media/sf_E_DRI VE/Data/Slides/Format 7/SlideBook BCG test data/Slide1.sld")
    if len(sys.argv) < 3:
        print ('usage: python est.py -i <inputfile>')
        sys.exit(2)

    theFileName = ''
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print ('usage: python test.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('usage: python test.py -i <inputfile>')
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
    theImageName = theSBFileReader.GetImageName(theCapture)
    print ("*** the image name: ",theImageName)

    theImageComments = theSBFileReader.GetImageComments(theCapture)
    print ("*** the image comments: ",theImageComments)

    theNumPositions = theSBFileReader.GetNumPositions(theCapture)
    print ("*** the image num positions: ",theNumPositions)

    theNumChannels = theSBFileReader.GetNumChannels(theCapture)
    print ("*** the image num channels: ",theNumChannels)

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

    image = theSBFileReader.ReadImagePlaneBuf(theCapture,0,0,theZplane,0,True) #captureid,position,timepoint,zplane,channel,as 2d
    print ("*** The read buffer len is: " , len(image))

    #plot the slice

    plt.imshow(image)
    plt.pause(0.001)

    data = input("Please hit Enter to exit:\n")
    print("Done")


if __name__ == "__main__":
    main(sys.argv[1:])
    


