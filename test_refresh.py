__copyright__  = "Copyright (c) 2022, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."

from SBReadFile import *
from matplotlib import pyplot as plt
import numpy as np
import sys, getopt
import time

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
        print ('usage: python test_refresh.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('usage: python test_refresh.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            theFileName = arg
    print ('Input file is ', theFileName)

    theRes = theSBFileReader.Open(theFileName,All=False)
    if not theRes:
        #print ('Cannot open the file: ', theFileName)
        sys.exit()

    #work on the first capture
    theCapture = 0
    #work on the first channel
    theChannel = 0

    
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
    #create a figure for animation
    fig = plt.figure(0)
    title = "Timepoint: {tp:6d}, Mean: {mn:.1f}"
    theFirstTP = 0
    theNoProgress = 0;
    theTimePaused = 0;
    theMaxWaitS = 5 # wait at most 5 seconds. If over this, quit
    theSleepS = 0.1 # sleep between refreshes
    thePlotFrequency = 10
    st = time.time()
    for theRetry in range(0,10000):
        for theTimepoint in range(theFirstTP,theNumTimepoints):
            image = theSBFileReader.ReadImagePlaneBuf(theCapture,0,theTimepoint,theZplane,0,True) #captureid,position,timepoint,zplane,channel,as 2d
            #print ("*** The read buffer len is: " , len(image))
            #calculate mean intensity using numpy
            theMean = np.mean(image)
            print ("*** theTimepoint: " , theTimepoint, "The mean: ",theMean)
            if theMean==0:
                #streaming has missed a timepoint
                #insert a break here
                print ("****** Mean is 0 ****** ")

            #plot the slice every n timepoints

            if theTimepoint%thePlotFrequency==0:
                if theTimepoint == 0:
                    img_artist = plt.imshow(image)
                else:
                    img_artist.set_data(image)
                plt.draw()
                fig.canvas.flush_events()
                plt.title(title.format(tp=theTimepoint,mn=theMean),loc='left')
                plt.pause(0.01)
                #time.sleep(0.1) # sleep 10 ms

        # see if there are any new timepoints
        theSBFileReader.Refresh(theCapture)
        if theFirstTP == theNumTimepoints:
            theNoProgress += 1
            time.sleep(theSleepS) # sleep 10 ms
            theTimePaused += theSleepS
        else:
            theNoProgress = 0
            time.sleep(theSleepS)

        # if we have waited too long, quit
        if theNoProgress * theSleepS  > theMaxWaitS:
            break

        #loop again
        theFirstTP = theNumTimepoints;
        theNumTimepoints = theSBFileReader.GetNumTimepoints(theCapture)-1

    et = time.time()
    elapsed_time = et - st - theTimePaused
    print('Execution time per loop iteration:', elapsed_time/theNumTimepoints, " s", ", waited for: ",theTimePaused," s")

    data = input("Please hit Enter to exit:\n")
    print("Done")


if __name__ == "__main__":
    main(sys.argv[1:])
    


