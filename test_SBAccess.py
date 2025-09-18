__copyright__  = "Copyright (c) 2022-2025, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."
"""A test file to test many features of the SBAccess library
"""

import socket
import numpy as np
import time
import random
from matplotlib import pyplot as plt
from SBAccess import *
#from io import StringIO

#HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
#HOST = '192.168.56.101'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def int32_to_bytes(inVal):
    theArray = np.array([inVal],np.int32)
    theBytes = theArray.tobytes()
    return theBytes

def float32_to_bytes(inVal):
    theArray = np.array([inVal],np.float32)
    theBytes = theArray.tobytes()
    return theBytes

def float64_to_bytes(inVal):
    theArray = np.array([inVal],np.float64)
    theBytes = theArray.tobytes()
    return theBytes

def string_to_bytes(inString):
    theBytes = str.encode(inString)
    return theBytes


def socket_server():
    HOST = ''  # Standard loopback interface address (localhost)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(4)

                if not data:
                    break
                theTokenArr = np.frombuffer(data,np.int32)
                theToken = theTokenArr[0]

                print ('token is: ',theToken)
                if theToken == 1:
                    data = conn.recv(8)
                    theDoubleArr = np.frombuffer(data,np.float64)
                    theDouble = theDoubleArr[0]
                    print ('theDouble is: ',theDouble)
                    theDoubleBuf = theDoubleArr.tobytes()
                    l = len(theDoubleBuf)
                    print ('length of buffer is: ',l)
                    conn.send(theDoubleBuf)
    return

def socket_client_test_send():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theToken = 1
        theBytes = int32_to_bytes(theToken)
        l = len(theBytes)
        print ('length of buffer is: ',l)

        s.send(theBytes)
        theBytes = float32_to_bytes(3.15)
        l = len(theBytes)
        print ('length of buffer is: ',l)
        s.send(theBytes)

        theBytes = float64_to_bytes(3.151562)
        l = len(theBytes)
        print ('length of buffer is: ',l)
        s.send(theBytes)

        the_str = "hello world"
        l = len(the_str)
        theBytes = int32_to_bytes(l)
        print ('length of string is: ',l)
        s.send(theBytes)
        theBytes = string_to_bytes(the_str)
        s.send(theBytes)



        data = s.recv(4)

def socket_client_test_array():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    numBytes = 2048*2048
    theArray = np.zeros(numBytes,dtype='uint16')
    theArrLen = len(theArray)
    theArrayBytes = theArray.tobytes()
    theLengthBytes = int32_to_bytes(len(theArrayBytes))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        for iter in range(1000000):
            s.send(theLengthBytes)
            data = s.recv(4)
            s.send(theArrayBytes)
            data = s.recv(4)
            #print ('iter: ',iter)


        print ('iter: ',iter)
        theBytes = int32_to_bytes(0)
        s.send(theBytes)

def test_add_new_channel():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theSbAccess.Open("E:\Data\Slides_msi\QweekTour.sldy");

        theNumCaptures = theSbAccess.GetNumCaptures()

        theCapture = 0;
        theNumRows = theSbAccess.GetNumYRows(theCapture)
        theNumColumns = theSbAccess.GetNumXColumns(theCapture)
        theNumPlanes = theSbAccess.GetNumZPlanes(theCapture)
        theNumChannels = theSbAccess.GetNumChannels(theCapture)
        theNewChannel = theNumChannels;


        for theZPlane in range(theNumPlanes):
            image = theSbAccess.ReadImagePlaneBuf(theCapture,0,0,theZPlane,0) #captureid,position,timepoint,zplane,channel
            # np.insert(the3DVolume,theNumRows*theNumColumns,image)
            print ("*** theZPlane: ",theZPlane," The read buffer len is: " , len(image))
            theSbAccess.WriteImagePlaneBuf(theCapture,0,theZPlane,theNewChannel,image)


        data = input("Please hit Enter to exit:\n")
        print("Done")


        return

def test_copy_capture():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theSbAccess.Open("E:\Data\Slides_msi\QweekTour.sldy");

        theNumCaptures = theSbAccess.GetNumCaptures()
        for theCapture in range(theNumCaptures):
            theImageName = theSbAccess.GetImageName(theCapture)
            print('the image name for capture: ',theCapture,' is: ',theImageName)
            theNumX = theSbAccess.GetNumXColumns(theCapture)
            print('    the num X: ',theNumX)

        theCapture = 0;
        theNumRows = theSbAccess.GetNumYRows(theCapture)
        theNumColumns = theSbAccess.GetNumXColumns(theCapture)
        theNumPlanes = theSbAccess.GetNumZPlanes(theCapture)

        theOutId = theSbAccess.CreateImageGroup('Made By Python 2',1,theNumPlanes,theNumRows,theNumColumns,1)
        #theOutId = theSbAccess.CopyImageGroup(0)

        for theZPlane in range(theNumPlanes):
            image = theSbAccess.ReadImagePlaneBuf(theCapture,0,0,theZPlane,0) #captureid,position,timepoint,zplane,channel
            # np.insert(the3DVolume,theNumRows*theNumColumns,image)
            print ("*** theZPlane: ",theZPlane," The read buffer len is: " , len(image))
            theSbAccess.WriteImagePlaneBuf(theOutId,0,theZPlane,0,image)


        data = input("Please hit Enter to exit:\n")
        print("Done")


        return

def test_new_slide():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theInpSlideId = theSbAccess.Open("E:\Data\Slides_msi\QweekTour.sldy");

        theNumCaptures = theSbAccess.GetNumCaptures()
        for theCapture in range(theNumCaptures):
            theImageName = theSbAccess.GetImageName(theCapture)
            print('the image name for capture: ',theCapture,' is: ',theImageName)
            theNumX = theSbAccess.GetNumXColumns(theCapture)
            print('    the num X: ',theNumX)

        theInpCaptureIndex = 0;
        theNumRows = theSbAccess.GetNumYRows(theInpCaptureIndex)
        theNumColumns = theSbAccess.GetNumXColumns(theInpCaptureIndex)
        theNumPlanes = theSbAccess.GetNumZPlanes(theInpCaptureIndex)
        theNumChannels = theSbAccess.GetNumChannels(theInpCaptureIndex)

        theOutSlideId = theSbAccess.CreateNewSlide()

        theOutCaptureIndex = theSbAccess.CreateImageGroup('Made By Python 2',theNumChannels,theNumPlanes,theNumRows,theNumColumns,1)

        for theZPlane in range(theNumPlanes):
            for theChannel in range(theNumChannels):
                #access the input slide
                theSbAccess.SetTargetSlide(theInpSlideId)
                image = theSbAccess.ReadImagePlaneBuf(theInpCaptureIndex,0,0,theZPlane,theChannel) #captureid,position,timepoint,zplane,channel
                #access the output slide
                theSbAccess.SetTargetSlide(theOutSlideId)
                theSbAccess.WriteImagePlaneBuf(theOutCaptureIndex,0,theZPlane,theChannel,image) #CaptureIndex,TimepointIndex,ZPlaneIndex,ChannelIndex,ByteArray


        data = input("Please hit Enter to exit:\n")
        print("Done")


        return

def test_create_new_slide():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)

        theOutSlideId = theSbAccess.CreateNewSlide()
        #close the slide in slidebook and test here to get an error because slide is not there anymore
        time.sleep(20)

        success = theSbAccess.SetTargetSlide(theOutSlideId)
        
        return theOutSlideId

def test_set_target_slide():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)

        success = theSbAccess.SetTargetSlide(0)
        
        return success

def test_create_and_setset_target_slide():

    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)

        theOutSlideId = theSbAccess.CreateNewSlide()
        success = theSbAccess.SetTargetSlide(theOutSlideId)

        return success

def test_plot_3dstack():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theSbAccess.Open("E:\Data\Slides_msi\QweekTour.sldy");

        theNumCaptures = theSbAccess.GetNumCaptures()
        for theCapture in range(theNumCaptures):
            theImageName = theSbAccess.GetImageName(theCapture)
            print('the image name for capture: ',theCapture,' is: ',theImageName)
            theNumX = theSbAccess.GetNumXColumns(theCapture)
            print('    the num X: ',theNumX)

        theCapture = 0;
        theNumRows = theSbAccess.GetNumYRows(theCapture)
        theNumColumns = theSbAccess.GetNumXColumns(theCapture)
        theNumPlanes = theSbAccess.GetNumZPlanes(theCapture)
        theVoxelX,theVoxelY,theVoxelZ = theSbAccess.GetVoxelSize(theCapture)
        theNumChannels = theSbAccess.GetNumChannels(theCapture)
        for theChannel in range(theNumChannels):
            name = theSbAccess.GetChannelName(theCapture,theChannel)
            print('Channel Name: ',name)


        the3DVolume = np.empty(theNumRows*theNumColumns*theNumPlanes,np.uint16)
        for theZPlane in range(theNumPlanes):
            image = theSbAccess.ReadImagePlaneBuf(theCapture,0,0,theZPlane,0) #captureid,position,timepoint,zplane,channel
            # np.insert(the3DVolume,theNumRows*theNumColumns,image)
            print ("*** theZPlane: ",theZPlane," The read buffer len is: " , len(image))
            image = image.reshape(theNumRows,theNumColumns)

            #plot the slice

            plt.imshow(image)
            plt.pause(0.001)

        #the3DVolume = the3DVolume.reshape(theNumRows,theNumColumns,theNumPlanes
        data = input("Please hit Enter to exit:\n")
        print("Done")


        return
def test_plot_mask():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theSbAccess.Open("E:\Data\Slides_msi\QweekTour.sldy");
        #theSbAccess.Open("E:\\Data\\Slides_msi\\3D Montage\\big3d.sldy");

        theNumCaptures = theSbAccess.GetNumCaptures()
        for theCapture in range(theNumCaptures):
            theImageName = theSbAccess.GetImageName(theCapture)
            print('the image name for capture: ',theCapture,' is: ',theImageName)
            theNumMasks = theSbAccess.GetNumMasks(theCapture)
            for theMask in range(theNumMasks):
                theMaskName = theSbAccess.GetMaskName(theCapture,theMask)
                print('The mask Name for index ',theMask,' is: ',theMaskName)

        theCapture = 0
        theMask = 1
        theNumRows = theSbAccess.GetNumYRows(theCapture)
        theNumColumns = theSbAccess.GetNumXColumns(theCapture)
        theNumPlanes = theSbAccess.GetNumZPlanes(theCapture)

        the3DVolume = np.empty(theNumRows*theNumColumns*theNumPlanes,np.uint16)
        for theZPlane in range(1):
            image = theSbAccess.ReadMaskPlaneBuf(theCapture,theMask,0,theZPlane) #captureid,maskName,timepoint,zplane
            print ("*** the maskZPlane: ",theZPlane," The read buffer len is: " , len(image))
            image = image.reshape(theNumRows,theNumColumns)
            theSbAccess.WriteMaskPlaneBuf(theCapture,"Mask Made by Python",0,theZPlane,image)


            #plot the slice

            plt.imshow(image)
            plt.pause(0.001)

        #the3DVolume = the3DVolume.reshape(theNumRows,theNumColumns,theNumPlanes
        data = input("Please hit Enter to exit:\n")
        print("Done")


        return

def test_send_mask():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        #theSbAccess.Open("E:\Data\Slides_msi\QweekTour.sldy");
        theSbAccess.Open("E:\\Data\\Slides_msi\\3D Montage\\big3d.sldy");

        theNumCaptures = theSbAccess.GetNumCaptures()
        for theCapture in range(theNumCaptures):
            theImageName = theSbAccess.GetImageName(theCapture)
            print('the image name for capture: ',theCapture,' is: ',theImageName)
            theNumMasks = theSbAccess.GetNumMasks(theCapture)
            for theMask in range(theNumMasks):
                theMaskName = theSbAccess.GetMaskName(theCapture,theMask)
                print('The mask Name for index ',theMask,' is: ',theMaskName)

        theCapture = 0
        theMask = 1
        theNumRows = theSbAccess.GetNumYRows(theCapture)
        theNumColumns = theSbAccess.GetNumXColumns(theCapture)
        theNumPlanes = theSbAccess.GetNumZPlanes(theCapture)

        theMaskArray = np.zeros(theNumRows*theNumColumns,dtype='uint16')
        theMaskArray = theMaskArray.reshape(theNumRows,theNumColumns)

        for theZPlane in range(1):
            theSbAccess.WriteMaskPlaneBuf(theCapture,"Mask Made by Python",0,theZPlane,theMaskArray)



        data = input("Please hit Enter to exit:\n")
        print("Done")


        return

def test_start_capture():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    #title = "Timepoint: {tp:6d}, Mean: {mn:.1f}"
    title = "Timepoint: {tp:6d}"
    testStop = False

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        theSbAccess = SBAccess(s)
        theCapture = theSbAccess.StartCapture('0000');

        while True:
            res = theSbAccess.IsCapturing()
            theLastCapture = theSbAccess.GetLastImageCaptured(theCapture)
            time.sleep(0.02)
            if(res and theLastCapture > 0):
                break


        theImageName = theSbAccess.GetImageName(theCapture)
        print('the image name for capture: ',theCapture,' is: ',theImageName)
        theNumChannels = theSbAccess.GetNumChannels(theCapture)
        theNumRows = theSbAccess.GetNumYRows(theCapture)
        theNumColumns = theSbAccess.GetNumXColumns(theCapture)
        theNumPlanes = theSbAccess.GetNumZPlanes(theCapture)
        theNumTimepoints = theSbAccess.GetNumTimepoints(theCapture) # the max number of timepoints to record

        the3DVolume = np.empty(theNumRows*theNumColumns*theNumPlanes,np.uint16)
        thePreviousCapture = -1

        theCnt = 0
        while True:
            time.sleep(0.02)
            res = theSbAccess.IsCapturing()
            if(not res):
                break

            theLastCapture = theSbAccess.GetLastImageCaptured(theCapture)
            if(theLastCapture == thePreviousCapture):
                continue

            print("theLastCapture {0}, thePreviousCapture {1}".format(theLastCapture,thePreviousCapture))
            for theTP in range(thePreviousCapture+1,theLastCapture+1):  # include theLastCapture

                for theChannel in range(theNumChannels):
                    for theZPlane  in range(theNumPlanes):
                        image = theSbAccess.ReadImagePlaneBuf(theCapture,0,theTP,theZPlane,theChannel) #captureid,position,timepoint,zplane,channel
                        # np.insert(the3DVolume,theNumRows*theNumColumns,image)
                        print ("*** read theTP: ",theTP)
                        if(theTP > 200 and testStop):
                            theSbAccess.StopCapture()
                            break
                        if (len(image) > 0):
                            average = sum(image.astype(float)) / len(image) #avoid overflow
                            print(" TP = {0}, Ch = {1}, Z = {2} Average pixel intensity = {3}".format(theTP,theChannel,theZPlane, average))
                        """
                        if( theCnt % 100 == 0):
                            image = image.reshape(theNumRows,theNumColumns)

                            #plot the slice

                            plt.imshow(image)
                            plt.title(title.format(tp=theTP),loc='left')
                            plt.pause(0.001)
                        """

                        theCnt = theCnt + 1
            thePreviousCapture = theLastCapture
            if(theLastCapture == theNumTimepoints-1):
                break
            res = theSbAccess.IsCapturing()
            if(not res):
                break

        #the3DVolume = the3DVolume.reshape(theNumRows,theNumColumns,theNumPlanes
        data = input("Please hit Enter to exit:\n")
        print("Done")


        return

def test_plot_current_capture():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    #title = "Timepoint: {tp:6d}, Mean: {mn:.1f}"
    title = "Timepoint: {tp:6d}"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theCapture = theSbAccess.GetCurrentCaptureId(0)
        while True:
            res = theSbAccess.IsCapturing()
            theLastCapture = theSbAccess.GetLastImageCaptured(theCapture)
            time.sleep(0.02)
            if(res and theLastCapture > 0):
                break


        theImageName = theSbAccess.GetImageName(theCapture)
        print('the image name for capture: ',theCapture,' is: ',theImageName)
        theNumChannels = theSbAccess.GetNumChannels(theCapture)
        theNumRows = theSbAccess.GetNumYRows(theCapture)
        theNumColumns = theSbAccess.GetNumXColumns(theCapture)
        theNumPlanes = theSbAccess.GetNumZPlanes(theCapture)
        theNumTimepoints = theSbAccess.GetNumTimepoints(theCapture) # the max number of timepoints to record

        the3DVolume = np.empty(theNumRows*theNumColumns*theNumPlanes,np.uint16)
        thePreviousCapture = -1

        theCnt = 0
        while True:
            time.sleep(0.02)
            res = theSbAccess.IsCapturing()
            if(not res):
                break

            theLastCapture = theSbAccess.GetLastImageCaptured(theCapture)
            if(theLastCapture == thePreviousCapture):
                continue

            for theTP in range(thePreviousCapture+1,theLastCapture+1):  # include theLastCapture

                for theChannel in range(theNumChannels):
                    for theZPlane  in range(theNumPlanes):
                        image = theSbAccess.ReadImagePlaneBuf(theCapture,0,theTP,theZPlane,theChannel) #captureid,position,timepoint,zplane,channel
                        # np.insert(the3DVolume,theNumRows*theNumColumns,image)
                        print ("*** read theTP: ",theTP)
                        if(theTP > 200 and testStop):
                            theSbAccess.StopCapture()
                            break
                        if (len(image) > 0):
                            average = sum(image.astype(float)) / len(image) #avoid overflow
                            print(" TP = {0}, Ch = {1}, Z = {2} Average pixel intensity = {3}".format(theTP,theChannel,theZPlane, average))
                        """
                        if( theCnt % 100 == 0):
                            image = image.reshape(theNumRows,theNumColumns)

                            #plot the slice

                            plt.imshow(image)
                            plt.title(title.format(tp=theTP),loc='left')
                            plt.pause(0.001)
                        """

                        theCnt = theCnt + 1
            thePreviousCapture = theLastCapture
            if(theLastCapture == theNumTimepoints-1):
                break
            res = theSbAccess.IsCapturing()
            if(not res):
                break

        #the3DVolume = the3DVolume.reshape(theNumRows,theNumColumns,theNumPlanes
        data = input("Please hit Enter to exit:\n")
        print("Done")


        return

def test_show_capture_status():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    #title = "Timepoint: {tp:6d}, Mean: {mn:.1f}"
    title = "Timepoint: {tp:6d}"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theCapture = theSbAccess.GetCurrentCaptureId(0)
        while True:
            res = theSbAccess.IsCapturing()
            theLastTimepointCaptured = theSbAccess.GetCurrentTimepointCaptured()
            theLastPlaneCaptured = theSbAccess.GetCurrentPlaneCaptured()
            theLastChannelCaptured = theSbAccess.GetCurrentChannelCaptured()
            time.sleep(0.02)
            if(theLastTimepointCaptured == 0 and theLastPlaneCaptured == 0 and theLastChannelCaptured == 0):
                continue
            if(res and theLastPlaneCaptured >= 0):
                break


        theImageName = theSbAccess.GetImageName(theCapture)
        print('the image name for capture: ',theCapture,' is: ',theImageName)
        theNumChannels = theSbAccess.GetNumChannels(theCapture)
        theNumRows = theSbAccess.GetNumYRows(theCapture)
        theNumColumns = theSbAccess.GetNumXColumns(theCapture)
        theNumPlanes = theSbAccess.GetNumZPlanes(theCapture)
        theNumTimepoints = theSbAccess.GetNumTimepoints(theCapture) # the max number of timepoints to record

        thePreviousTimepointCaptured = -1
        thePreviousChannelCaptured = -1
        thePreviousPlaneCaptured = -1

        while True:
            time.sleep(0.02)
            res = theSbAccess.IsCapturing()
            if(not res):
                break

            theLastTimepointCaptured = theSbAccess.GetCurrentTimepointCaptured()
            theLastChannelCaptured = theSbAccess.GetCurrentChannelCaptured()
            theLastPlaneCaptured = theSbAccess.GetCurrentPlaneCaptured()
            theNumPositions = theSbAccess.GetCurrentNumPositionsCaptured()
            thePositionIndex = theSbAccess.GetCurrentPositionIndexCaptured()
            #print("Last Captured: TP = {0}, Ch = {1}, Z = {2}".format(theLastTimepointCaptured,theLastChannelCaptured,theLastPlaneCaptured))


            if(theLastTimepointCaptured == thePreviousTimepointCaptured and theLastChannelCaptured == thePreviousChannelCaptured and theLastPlaneCaptured == thePreviousPlaneCaptured ):
                continue

            theTP = theLastTimepointCaptured
            theChannel = theLastChannelCaptured
            theZPlane = theLastPlaneCaptured
            if(theNumPositions > 1):
                print(" TP = {0}, Ch = {1}, Z = {2}, Pos = {3} / {4}".format(theTP+1,theChannel+1,theZPlane+1,thePositionIndex+1,theNumPositions))
            else:
                print(" TP = {0}, Ch = {1}, Z = {2}".format(theTP+1,theChannel+1,theZPlane+1))


            thePreviousTimepointCaptured = theLastTimepointCaptured
            thePreviousChannelCaptured = theLastChannelCaptured
            thePreviousPlaneCaptured = theLastPlaneCaptured
            if(theLastTimepointCaptured == theNumTimepoints-1):
                break
            res = theSbAccess.IsCapturing()
            if(not res):
                break

        return

def set_xyz_point_in_focus_xy_tab():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)

        theNumXY, res = theSbAccess.GetXYZPointCount()
        print("The num points", theNumXY)

        theSbAccess.AddXYZPoint(1.0,2.0,3.0)
        theSbAccess.AddXYZPoint(-1.0,-2.0,-3.0)

        theNumXY, res = theSbAccess.GetXYZPointCount()
        print("The num points", theNumXY)

        theSbAccess.ClearXYZPoints()

        theNumXY, res = theSbAccess.GetXYZPointCount()
        print("The num points", theNumXY)

def test_get_xyz_position():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theSbAccess.Open("E:\Data\Slides_msi\PythonTestData\Simple2DTest.sld");
        x = theSbAccess.GetXPosition(0,0)
        print('x is: ',x)
        y = theSbAccess.GetYPosition(0,0)
        print('y is: ',y)

def test_start_streaming():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    #title = "Timepoint: {tp:6d}, Mean: {mn:.1f}"
    title = "Timepoint: {tp:6d}"
    testStop = False

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        theSbAccess = SBAccess(s)
        theCapture = theSbAccess.StartStreaming();

        while True:
            res = theSbAccess.IsStreaming()
            theLastCapture = theSbAccess.GetLastImageStreamed(theCapture)
            time.sleep(0.02)
            if(res and theLastCapture >= 0):
                break


        theImageName = theSbAccess.GetImageName(theCapture)
        print('the image name for capture: ',theCapture,' is: ',theImageName)
        theNumRows = theSbAccess.GetNumYRows(theCapture)
        theNumColumns = theSbAccess.GetNumXColumns(theCapture)
        theNumPlanes = theSbAccess.GetNumZPlanes(theCapture)

        the3DVolume = np.empty(theNumRows*theNumColumns*theNumPlanes,np.uint16)
        thePreviousCapture = -1

        theCnt = 0
        while True:
            time.sleep(0.001)
            res = theSbAccess.IsStreaming()
            if(not res):
                break

            theLastCapture = theSbAccess.GetLastImageStreamed(theCapture)
            if(theLastCapture == thePreviousCapture):
                continue

            for theTP in range(thePreviousCapture+1,theLastCapture+1):  # include theLastCapture

                theZPlane = 0;
                image = theSbAccess.ReadImagePlaneBuf(theCapture,0,theTP,theZPlane,0) #captureid,position,timepoint,zplane,channel
                # np.insert(the3DVolume,theNumRows*theNumColumns,image)
                print ("*** read theTP: ",theTP)
                if(theTP > 200 and testStop):
                    theSbAccess.StopStreaming()
                    break
                if( theCnt % 50 == 0):
                    image = image.reshape(theNumRows,theNumColumns)

                    #plot the slice

                    plt.imshow(image)
                    plt.title(title.format(tp=theTP),loc='left')
                    plt.pause(0.001)

                theCnt = theCnt + 1
            thePreviousCapture = theLastCapture
            theNumTimepoints = theSbAccess.GetNumTimepoints(theCapture) # the max number of timepoints to record
            print('theNumTimepoints =',theNumTimepoints)
            res = theSbAccess.IsStreaming()
            if(not res):
                break
                 


        #the3DVolume = the3DVolume.reshape(theNumRows,theNumColumns,theNumPlanes
        data = input("Please hit Enter to exit:\n")
        print("Done")


        return

def test_focus_window_parameters():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theSbAccess.FocusWindowMainSetExposure(91)
        test_main = True
        test_move = True
        test_scope = True
        test_stream = True
        if(test_main):
            ret = theSbAccess.FocusWindowMainSelectBin('2x2')
            if(ret == 0):
                print('!!! FocusWindowMainSelectBin failed')
            ret = theSbAccess.FocusWindowMainSelectFilterSet('Fixed')
            if(ret == 0):
                print('!!! FocusWindowMainSelectFilterSet failed')
            ret = theSbAccess.FocusWindowMainSelectChannel('561')
            if(ret == 0):
                print('!!! FocusWindowMainSelectChannel failed')
            ret = theSbAccess.FocusWindowMainSelectLaserPower('56')
            if(ret == 0):
                print('!!! FocusWindowMainSelectLaserPower failed')
            ret = theSbAccess.FocusWindowMainSelectNDAuxiliary('23')
            if(ret == 0):
                print('!!! FocusWindowMainSelectNDAuxiliary failed')
            ret = theSbAccess.FocusWindowMainSelectNDPrimary('45')
            if(ret == 0):
                print('!!! FocusWindowMainSelectNDPrimary failed')
            ret = theSbAccess.FocusWindowMainSetFluorOpen();
            time.sleep(2)   # sleep 2 sec
            ret = theSbAccess.FocusWindowMainSetFluorClose();
            ret = theSbAccess.FocusWindowMainSetFluorClose(); # this one will do nothing

            ret = theSbAccess.FocusWindowMainSetAltOpen();
            time.sleep(2)   # sleep 2 sec
            ret = theSbAccess.FocusWindowMainSetAltClose();
            time.sleep(2)   # sleep 2 sec
            ret = theSbAccess.FocusWindowMainSetAltClose(); # this one will do nothing

            ret = theSbAccess.FocusWindowMainSetBrightOpen();
            time.sleep(2)   # sleep 2 sec
            ret = theSbAccess.FocusWindowMainSetBrightClose();

            ret = theSbAccess.FocusWindowMainSetSnap();

            ret = theSbAccess.FocusWindowMainSetStop();
            time.sleep(2)   # sleep 2 sec
            ret = theSbAccess.FocusWindowMainSetLive();
            time.sleep(2)   # sleep 2 sec
            ret = theSbAccess.FocusWindowMainSetStop();
            ret = theSbAccess.FocusWindowMainSetStop();  # this one will do nothing
        if(test_move):
            ret = theSbAccess.FocusWindowMainMoveX(100)
            ret = theSbAccess.FocusWindowMainMoveY(50)
            ret = theSbAccess.FocusWindowMainMoveZPrimary(4.5)

        if(test_scope):
            # scope tab params
            ret = theSbAccess.FocusWindowScopeSelectCameraOrVideo(0) # camera
            time.sleep(2)   # sleep 2 sec
            ret = theSbAccess.FocusWindowScopeSelectCameraOrVideo(1) # video
            ret = theSbAccess.FocusWindowScopeSelectCondenserPosition('Pos 2')
            ret = theSbAccess.FocusWindowScopeSelectEmissionSelection(1)
            ret = theSbAccess.FocusWindowScopeSelectMagnificationChanger('4x')
            ret = theSbAccess.FocusWindowScopeSelectObjective('10x Dry')
            ret = theSbAccess.FocusWindowScopeSetLampVoltage(35)
            ret = theSbAccess.FocusWindowScopeSetCondenserAperture(53)

        if(test_stream):
            ret = theSbAccess.FocusWindowStreamSetNumberFrames(300)
            ret = theSbAccess.FocusWindowStreamSetNumberFramesToAverage('3')

def test_focus_window_add_region():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        #theSbAccess.LiveWindowAddRectangleRegion(0,400,400,200,200)
        #theSbAccess.LiveWindowAddEllipseRegion(0,600,700,100,100,True)
        #theSbAccess.LiveWindowAddLineRegion(0,800,700,200,200)
        theSbAccess.LiveWindowAddPolygonRegion(0,[800,700,900,700,950,800,750,1050])


def test_get_objectives():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theObjectiveList = theSbAccess.GetObjectives()

        for lens in theObjectiveList:
            print("lens name ",lens.mName)
            print("mActualMagnification ",lens.mActualMagnification)
            print("mMicronPerPixel ",lens.mMicronPerPixel)
            print("")

        theFilterList = theSbAccess.GetFilters()

        for filter in theFilterList:
            print("filter name ",filter.mName)
            print("")

        theMagnificationChangerList = theSbAccess.GetMagnificationChangers()

        for magnificationChanger in theMagnificationChangerList:
            print("magnificationChanger name ",magnificationChanger.mName)
            print("")

    return

def test_image_capture():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        result = theSbAccess.ConfirmFocusWindow()
        print(f"Focus window confirmed =  {'yes' if result == 1 else 'no'}")

        width, height, image, Result = theSbAccess.CaptureImage(0, 50)
        print("Width =", width, "height =", height, "First pixel =", image[0], f"success =  {'yes' if Result == 1 else 'no'}")

        if (len(image) > 0):
            average = sum(image.astype(float)) / len(image) #avoid overflow
            print("Average pixel intensity =", average)
        image = image.reshape(height,width)

        #plot the slice
        plt.imshow(image)
        #plt.title(title.format(tp=theTP),loc='left')
        #plt.pause(0.001)
        #data = input("Please hit Enter to exit:\n")
        #print("Done")

        #test error handling
        width, height, image, Result = theSbAccess.CaptureImage(7, 50)
        if (width > 0 and height > 0):
            print("Width =", width, "height =", height, "First pixel =", image[0], f"success =  {'yes' if Result == 1 else 'no'}")
        else:
            print("Width =", width, "height =", height, f"success =  {'yes' if Result == 1 else 'no'}")

    return

def test_ao():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)

        isEnabled = theSbAccess.GetIsHardwareComponentEnabled(MicroscopeHardwareComponent.AdaptiveOptics)

        theResultString, theResult = theSbAccess.SetAOOptimizerExposureTime(10)

    return


def test_tirf_hardware():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        result = theSbAccess.ConfirmFocusWindow()
        print(f"Focus window confirmed =  {'yes' if result == 1 else 'no'}" )

        Radius_mV, X_mV, Y_mV, Duration_ms, MotorPos, MotorEnable, SpinEnable = theSbAccess.FocusWindowGetTIRFParameters(0 )
        print("Radius=", Radius_mV, "X =", X_mV, "Y =", Y_mV, "Motor =", MotorPos, f"Motor enabled=  {'yes' if MotorEnable == 1 else 'no'}",  f"Spin enabled=  {'yes' if SpinEnable == 1 else 'no'}" )

        theSbAccess.FocusWindowSetTIRFParameters(0, 500, 500, 500, 20, MotorPos, 1, 1, 0)
        result = theSbAccess.SetHardwareComponentPosition(MicroscopeHardwareComponent.TIRFSlider, 0)

        theSbAccess.FocusWindowSetTIRFParameters(0, 1000, -500, -500, 20, MotorPos, 1, 1, 0)
        result = theSbAccess.SetHardwareComponentPosition(MicroscopeHardwareComponent.TIRFSlider, 0)

        theSbAccess.FocusWindowSetTIRFParameters(0, 500, 500, 500, 20, MotorPos, 1, 1, 0)
        result = theSbAccess.SetHardwareComponentPosition(MicroscopeHardwareComponent.TIRFSlider, 0)

        StepperPos = theSbAccess.GetVector3StepperPosition()
        print("Stepper pos =", StepperPos)
        result = theSbAccess.SetVector3StepperPosition(StepperPos + 1)
        print("Selecting new stepper pos =", StepperPos + 1, f"success =  {'yes' if result == 1 else 'no'}")
        StepperPos = theSbAccess.GetVector3StepperPosition()
        print("Confirming stepper pos =", StepperPos)

        theX_mV, theY_mV, isSpin = theSbAccess.GetVector3ScannerPosition()
        print("X =", theX_mV, "Y =", theY_mV, f"Spin =  {'yes' if isSpin == 1 else 'no'}")

        Result = theSbAccess.SetVector3ScannerPosition(theX_mV + 10, theY_mV + 50, 1)
        print("Set new X =", theX_mV + 10, "Y =", theY_mV + 50, f"Result =  {'success' if Result == 1 else 'fail'}")

        theX_mV, theY_mV, isSpin = theSbAccess.GetVector3ScannerPosition()
        print("X =", theX_mV, "Y =", theY_mV, f"Spin =  {'yes' if isSpin == 1 else 'no'}")

        width, height, image, Result = theSbAccess.CaptureImage(0, 50)
        print("Width =", width, "height =", height, "First pixel =", image[0], f"success =  {'yes' if Result == 1 else 'no'}")

def test_arc_slice_tirf():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        result = theSbAccess.ConfirmFocusWindow()
        print(f"Focus window confirmed =  {'yes' if result == 1 else 'no'}" )

        isSupported = theSbAccess.FocusWindowSupportsARCSliceTIRF()
        print(f"ARC/Slice enabled=  {'yes' if isSupported == 1 else 'no'}" )

        if (isSupported):
            arcs, slices, result = theSbAccess.FocusWindowGetARCSliceTIRFParameters(1)
            print("Position 1 arcs=", arcs,"slices=", slices, f"success =  {'yes' if result == 1 else 'no'}")
            rand_arc = random.randint(910,1800)
            arcs = f"450,900,{rand_arc},3600"
            rand_slice = random.randint(200,2000)
            slices = f"10,{rand_slice}"
            print("Setting arc =", arcs, "slices =", slices)
            result = theSbAccess.FocusWindowSetARCSliceTIRFParameters(1, arcs, slices, 0)
            arcs, slices, result = theSbAccess.FocusWindowGetARCSliceTIRFParameters(1)
            print("Position 1 arcs=", arcs,"slices=", slices, f"success =  {'yes' if result == 1 else 'no'}")

            arcs = f"450,900,{rand_arc},3600"
            rand_slice = random.randint(1000,2000)
            slices = ""
            print("Setting arc =", arcs, "slices =", slices)
            result = theSbAccess.FocusWindowSetARCSliceTIRFParameters(1, arcs, slices, 0)
            arcs, slices, result = theSbAccess.FocusWindowGetARCSliceTIRFParameters(1)
            print("Position 1 arcs=", arcs,"slices=", slices, f"success =  {'yes' if result == 1 else 'no'}")
        else:
            print("Not supported")


def test_get_hardware_metadata():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        for x in range (46):
            try:
                isEnabled = theSbAccess.GetIsHardwareComponentEnabled(x)
                theName = theSbAccess.GetHardwareComponentName(x)
                print("Component", x + 1, "name  = ", theName + f"enabled =  {'yes' if isEnabled else 'no'}")
            except:
                print("Component", x + 1, "is not supported")

def test_get_set_shutter(inComponentID):
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        isEnabled = theSbAccess.GetIsHardwareComponentEnabled(inComponentID)
        if isEnabled:
            theName = theSbAccess.GetHardwareComponentName(inComponentID)
            # read current state
            theOrigState, success = theSbAccess.GetHardwareComponentOpen(inComponentID)
            print("Component", inComponentID, "name =", theName, f"startup state = {'open' if theOrigState == 1 else 'closed'}", f"success = {'yes' if success else 'no'}")

            # toggle current state
            theNewState = 1
            if (theOrigState == 1):
                theNewState = 0

            success = theSbAccess.SetHardwareComponentOpen(inComponentID, theNewState)
            print("Component", inComponentID, "name =", theName, f"setting new state = {'open' if theNewState == 1 else 'closed'}", f"success = {'yes' if success else 'no'}")

            # confirm new state
            theReadPosition, success = theSbAccess.GetHardwareComponentOpen(inComponentID)
            print("Component", inComponentID, "name =", theName, f"reading back state = {'open' if theReadPosition == 1 else 'closed'}", f"success = {'yes' if success else 'no'}")

            #set back to original state
            success = theSbAccess.SetHardwareComponentOpen(inComponentID, theOrigState)
            print("Component", inComponentID, "name =", theName, f"restoring original state = {'open' if theOrigState == 1 else 'closed'}", f"success = {'yes' if success else 'no'}")
        return

def test_get_microscope_state():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        try:
            theObj = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentObjective)
            theFilter = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentFilter)
            theMag = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentMagnification)

            thePower = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentLaserPower)
            theND = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentNDPrimary)
            theAuxND = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentNDAux)
            theLamp = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentLampVoltage)
            theFL = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentFLshutter)

            theBF = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentBFshutter)
            theAlt = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentAltSource)
            theXY = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentXYstagePosition)
            theZ = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentZstagePosition)
            theAuxZ = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentAltZstagePosition)

            theCondenser = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentCondenserPrismPosition)
            theCameraPos = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentVideoOrCameraPosition)
            theCondenserAperture = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentCondenserAperture)
            theBin = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentBin)
            theFilterSet = theSbAccess.GetMicroscopeState(MicroscopeStates.CurrentFilterSet)

        except:
            print ("failed")

        return

def test_get_hardware_position(inComponentID, inPosition):
    HOST = '127.0.0.1'  # The server's hostname or IP address
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            theSbAccess = SBAccess(s)
            isEnabled = theSbAccess.GetIsHardwareComponentEnabled(inComponentID)
            if isEnabled:
                theName = theSbAccess.GetHardwareComponentName(inComponentID)
                theMinMax, result = theSbAccess.GetHardwareComponentMinMax(inComponentID)
                theOrigPosition = theSbAccess.GetHardwareComponentPosition(inComponentID)
                print("Component", inComponentID, "name =", theName, "min =",  theMinMax[0], "max", theMinMax[1],  "original position ",  theOrigPosition, f"result = {'success' if result == 1 else 'failure'}")

                isSuccess = theSbAccess.SetHardwareComponentPosition(inComponentID, inPosition)
                print("Component", inComponentID, "name =", theName, "new position =", inPosition, f"success =  {'yes' if isSuccess else 'no'}")

                theReadPosition, result = theSbAccess.GetHardwareComponentPosition(inComponentID)
                print("Component", inComponentID, "name =", theName, "read position ", theReadPosition, f"result = {'success' if result == 1 else 'failure'}")
    except:
        print("test_get_hardware_position failed")
    return

def test_get_hardware_location_microns(inComponentID : MicroscopeHardwareComponent):
    HOST = '127.0.0.1'  # The server's hostname or IP address
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            theSbAccess = SBAccess(s)
            isEnabled = theSbAccess.GetIsHardwareComponentEnabled(inComponentID)
            if isEnabled:
                theName = theSbAccess.GetHardwareComponentName(inComponentID)

                theX, theY, theZ = theSbAccess.GetHardwareComponentLocationMicrons(inComponentID)
                print("Component", inComponentID, "name =", theName, "GetHardwareComponentMicrons ", "z =",  theX, "y=", theY,  "z=",  theZ)

                isSuccess = theSbAccess.SetHardwareComponentLocationMicrons(inComponentID, theX + 1, theY + 1, theZ + 1)
                print("Component", inComponentID, "name =", theName, "SetHardwareComponentMicrons ", "z =", theX + 1, "y=", theY + 1, "z=", theZ + 1)

                theX, theY, theZ = theSbAccess.GetHardwareComponentLocationMicrons(inComponentID)
                print("Component", inComponentID, "name =", theName, "GetHardwareComponentMicrons ", "z =", theX, "y=", theY, "z=", theZ)

                isSuccess = theSbAccess.IncrementHardwareComponentLocationMicrons(inComponentID, 1, 1, 1)
                print("Component", inComponentID, "name =", theName, "IncrementHardwareComponentLocationMicrons ", "z =", 1, "y=", 1, "z=", 1)

                theX, theY, theZ = theSbAccess.GetHardwareComponentLocationMicrons(inComponentID)
                print("Component", inComponentID, "name =", theName, "GetHardwareComponentMicrons ", "z =", theX, "y=", theY, "z=",  theZ)

    except:
        print("test_get_hardware_location failed")

def get_xyz_point_list():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        the_xyz_point_list = theSbAccess.GetXYZPointList()
        print("the_xyz_point_list\n",the_xyz_point_list)

def test_save_as_slide():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theOutSlideId = theSbAccess.CreateNewSlide()
        theSbAccess.SaveAsSlide(theOutSlideId,"E:\\Data\\Slides_msi\\3D Montage\\test_save_as.sldy")

def test_close_slide():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theOutSlideId = theSbAccess.CreateNewSlide()
        isModified, theResult = theSbAccess.GetIsSlideModified(theOutSlideId)
        print("SlideID", theOutSlideId, f"result = {'success' if theResult == 1 else 'failure'}", f"is modified = {'yes' if isModified == 1 else 'no'}")
        theResult = theSbAccess.CloseSlide(theOutSlideId,0)

def test_close_modified_slide():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theOutSlideId = theSbAccess.GetCurrentSlideId()
        isModified, theResult = theSbAccess.GetIsSlideModified(theOutSlideId)
        print("SlideID", theOutSlideId, f"result = {'success' if theResult == 1 else 'failure'}", f"is modified = {'yes' if isModified == 1 else 'no'}")
        theResult = theSbAccess.CloseSlide(theOutSlideId,1)
        print("CloseSlide, res: ",theResult)


def test_save_slide():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theOutSlideId = theSbAccess.GetCurrentSlideId()
        theSbAccess.SaveSlide(theOutSlideId)

def test_focus_surface():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)

        theSbAccess.FocusSurface_Open()
        theSbAccess.FocusSurface_ClearCalibrationPoints()
        theSbAccess.FocusSurface_AddCalibrationPoint(10000,10000,-100)
        theSbAccess.FocusSurface_AddCalibrationPoint(20000,10000,200)
        theSbAccess.FocusSurface_AddCalibrationPoint(20000,40000,350)
        theSbAccess.FocusSurface_AddCalibrationPoint(30000,40000,550)
        theSbAccess.FocusSurface_FitSurface()
        if(theSbAccess.FocusSurface_IsSurfaceFit()):
            theZ = theSbAccess.FocusSurface_FitPoint(15000,10000);
            print("the Z of the fitted  point is: ",theZ)

def test_run_saved_script():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)

        theSbAccess.RunSavedScript('C:\\ProgramData\\Intelligent Imaging Innovations\\SlideBook 2025\\Users\\Default User\\Scripts\\exp2.sbs')
        data = input("Please hit Enter to exit:\n")
        print("Done")

def test_run_user_script():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)

        #substitute your file on the Python_Export
        #must not use thread to do a plot
        theString = """
OpenSlide(Filename = "E:\Data\Slides_msi\QweekTour.sldy")
Python_SetEnvironment(Environment ="DeepCGH",UseThread=false)
Python_Export("Metaphase B-Cell","FITC", First =0, Last =49, Matrix = "PyImg")
Python_RunCommand(Command="from matplotlib import pyplot as plt;")
Python_RunCommand(Command="plt.figure(1);")
Python_RunCommand(Command="plt.imshow(PyImg[1,:,:]);")
Python_RunCommand(Command="plt.pause(1);")
"""
        theSbAccess.RunUserScript(theString)
        data = input("Please hit Enter to exit:\n")
        print("Done")

def test_xyz_saved_experiment_name():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)

        theExperimentName, theRes = theSbAccess.GetXYZSavedExperimentName(2)
        print('GetXYZSavedExperimentName: theExperimentName: ',theExperimentName)
        print('GetXYZSavedExperimentName: theRes: ',theRes)

        #now set a NON eexisting name
        theRes = theSbAccess.SetXYZSavedExperimentName(2,'pincopallino')
        print('SetXYZSavedExperimentName: theRes: ',theRes)
        #check if worked
        theExperimentName, theRes = theSbAccess.GetXYZSavedExperimentName(2)
        print('GetXYZSavedExperimentName: theExperimentName: ',theExperimentName)
        print('GetXYZSavedExperimentName: theRes: ',theRes)

        #now set an existing name
        theRes = theSbAccess.SetXYZSavedExperimentName(2,'003d')

        #check if worked
        print('SetXYZSavedExperimentName: theRes: ',theRes)
        theExperimentName, theRes = theSbAccess.GetXYZSavedExperimentName(2)
        print('GetXYZSavedExperimentName: theExperimentName: ',theExperimentName)
        print('GetXYZSavedExperimentName: theRes: ',theRes)

def test_get_open_slides():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        theDict = theSbAccess.GetOpenSlides()
        for id, path in theDict.items():
            print(f"{id} -> {path}")

def main():
    try:
        #test_new_slide()
        #test_plot_mask()
        #test_send_mask()
        #test_plot_3dstack()
        #test_plot_current_capture()
        #test_start_capture()
        #test_add_new_channel()
        #test_copy_capture()
        #set_xyz_point_in_focus_xy_tab()
        #test_get_xyz_position()
        #test_start_streaming()
        #test_focus_window_parameters()
        #test_focus_window_add_region()
        #test_create_new_slide()
        #test_set_target_slide()
        #test_create_and_setset_target_slide()
        #test_get_objectives()
        #test_get_hardware_metadata()
        #test_get_hardware_location_microns(MicroscopeHardwareComponent.ZStage)
        #test_get_hardware_position(MicroscopeHardwareComponent.ExcitationFilterWheel, 10)
        #test_get_hardware_position(MicroscopeHardwareComponent.FluorescenceShutter, 10)
        #test_get_set_shutter(MicroscopeHardwareComponent.BrightfieldShutter)
        #test_get_microscope_state()
        #test_get_xyz_point_list()
        #test_save_slide()
        #test_save_as_slide()
        #test_close_slide()
        #test_close_modified_slide()
    	#test_tirf_hardware()
        #test_arc_slice_tirf()
        #test_image_capture()
        #test_ao()
        #test_show_capture_status()
        #test_focus_surface()
        #test_run_saved_script()
        #test_run_user_script()
        #test_xyz_saved_experiment_name()
        test_get_open_slides()
    except Exception as e:
        print(f"Error: {e}")
    except: 
        print("Error")
    finally:
        print("Finished")

if __name__ == "__main__":
    main()
        


