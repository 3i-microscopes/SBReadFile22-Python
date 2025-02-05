import socket
import numpy as np
import time
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
        
        return theOutSlideId

def test_set_target_slide():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)

        success = theSbAccess.SetTargetSlide(1)
        
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

        theNumCaptures = theSbAccess.GetNumCaptures()
        for theCapture in range(theNumCaptures):
            theImageName = theSbAccess.GetImageName(theCapture)
            print('the image name for capture: ',theCapture,' is: ',theImageName)
            theNumMasks = theSbAccess.GetNumMasks(theCapture)
            for theMask in range(theNumMasks):
                theMaskName = theSbAccess.GetMaskName(theCapture,theMask)
                print('The mask Name for index ',theMask,' is: ',theMaskName)

        theCapture = 0
        theMask = 5
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

                theZPlane = 0;
                image = theSbAccess.ReadImagePlaneBuf(theCapture,0,theTP,theZPlane,0) #captureid,position,timepoint,zplane,channel
                # np.insert(the3DVolume,theNumRows*theNumColumns,image)
                print ("*** read theTP: ",theTP)
                if(theTP > 200 and testStop):
                    theSbAccess.StopCapture()
                    break
                if( theCnt % 100 == 0):
                    image = image.reshape(theNumRows,theNumColumns)

                    #plot the slice

                    plt.imshow(image)
                    plt.title(title.format(tp=theTP),loc='left')
                    plt.pause(0.001)

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

                theZPlane = 0;
                image = theSbAccess.ReadImagePlaneBuf(theCapture,0,theTP,theZPlane,0) #captureid,position,timepoint,zplane,channel
                # np.insert(the3DVolume,theNumRows*theNumColumns,image)
                print ("*** read theTP: ",theTP)
                if( theCnt % 100 == 0):
                    image = image.reshape(theNumRows,theNumColumns)

                    #plot the slice

                    plt.imshow(image)
                    plt.title(title.format(tp=theTP),loc='left')
                    plt.pause(0.001)

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

def set_xyz_point_in_focus_xy_tab():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)

        theSbAccess.AddXYZPoint(1.0,2.0,3.0)
        theSbAccess.AddXYZPoint(-1.0,-2.0,-3.0)

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


def test_get_xyz_point_list():
    HOST = '127.0.0.1'  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        theSbAccess = SBAccess(s)
        the_xyz_point_list = theSbAccess.GetXYZPointList()
        print("the_xyz_point_list\n",the_xyz_point_list)


def main():
    #test_new_slide()
    #test_plot_mask()
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
    test_get_xyz_point_list()

if __name__ == "__main__":
    main()
        


