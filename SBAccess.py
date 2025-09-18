from __future__ import annotations
__copyright__  = "Copyright (c) 2022-2025, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."

#Help obtained with the command:
#python -c "import SBAccess ; help(SBAccess)"
#check syntax with: pyflakes SBaccess.py

#Must set the right put to where CMetadataLib.py and Basedecode.py are
#import sys
#they are in the sandbox, or on github
#sys.path.append('C:/Users/Nicola Papp/Perforce/Nicola_MSI_552/dev/SB_7.0_BCG/SBReadFile/dist/Python/Format 7')
import io
from CMetadataLib import BaseDecoder
from CMetadataLib import CLensDef70
from CMetadataLib import CFluorDef70
from CMetadataLib import COptovarDef70
from enum import Enum
import yaml


import ByteUtil as bu
import numpy as np

class MicroscopeStates(Enum):
    """
    Enumeration of microscope state codes used to represent various 
    hardware settings or readouts from a microscope control system.
    """

    CurrentObjective = 1
    """Current objective lens in use."""

    CurrentFilter = 2
    """Current filter in use."""

    CurrentMagnification = 3
    """Current total magnification."""

    CurrentLaserPower = 4
    """Current laser power setting."""

    CurrentNDPrimary = 5
    """Current position of the primary neutral density (ND) filter."""

    CurrentNDAux = 6
    """Current position of the auxiliary ND filter."""

    CurrentLampVoltage = 7
    """Current lamp voltage level."""

    CurrentFLshutter = 8
    """Current state of the fluorescence shutter (open/closed)."""

    CurrentBFshutter = 9
    """Current state of the brightfield shutter (open/closed)."""

    CurrentAltSource = 10
    """Current alternative illumination source."""

    CurrentXYstagePosition = 11
    """Current XY stage coordinates."""

    CurrentZstagePosition = 12
    """Current Z stage position."""

    CurrentAltZstagePosition = 13
    """Current position of an alternate Z stage (if present)."""

    CurrentCondenserPrismPosition = 14
    """Current position of the condenser prism."""

    CurrentVideoOrCameraPosition = 15
    """Current position of the video/camera selector."""

    CurrentCondenserAperture = 16
    """Current condenser aperture setting."""

    CurrentBin = 17
    """Current camera binning setting."""

    CurrentFilterSet = 18
    """Current active filter set."""



class MicroscopeHardwareComponent(Enum):
    """
    Enumeration of direct microscope hardware components for low-level access
    and control within microscope systems.
    """

    ExcitationFilterWheel = 0 #:The excitation filter wheel component.

    FilterTurret = 1 #:The filter turret (e.g., for dichroics or filter sets).

    EmissionFilterWheel = 2
    """The emission filter wheel component."""

    FluorescenceShutter = 3
    """Shutter controlling the fluorescence light path."""

    BrightfieldShutter = 4
    """Shutter controlling the brightfield light path."""

    BrightfieldLamp = 5
    """The brightfield illumination source."""

    LCDFilter = 6
    """LCD-based filter or attenuator component."""

    XYStage = 7
    """Motorized XY stage."""

    ZStage = 8
    """Primary motorized Z-axis stage."""

    ObjectiveTurret = 9
    """Turret for switching microscope objectives."""

    OptovarTurret = 10
    """Optovar turret for magnification adjustment."""

    OcularPhotoPrism = 11
    """Selector between ocular and photo/camera paths."""

    CameraVideoPrism = 12
    """Prism directing light to camera or video system."""

    AltSourceSelection = 13
    """Selector for alternate illumination sources."""

    FluorescenceLamp = 14
    """Main fluorescence lamp (e.g., mercury or LED)."""

    AuxZStage = 15
    """Auxiliary Z-axis stage."""

    AuxFluorescenceLamp = 16
    """Secondary fluorescence lamp."""

    AuxFilterWheel = 17
    """First auxiliary filter wheel."""

    AuxFilterWheel2 = 18
    """Second auxiliary filter wheel."""

    AuxFilterWheel3 = 19
    """Third auxiliary filter wheel."""

    LaserAblationDevice = 20
    """Laser ablation or photoactivation system."""

    SACorrection = 21
    """Spherical aberration correction mechanism."""

    ReuseThisPosition = 22
    """Special placeholder for reusing previous hardware positions."""

    AuxFilterWheel4 = 23
    """Fourth auxiliary filter wheel."""

    TIRFSlider = 24
    """Total internal reflection fluorescence (TIRF) slider."""

    LaserPowerControl = 25
    """Laser power control module."""

    AdaptiveOptics = 26
    """Adaptive optics component for wavefront correction."""

    BeamExpander = 27
    """Optical beam expander system."""

    AuxFilterWheel5 = 28
    """Fifth auxiliary filter wheel."""

    AuxFilterWheel6 = 29
    """Sixth auxiliary filter wheel."""

    IncubatorControl = 30
    """Environmental control system (e.g., incubator)."""

    LaserTemperatureControl = 31
    """Laser temperature stabilization or monitoring module."""

    LaserPowerMeter = 32
    """First laser power meter."""

    Lightsheet = 33
    """Lightsheet illumination system."""

    AuxFilterWheel7 = 34
    """Seventh auxiliary filter wheel."""

    LaserPowerMeter2 = 35
    """Second laser power meter."""

    LaserPowerMeter3 = 36
    """Third laser power meter."""

    LaserPowerMeter4 = 37
    """Fourth laser power meter."""

    AuxFilterWheel8 = 41
    """Eighth auxiliary filter wheel."""

    AuxFilterWheel9 = 42
    """Ninth auxiliary filter wheel."""

    AuxFilterWheel10 = 43
    """Tenth auxiliary filter wheel."""

    PMTController1 = 44
    """First photomultiplier tube (PMT) controller."""

    PMTController2 = 45
    """Second PMT controller."""

    PMTController3 = 46
    """Third PMT controller."""
    
#: Descriptions for each MicroscopeHardwareComponent enum member.

descriptions = {
    MicroscopeHardwareComponent.ExcitationFilterWheel: "The excitation filter wheel component.",
    MicroscopeHardwareComponent.FilterTurret: "The filter turret (e.g., for dichroics or filter sets).",
    MicroscopeHardwareComponent.EmissionFilterWheel: "The emission filter wheel component.",
    MicroscopeHardwareComponent.FluorescenceShutter: "Shutter controlling the fluorescence light path.",
    MicroscopeHardwareComponent.BrightfieldShutter: "Shutter controlling the brightfield light path.",
    MicroscopeHardwareComponent.BrightfieldLamp: "The brightfield illumination source.",
    MicroscopeHardwareComponent.LCDFilter: "LCD-based filter or attenuator component.",
    MicroscopeHardwareComponent.XYStage: "Motorized XY stage.",
    MicroscopeHardwareComponent.ZStage: "Primary motorized Z-axis stage.",
    MicroscopeHardwareComponent.ObjectiveTurret: "Turret for switching microscope objectives.",
    MicroscopeHardwareComponent.OptovarTurret: "Optovar turret for magnification adjustment.",
    MicroscopeHardwareComponent.OcularPhotoPrism: "Selector between ocular and photo/camera paths.",
    MicroscopeHardwareComponent.CameraVideoPrism: "Prism directing light to camera or video system.",
    MicroscopeHardwareComponent.AltSourceSelection: "Selector for alternate illumination sources.",
    MicroscopeHardwareComponent.FluorescenceLamp: "Main fluorescence lamp (e.g., mercury or LED).",
    MicroscopeHardwareComponent.AuxZStage: "Auxiliary Z-axis stage.",
    MicroscopeHardwareComponent.AuxFluorescenceLamp: "Secondary fluorescence lamp.",
    MicroscopeHardwareComponent.AuxFilterWheel: "First auxiliary filter wheel.",
    MicroscopeHardwareComponent.AuxFilterWheel2: "Second auxiliary filter wheel.",
    MicroscopeHardwareComponent.AuxFilterWheel3: "Third auxiliary filter wheel.",
    MicroscopeHardwareComponent.LaserAblationDevice: "Laser ablation or photoactivation system.",
    MicroscopeHardwareComponent.SACorrection: "Spherical aberration correction mechanism.",
    MicroscopeHardwareComponent.ReuseThisPosition: "Special placeholder for reusing previous hardware positions.",
    MicroscopeHardwareComponent.AuxFilterWheel4: "Fourth auxiliary filter wheel.",
    MicroscopeHardwareComponent.TIRFSlider: "Total internal reflection fluorescence (TIRF) slider.",
    MicroscopeHardwareComponent.LaserPowerControl: "Laser power control module.",
    MicroscopeHardwareComponent.AdaptiveOptics: "Adaptive optics component for wavefront correction.",
    MicroscopeHardwareComponent.BeamExpander: "Optical beam expander system.",
    MicroscopeHardwareComponent.AuxFilterWheel5: "Fifth auxiliary filter wheel.",
    MicroscopeHardwareComponent.AuxFilterWheel6: "Sixth auxiliary filter wheel.",
    MicroscopeHardwareComponent.IncubatorControl: "Environmental control system (e.g., incubator).",
    MicroscopeHardwareComponent.LaserTemperatureControl: "Laser temperature stabilization or monitoring module.",
    MicroscopeHardwareComponent.LaserPowerMeter: "First laser power meter.",
    MicroscopeHardwareComponent.Lightsheet: "Lightsheet illumination system.",
    MicroscopeHardwareComponent.AuxFilterWheel7: "Seventh auxiliary filter wheel.",
    MicroscopeHardwareComponent.LaserPowerMeter2: "Second laser power meter.",
    MicroscopeHardwareComponent.LaserPowerMeter3: "Third laser power meter.",
    MicroscopeHardwareComponent.LaserPowerMeter4: "Fourth laser power meter.",
    MicroscopeHardwareComponent.AuxFilterWheel8: "Eighth auxiliary filter wheel.",
    MicroscopeHardwareComponent.AuxFilterWheel9: "Ninth auxiliary filter wheel.",
    MicroscopeHardwareComponent.AuxFilterWheel10: "Tenth auxiliary filter wheel.",
    MicroscopeHardwareComponent.PMTController1: "First photomultiplier tube (PMT) controller.",
    MicroscopeHardwareComponent.PMTController2: "Second PMT controller.",
    MicroscopeHardwareComponent.PMTController3: "Third PMT controller.",
}

class SBAccess(object):

    """ A Class to Read Slide Book Format 7 Files """

    # All access functions as in SBReadFile.h

    def __init__(self, inSocket):
        self.mSocket = inSocket

    def SendCommand(self,inCommand):
        theBytes = bu.string_to_bytes(inCommand)
        self.mSocket.send(theBytes)

    def SendVal(self,inVal,inType):
        theBytes = bu.type_to_bytes(inVal,inType)
        self.mSocket.send(theBytes)

    def mysend(self, inBytes):
        totalsent = 0
        MSGLEN = len(inBytes)
        while totalsent < MSGLEN:
            sent = self.mSocket.send(inBytes[totalsent:])
            #print("sent: ",sent)
            if sent == 0:
                raise Exception("Socket connection broken, unable to send")
            totalsent = totalsent + sent
        #print("totalsent: ",totalsent)

    def SendByteArray(self,inBytes):
        #self.mSocket.send(inBytes)
        self.mysend(inBytes)

    def RecvBigData(self,n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = self.mSocket.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def Recv(self):

        theRecvBuf = b''
        b = self.mSocket.recv(1)
        if b != b'&':
            raise Exception("First character in answer must be a: &")
        while True:
            b = self.mSocket.recv(1)
            if b == b'(':
                continue
            if b == b')':
                break;

            theRecvBuf += bytes(b)
        # parse the string
        str = bu.bytes_to_string(theRecvBuf)
        #print("str is: ",str)
        #split in list of arguments
        largs = str.split(',')
        #receive all the largs
        if(len(largs) != 1):
            raise Exception("Can only receive n values of same type")
        arg = largs[0]

        #split is size and format
        prop = arg.split(":")
        if(len(prop) != 2):
            raise Exception("Invalid argument format: " + str)
        theNum = int(prop[0])
        theType = prop[1]

        theSize = 1
        if (theType == 'i4' or theType == 'u4' or theType == 'f4'):
            theSize = 4
        elif (theType == 'i2' or theType == 'u2'):
            theSize = 2
        elif (theType == 'i8' or theType == 'u8' or theType == 'f8'):
            theSize = 8

        theValBuf = b''
        theValBuf =  self.RecvBigData(theNum * theSize)
        #print('theValBuf is: ',theValBuf)

        if(len(theValBuf) != theNum * theSize):
            raise Exception("Did not receive enough data")

        if theType == 's':
            theStr = bu.bytes_to_string(theValBuf)
            return theStr
        else:
            theArr = bu.bytes_to_type(theValBuf,theType)
            return theNum,theArr
        
    def SendIntParam(self,inCommandName,inIntParam):
        self.SendCommand('$'+inCommandName+'(IntParam=i4)')
        self.SendVal(int(inIntParam),'i4')
        theNum,theVals = self.Recv()
        if( theNum != 1 and theVals[0] != 1):
            raise Exception(inCommandName+': error')
        return theVals[0]

    def SendFloatParam(self,inCommandName,inFloatParam):
        self.SendCommand('$'+inCommandName+'(FloatParam=f4)')
        self.SendVal(float(inFloatParam),'f4')
        theNum,theVals = self.Recv()
        if( theNum != 1 and theVals[0] != 1):
            raise Exception(inCommandName+': error')
        return theVals[0]

    def SendStringParam(self,inCommandName,inStringParam):
        l = len(inStringParam)
        self.SendCommand('$'+inCommandName+'(StringParam='+str(l)+':s)')
        self.SendVal(inStringParam,'s')
        theNum,theVals = self.Recv()
        if( theNum != 1 or theVals[0] == -1):
            raise Exception(inCommandName+': error')
        return theVals[0]

    def SendNullParam(self,inCommandName):
        self.SendCommand('$'+inCommandName+'()')
        theNum,theVals = self.Recv()
        if( theNum != 1 and theVals[0] != 1):
            raise Exception(inCommandName+': error')
        return theVals[0]



    def Open(self,inPath):
        """Open a SlideBook file and loads the Metadata

        Parameters
        ----------
        inPath : str
            The path of the SlideBook file to open

        Returns
        -------
        int
            The Slide Id
        """
        l = len(inPath)
        self.SendCommand('$Open(FileName='+str(l)+':s)')
        self.SendVal(inPath,'s')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("OpenFile: colud not open path: "+inPath)
        return theVals[0]

    def GetCurrentSlideId(self):
        """Gets the Slide Id of the active slide

        Parameters
        ----------
            none

        Returns
        -------
        int
            The Slide Id
        """
        self.SendCommand('$GetCurrentSlideId()')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetCurrentSlideId: error")
        return theVals[0]

    def GetOpenSlides(self):
        """Gets a dictionary of  Slide Id  vs Pathname of all open slides

        Parameters
        ----------
            none

        Returns
        -------
        dict
            The dictionary of IDs/SlideName(Pathname)
        """
        self.SendCommand('$GetOpenSlides()')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetOpenSlides: error")
        theDict = dict()
        for id in range(theVals[0]):

            theNum,theVals = self.Recv()
            if( theNum != 1):
                raise Exception("GetOpenSlides: error")
            theId = theVals[0]
            thePath = self.Recv()
            theDict[theId]= thePath

        return theDict


    def SetTargetSlide(self,inSlideId):
        """Sets the target slide for subsequent operations 

        Parameters
        ----------
        int
            The Slide Id

        Returns
        -------
        int
            1 on success
        """

        self.SendCommand('$SetTargetSlide(SlideId=i4)')
        self.SendVal(int(inSlideId),'i4')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("SetTargetSlide: invalid value")
        if( theVals[0] != 1):
            raise Exception("SetTargetSlide: failed")

        return

    def CreateNewSlide(self):
        """Creates a new Slide

        Returns
        -------
        int
            The Slide Id
        """
        self.SendCommand('$CreateNewSlide()')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("CreateNewSlide: error")
        return theVals[0]

    def CloseSlide(self,inSlideId,inSaveChanges):
        """Close a slide
        Parameters
        ----------
        inSlideId : int
            The Slide Id
        inSaveChanges
            If the slide has been modified, save changes?

        Returns
        -------
        int
            True if successful and false if failure (failure to save is most commonly caused by a new file without a pathname)
        """
        self.SendCommand('$CloseSlide(SlideId=i4,SaveChanges=i4)')
        self.SendVal(int(inSlideId),'i4')
        self.SendVal(int(inSaveChanges),'i4')
        theNum,theStatus = self.Recv()
        if( theNum != 1):
            raise Exception("SaveSlide: invalid statuc")

        return theStatus[0]

    def GetIsSlideModified(self, inSlideId):
        """Get modified status of slide
        Parameters
        ----------
        inSlideId : int
            The Slide Id

        Returns
        -------
        bool
            True if file has been modified since last save, false if the file has not been modified
        int
            True if successful and false if failure
        """
        self.SendCommand('$GetIsSlideModified(SlideId=i4)')
        self.SendVal(int(inSlideId), 'i4')
        theNum, theStatus = self.Recv()
        if (theNum != 1):
            raise Exception("SaveSlide: invalid status")
        theNum, theReturn = self.Recv()
        if (theNum != 1):
            raise Exception("SaveSlide: invalid return")

        return theStatus[0], theReturn[0]

    def SaveSlide(self,inSlideId):
        """Saves a slide
        Parameters
        ----------
        inSlideId : int
            The Slide Id

        Returns
        -------
        int
            1 on success
        """
        self.SendCommand('$SaveSlide(SlideId=i4)')
        self.SendVal(int(inSlideId),'i4')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("SaveSlide: invalid value")
        if( theVals[0] != 1):
            raise Exception("SaveSlide: failed")

        return

    def SaveAsSlide(self,inSlideId,inPathname):
        """Saves a slide
        Parameters
        ----------
        inSlideId : int
            The Slide Id

        inPathname : str
            The pathname to save the slide with
            

        Returns
        -------
        int
            1 on success
        """
        l = len(inPathname)
        self.SendCommand('$SaveAsSlide(SlideId=i4,Pathname='+str(l)+':s)')
        self.SendVal(int(inSlideId),'i4')
        self.SendVal(inPathname,'s')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("SaveAsSlide: invalid value")
        if( theVals[0] != 1):
            raise Exception("SaveAsSlide: failed")

        return


    def GetNumCaptures(self):
        """ Gets the number of captures (image groups) in the file

        Returns
        -------
        int
            The number of captures
        """

        self.SendCommand('$GetNumCaptures()')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetNumCaptures: invalid value")

        print("GetNumCaptures: ",theVals[0])

        return theVals[0]

    def GetNumLiveCaptures(self):
        """ Gets the number of live captures (image groups) in the file

        Returns
        -------
        int
            The number of live captures
        """

        self.SendCommand('$GetNumLiveCaptures()')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetNumLiveCaptures: invalid value")

        print("GetNumLiveCaptures: ",theVals[0])

        return theVals[0]

    def GetNumMasks(self,inCaptureIndex):
        """ Gets the number of masks in an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        int
            The number of masks
        """

        self.SendCommand('$GetNumMasks(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetNumMasks: invalid value")


        return theVals[0]

    def GetNumPositions(self,inCaptureIndex):
        """ Gets the number of (montage) positions in an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        int
            The number of positions
        """

        self.SendCommand('$GetNumPositions(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetNumPositions: invalid value")


        return theVals[0]

    def GetNumXColumns(self,inCaptureIndex):
        """ Gets the number of columns (width) of an image in an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        int
            The number of columns or width of the image
        """
        self.SendCommand('$GetNumXColumns(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetNumXColumns: invalid value")

        print("GetNumXColumns: ",theVals[0])

        return theVals[0]

    def GetNumYRows(self,inCaptureIndex):
        """ Gets the number of rows (height) of an image in an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        int
            The number of rows or height of the image
        """

        self.SendCommand('$GetNumYRows(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetNumYRows: invalid value")

        print("GetNumYRows: ",theVals[0])

        return theVals[0]
        


    def GetNumZPlanes(self,inCaptureIndex):
        """ Gets the number of z planes of an image in an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        int
            The number of z planes of the image
        """

        self.SendCommand('$GetNumZPlanes(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetNumZPlanes: invalid value")

        print("GetNumZPlanes: ",theVals[0])

        return theVals[0]


    def GetNumTimepoints(self,inCaptureIndex):
        """ Gets the number of time points in an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        int
            The number of time points
        """

        self.SendCommand('$GetNumTimepoints(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetNumTimepoints: invalid value")


        return theVals[0]


    def GetNumChannels(self,inCaptureIndex):
        """ Gets the number of channels in an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        int
            The number of channels
        """
        self.SendCommand('$GetNumChannels(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetNumChannels: invalid value")

        return theVals[0]

    def GetExposureTime(self,inCaptureIndex,inChannelIndex):
        """ Gets the exposure time in ms for a particular channel of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        inChannelIndex: int
            The index of the channel. Must be in range(0,number of channels)

        Returns
        -------
        int
            The exposure time in ms
        """
        self.SendCommand('$GetExposureTime(CaptureIndex=i4,ChannelIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetExposureTime: invalid value")

        return theVals[0]


    def GetVoxelSize(self,inCaptureIndex):
        """ Gets the voxel size in microns of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        float
            The X voxel size in um
        float
            The Y voxel size in um
        float
            The Z voxel size in um

        """
        self.SendCommand('$GetVoxelSize(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')

        theNum,theVoxelX = self.Recv()
        if( theNum != 1):
            raise Exception("GetVoxelSize: invalid value")

        theNum,theVoxelY = self.Recv()
        if( theNum != 1):
            raise Exception("GetVoxelSize: invalid value")

        theNum,theVoxelZ = self.Recv()
        if( theNum != 1):
            raise Exception("GetVoxelSize: invalid value")

        return theVoxelX[0],theVoxelY[0],theVoxelZ[0]


    def GetXPosition(self,inCaptureIndex,inPositionIndex):
        """ Gets the X position in microns of the center of an image of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inPositionIndex: int
            The index of the image in the montage, or 0 if all images are at the same location

        Returns
        -------
        float
            The X position in um
        """
        self.SendCommand('$GetXPosition(CaptureIndex=i4,PositionIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inPositionIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetXPosition: invalid value")

        return theVals[0]

    def GetYPosition(self,inCaptureIndex,inPositionIndex):
        """ Gets the Y position in microns of the center of an image of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inPositionIndex: int
            The index of the image in the montage, or 0 if all images are at the same location

        Returns
        -------
        float
            The Y position in um
        """
        self.SendCommand('$GetYPosition(CaptureIndex=i4,PositionIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inPositionIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetYPosition: invalid value")

        return theVals[0]



    def GetZPosition(self,inCaptureIndex,inPositionIndex,inZPlaneIndex):
        """ Gets the Z position in microns of the center of an image of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inPositionIndex: int
            The index of the image in the montage, or 0 if all images are at the same location

        Returns
        -------
        float
            The Z position in um
        """
        self.SendCommand('$GetZPosition(CaptureIndex=i4,PositionIndex=i4,ZPlaneIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inPositionIndex),'i4')
        self.SendVal(int(inZPlaneIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetZPosition: invalid value")

        return theVals[0]



    def GetMontageRow(self,inCaptureIndex,inPositionIndex):
        """ Gets the rows of the montage at a given position in an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inPositionIndex: int
            The position of an image whose row is to be retrieved

        Returns
        -------
        int
            The row number (first row is 0)
        """
        self.SendCommand('$GetMontageRow(CaptureIndex=i4,PositionIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inPositionIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetMontageRow: invalid value")

        return theVals[0]

    def GetMontageColumn(self,inCaptureIndex,inPositionIndex):
        """ Gets the number of columns of the montage at a given position in an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inPositionIndex: int
            The position of an image whose column is to be retrieved

        Returns
        -------
        int
            The column number (first column is 0) 
        """
        self.SendCommand('$GetMontageColumn(CaptureIndex=i4,PositionIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inPositionIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetMontageColumn: invalid value")

        return theVals[0]

    def GetElapsedTime(self,inCaptureIndex,inTimepointIndex):
        """ Gets the elapsed time in ms at a given time point in an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inTimepointIndex: int
            The time point number

        Returns
        -------
        int
            The elapsed time in ms
        """
        self.SendCommand('$GetElapsedTime(CaptureIndex=i4,TimepointIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inTimepointIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetElapsedTime: invalid value")

        return theVals[0]



    def GetChannelName(self,inCaptureIndex,inChannelIndex):
        """ Gets the name of a given channel of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        inChannelIndex: int
            The index of the channel. Must be in range(0,number of channels)

        Returns
        -------
        str
            The name of the channel
        """
        self.SendCommand('$GetChannelName(CaptureIndex=i4,ChannelIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')

        theStr = self.Recv()
        return theStr

    def GetLensName(self,inCaptureIndex):
        """ Gets the name of the lens of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        str
            The name of the lens
        """
        self.SendCommand('$GetLensName(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')

        theStr = self.Recv()
        return theStr

    def GetMagnification(self,inCaptureIndex):
        """ Gets the magnification of the lens of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        float
            The magnification of the lens
        """
        self.SendCommand('$GetMagnification(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetMagnification: invalid value")

        return theVals[0]


    def GetImageName(self,inCaptureIndex):
        """ Gets the name of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        str
            The name of the image group
        """

        self.SendCommand('$GetImageName(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')

        theStr = self.Recv()
        return theStr
        
    def GetImageLowRenormalization(self,inCaptureIndex,inChannelIndex):
        """ Gets the default low renormalization value for channel

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inChannelIndex: int
            The channel number. Must be in range (0,number of channels)

        Returns
        -------
        int
            The low renormalization value (0-65535) 
        """
        self.SendCommand('$GetImageLowRenormalization(CaptureIndex=i4,ChannelIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetImageLowRenormalization: invalid value")

        return theVals[0]

    def GetImageHighRenormalization(self,inCaptureIndex,inChannelIndex):
        """ Gets the default high renormalization value for channel

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inChannelIndex: int
            The channel number. Must be in range (0,number of channels)

        Returns
        -------
        int
            The low renormalization value (0-65535) 
        """
        self.SendCommand('$GetImageHighRenormalization(CaptureIndex=i4,ChannelIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetImageHighRenormalization: invalid value")

        return theVals[0]
        
    def GetMaskName(self,inCaptureIndex,inMaskIndex):
        """ Gets the name of a mask

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        inMaskIndex: int
            The index of the mask. Must be in range(0,number of masks)

        Returns
        -------
        str
            The name of the mask
        """

        self.SendCommand('$GetMaskName(CaptureIndex=i4,MaskIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inMaskIndex),'i4')

        theStr = self.Recv()
        return theStr

    def GetImageComment(self,inCaptureIndex):
        """ Gets the comments of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        str
            The comments of the image group
        """
        self.SendCommand('$GetImageComment(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')

        theStr = self.Recv()
        return theStr

    def GetCaptureDate(self,inCaptureIndex):
        """ Gets the date of acquisition of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        str
            date is inhe format: yyyy:MM:dd:hh:mm:ss
        """
        self.SendCommand('$GetCaptureDate(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')

        theStr = self.Recv()
        return theStr

    def GetObjectives(self):
        """ Gets the objectives

        Parameters
        ----------
            none

        Returns
        -------
        list
            a list of CLensDef70 objects
        """
        self.SendCommand('$GetObjectives()')

        theStr = self.Recv()
        txt_stream = io.StringIO(theStr)
        theNode = yaml.compose(txt_stream)
        theLastIndex = 0
        theDecoder = BaseDecoder()
        theObjectiveCount,theLastIndex = theDecoder.GetIntValue(theNode, theLastIndex, 'ObjectiveCount')
        theObjectiveList = []
        for theObjectiveIndex in range(theObjectiveCount):
            theLensDef70 = CLensDef70()
            theLastIndex = theLensDef70.Decode(theNode, theLastIndex)
            theObjectiveList.append(theLensDef70)


        return theObjectiveList

    def GetAOOptimizerStatus(self):
        """ Returns the current AO optimizer status and settings

        Parameters
        ----------
        none

        Returns
        -------
        Number of Zernike mode
            Returns the number of Zernike modes
        Zernike Modes
            Returns an array of Zernike modes
        Minimum Amplitude
            The minimum amplitude
        Maximum Amplitude
            The maximum amplitude
        Exposure Time MS
            Exposure time (ms)
        Iterations
            Number of iterations
        Merit Function
            Name of merit function, or unknown
        Result
            1 = success 0 = failure

        """
        self.SendCommand('$GetAOOptimizerStatus')

        theNum, theNumZernikes = self.Recv()
        if (theNum != 1):
            raise Exception("GetAOOptimizerStatus: failed")

        theNum, theZernikes = self.Recv()
        if (theNum != theNumZernikes):
            raise Exception("GetAOOptimizerStatus: failed")

        theNum, theMinAmp = self.Recv()
        if (theNum != 1):
            raise Exception("GetAOOptimizerStatus: failed")

        theNum, theMaxAmp = self.Recv()
        if (theNum != 1):
            raise Exception("GetAOOptimizerStatus: failed")

        theNum, theExposureTime = self.Recv()
        if (theNum != 1):
            raise Exception("GetAOOptimizerStatus: failed")

        theMeritFunction = self.Recv()

        theNum, theResult = self.Recv()
        if (theNum != 1):
            raise Exception("GetAOOptimizerStatus: failed")

        return theNumZernikes, theZernikes, theMinAmp, theMaxAmp, theExposureTime, theMeritFunction, theResult

    def SetAOOptimizerExposureTime(self, inExposureTimeMS):
        """ Set the open or close position of a hardware device

        Parameters
        ----------
        inExposureTimeMS
            New exposure time in ms

        Returns
        -------
        string
            Returns information about the status of the command
        bool
            Returns success or failure

        """
        self.SendCommand('$SetAOOptimizerExposureTime(ExposureTimeMS=i4)')
        self.SendVal(int(inExposureTimeMS), 'i4')
        theResultString = self.Recv()

        theNum, theResult = self.Recv()
        if (theNum != 1):
            raise Exception("SetAOOptimizerExposureTime: failed")

        if (theResult[0] > 0):
            theResult = True
        else:
            theResult = False

        return theResultString, theResult

    def GetFilters(self):
        """ Gets the filters

        Parameters
        ----------
            none

        Returns
        -------
        list
            a list of CFluorDef70 objects
        """
        self.SendCommand('$GetFilters()')

        theStr = self.Recv()
        txt_stream = io.StringIO(theStr)
        theNode = yaml.compose(txt_stream)
        theLastIndex = 0
        theDecoder = BaseDecoder()
        theFilterCount,theLastIndex = theDecoder.GetIntValue(theNode, theLastIndex, 'FilterCount')
        theFilterList = []
        for theFilterIndex in range(theFilterCount):
            theFluorDef70 = CFluorDef70()
            theLastIndex = theFluorDef70.Decode(theNode, theLastIndex)
            theFilterList.append(theFluorDef70)


        return theFilterList


    def GetMagnificationChangers(self):
        """ Gets the Magnification Changers

        Parameters
        ----------
            none

        Returns
        -------
        list
            a list of COptovarDef70 objects
        """
        self.SendCommand('$GetMagnificationChangers()')

        theStr = self.Recv()

        txt_stream = io.StringIO(theStr)
        theNode = yaml.compose(txt_stream)
        theLastIndex = 0
        theDecoder = BaseDecoder()
        theMagnificationChangerCount,theLastIndex = theDecoder.GetIntValue(theNode, theLastIndex, 'MagnificationChangerCount')
        theMagnificationChangerList = []
        for theMagnificationChangerIndex in range(theMagnificationChangerCount):
            theOptovarDef70 = COptovarDef70()
            theLastIndex = theOptovarDef70.Decode(theNode, theLastIndex)
            theMagnificationChangerList.append(theOptovarDef70)


        return theMagnificationChangerList


    def GetLensInfo(self):
        """ Gets the lens info

        Parameters
        ----------
            none

        Returns
        -------
        str
            the objectives
        """
        self.SendCommand('$GetLensInfo()')

        theStr = self.Recv()
        return theStr

    def CaptureImage(self,CameraIndex,ExposureTimeMS):
        """ Return an image from the specified camera

                Parameters
                ----------
                CameraIndex: int
                    The index of the image group. Must be in range(0, maximum number of cameras (6)) and the camera must be valid
                ExposureTimeMS: int
                    The desired camera exposure time in milliseconds

                Returns
                -------
                width
                    The width in pixels
                height
                    The height in pixels
                numpy uint16 array 
                    The image is returned as 1D numpy uint16 array
                bool
                    True (1) if success false (0) if failure
                """
        self.SendCommand('$CaptureImage(CameraIndex=i4,ExposureTime=i4)')
        self.SendVal(int(CameraIndex), 'i4')
        self.SendVal(int(ExposureTimeMS), 'i4')

        theNum, theWidth = self.Recv()
        if (theNum != 1):
            raise Exception("CaptureCameraImage: failed")
        theNum, theHeight = self.Recv()
        if (theNum != 1):
            raise Exception("CaptureCameraImage: failed")

        theNum, theVals = self.Recv()

        theNum, theResult = self.Recv()
        if (theNum != 1):
            raise Exception("CaptureCameraImage: failed")

        return theWidth[0], theHeight[0], theVals, theResult


    def ReadImagePlaneBuf(self,inCaptureIndex,inPositionIndex,inTimepointIndex,inZPlaneIndex,inChannelIndex):
        """ Reads a z plane of an image into a numpy array

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inPositionIndex: int
            The position of the image. If the image group is not a montage, use 0
        inTimepointIndex: int
            The time point
        inZPlaneIndex: int
            The z plane number
        inChannelIndex: int
            The channel number

        Returns
        -------
        numpy uint16 array 
            The image is returned as 1D numpy uint16 array

        """
        self.SendCommand('$ReadImagePlaneBuf(CaptureIndex=i4,PositionIndex=i4,TimepointIndex=i4,ZPlaneIndex=i4,ChannelIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inPositionIndex),'i4')
        self.SendVal(int(inTimepointIndex),'i4')
        self.SendVal(int(inZPlaneIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')

        theNum,theVals = self.Recv()
        return theVals

    def GetAuxDataXMLDescriptor(self,inCaptureIndex,inChannelIndex):
        """ Gets the Auxiliary Data XML Descriptor for an image group and a channel
        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inChannelIndex: int
            The channel number

        Returns
        -------
        str
            The XML Descriptor
        """
        self.SendCommand('$GetAuxDataXMLDescriptor(CaptureIndex=i4,ChannelIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')

        theStr = self.Recv()
        return theStr


    def GetAuxDataNumElements(self,inCaptureIndex,inChannelIndex):
        """ Gets the Auxiliary Data number of elements for an image group and a channel
        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inChannelIndex: int
            The channel number

        Returns
        -------
        int
            The number of elements
        """
        self.SendCommand('$GetAuxDataNumElements(CaptureIndex=i4,ChannelIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetAuxDataNumElements: invalid value")

        return theVals[0]


        

    def GetAuxFloatData(self,inCaptureIndex,inChannelIndex):
        """ Gets the Auxiliary Float Data for an image group and a channel
        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inChannelIndex: int
            The channel number

        Returns
        -------
        list : float
            The Float Data as a list
        """
        self.SendCommand('$GetAuxFloatData(CaptureIndex=i4,ChannelIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')

        theNum,theVals = self.Recv()
        return theVals


    def GetAuxDoubleData(self,inCaptureIndex,inChannelIndex):
        """ Gets the Auxiliary Double Data for an image group and a channel
        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inChannelIndex: int
            The channel number

        Returns
        -------
        list : float
            The Double Data as a list
        """
        self.SendCommand('$GetAuxDoubleData(CaptureIndex=i4,ChannelIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')

        theNum,theVals = self.Recv()
        return theVals



    def GetAuxSInt32Data(self,inCaptureIndex,inChannelIndex):
        """ Gets the Auxiliary Signed Int32 Data for an image group and a channel
        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inChannelIndex: int
            The channel number

        Returns
        -------
        list: int
            The Signed Int32 Data as a list
        """
        self.SendCommand('$GetAuxSInt32Data(CaptureIndex=i4,ChannelIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')

        theNum,theVals = self.Recv()
        return theVals


    def GetAuxSInt64Data(self,inCaptureIndex,inChannelIndex):
        """ Gets the Auxiliary Signed Int64 Data for an image group and a channel
        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inChannelIndex: int
            The channel number

        Returns
        -------
        list: int
            The Signed Int64 Data as a list
        """
        self.SendCommand('$GetAuxSInt64Data(CaptureIndex=i4,ChannelIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')

        theNum,theVals = self.Recv()
        return theVals


    def GetAuxSerializedData(self,inCaptureIndex,inChannelIndex,inElementIndex):
        """ Gets the Auxiliary XML Data for an image group and a channel
        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inChannelIndex: int
            The channel number

        Returns
        -------
        list: str
            The XML Data as a list
        """
        self.SendCommand('$GetAuxSerializedData(CaptureIndex=i4,ChannelIndex=i4,ElementIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')
        self.SendVal(int(inElementIndex),'i4')

        theStr = self.Recv()
        return theStr
        
    def CreateImageGroup(self,inImageName,inNumChannels,inNumPlanes,inNumRows,inNumColumns,inNumTimepoints):
        """ creates a new image in the current slide

        Parameters
        ----------
        inImageName:    str
            The name of the image
        inNumChannels: int
            The number of channels in the image. Must be in the range(1,8)
        inNumPlanes: int
            The number of planes in the image (numZ). Must be in the range(1,65535)
        inNumRows: int
            The number of rows in the image (numY). Must be in the range(2,2^11)
        inNumColumns: int
            The number of columns in the image (numX). Must be in the range(2,2^11)
        inNumTimepoints: int
            The number of timepoints in the image (numT). Must be in the range(1,2^11)

        Returns
        -------
        int
            The index of the image group.
        """
        l = len(inImageName)

        self.SendCommand('$CreateImageGroup(ImageName='+str(l)+':s,NumChannels=i4,NumPlanes=i4,NumRows=i4,NumColumns=i4,NumTimepoints=i4)')
        self.SendVal(inImageName,'s')
        self.SendVal(int(inNumChannels),'i4')
        self.SendVal(int(inNumPlanes),'i4')
        self.SendVal(int(inNumRows),'i4')
        self.SendVal(int(inNumColumns),'i4')
        self.SendVal(int(inNumTimepoints),'i4')

        theNum,theVals = self.Recv()
        return theVals

    def CopyImageGroup(self,inCopyCaptureIndex):
        """ Copy an image group from another one

        Parameters
        ----------
        inCopyCaptureIndex: int
            The index of the source image group. Must be in range(0,number of captures)
        Returns
        -------
        none
        """
        self.SendCommand('$CopyImageGroup(CopyCaptureIndex=i4)')
        self.SendVal(int(inCopyCaptureIndex),'i4')
        theNum,theVals = self.Recv()
        return theVals

    def SetImageComment(self,inCaptureIndex,inComment):

        """ Sets the comment (info) of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inComment:    str
            The comments of the image

        Returns
        -------
        none
        """
        l = len(inComment)
        self.SendCommand('$SetImageComment(CaptureIndex=i4,Comment='+str(l)+':s)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(inComment,'s')


    def SetChannelName(self,inCaptureIndex,inChannelIndex,inChannelName):
        """ Sets the name of an channel

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inChannelIndex: int
            The index of the channel in range(0,NumChannels-1)
        inChannelName:  str
            The name of the channel

        Returns
        -------
        none
        """
        l = len(inChannelName)
        self.SendCommand('$SetChannelName(CaptureIndex=i4,ChannelIndex=i4,ChannelName='+str(l)+':s)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')
        self.SendVal(inChannelName,'s')


    def SetMagnification(self,inCaptureIndex,inLensMagnification,inOptovarMagnification):
        """ Sets the Magnification of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inMagnification: float
            The inMagnification of the image

        Returns
        -------
        none
        """
        
        self.SendCommand('$SetMagnification(CaptureIndex=i4,LensMagnification=f4,OptovarMagnification=f4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(float(inLensMagnification),'f4')
        self.SendVal(float(inOptovarMagnification),'f4')

    def SetVoxelSize(self,inCaptureIndex,inSizeX,inSizeY,inSizeZ):
        """ Sets the voxel size in microns of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inSizeX: float
            The X voxel size in um
        inSizeY: float
            The Y voxel size in um
        inSizeZ: float
            The Z voxel size in um

        Returns
        -------
        none
        """
        
        self.SendCommand('$SerVoxelSize(CaptureIndex=i4,SizeX=f4,SizeY=f4,SizeZ=f4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(float(inSizeX),'f4')
        self.SendVal(float(inSizeY),'f4')
        self.SendVal(float(inSizeZ),'f4')

    def SetCaptureDate(self,inCaptureIndex,inYear,inMonth,inDay,inHour,inMinute,inSecond):
        """ Sets the date of acquisition of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inDateStr: str
            date is in the format: yyyy:MM:dd:hh:mm:ss

        Returns
        -------
        none
        """
        self.SendCommand('$SetCaptureDate(CaptureIndex=i4,Year=i4,Month=i4,Day=i4,Hour=i4,Minute=i4,Second=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inYear),'i4')
        self.SendVal(int(inMonth),'i4')
        self.SendVal(int(inDay),'i4')
        self.SendVal(int(inHour),'i4')
        self.SendVal(int(inMinute),'i4')
        self.SendVal(int(inSecond),'i4')
        
    def SetXYZPosition(self,inCaptureIndex,inPositionX,inPositionY,inPositionZ):
        """ Sets the x,y,z position of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inPositionX: float
            The X Position
        inPositionY: float
            The Y Position
        inPositionZ: float
            The Z Position

        Returns
        -------
        none
        """
        self.SendCommand('$SetXYZPosition(CaptureIndex=i4,PositionX=f4,PositionY=f4,PositionZ=f4)')
        self.SendVal(float(inPositionX),'f4')
        self.SendVal(float(inPositionY),'f4')
        self.SendVal(float(inPositionZ),'f4')

    def WriteImagePlaneBuf(self,inCaptureIndex,inTimepointIndex,inZPlaneIndex,inChannelIndex,inNumpyArray):
        """ Writes a z plane of an image from a numpy array

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inTimepointIndex: int
            The time point
        inZPlaneIndex: int
            The z plane number
        inChannelIndex: int
            The channel number. If the channel number (they start at 0) is equal to the number of channels, then a new channel is added
        inNumpyArray: numpy array of u2 (unsigned 16 bit integer)
            The data buffer for the plane to be written

        Returns
        -------
        none
        """
        theBytes = inNumpyArray.tobytes()
        l = len(theBytes)

        self.SendCommand('$WriteImagePlaneBuf(CaptureIndex=i4,TimepointIndex=i4,ZPlaneIndex=i4,ChannelIndex=i4,ByteArray='+str(l)+':b)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inTimepointIndex),'i4')
        self.SendVal(int(inZPlaneIndex),'i4')
        self.SendVal(int(inChannelIndex),'i4')
        self.SendByteArray(theBytes);

        theNum,theVals = self.Recv()
        if( theNum != 1 and theVals[0] != 1):
            raise Exception("WriteImagePlaneBuf: error")
    
    # Mask fucntions

    def ReadMaskPlaneBuf(self,inCaptureIndex,inMaskIndex,inTimepointIndex,inZPlaneIndex):
        """ Reads a z plane of a mask into a numpy array

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inMaskIndex: int
            The nindex of the mask
        inTimepointIndex: int
            The time point
        inZPlaneIndex: int
            The z plane number
        Returns
        -------
        numpy uint16 array 
            The mask is returned as 1D numpy uint16 array

        """

        self.SendCommand('$ReadMaskPlaneBuf(CaptureIndex=i4,MaskIndex=i4,TimepointIndex=i4,ZPlaneIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(int(inMaskIndex),'i4')
        self.SendVal(int(inTimepointIndex),'i4')
        self.SendVal(int(inZPlaneIndex),'i4')

        theNum,theVals = self.Recv()
        return theVals


    def WriteMaskPlaneBuf(self,inCaptureIndex,inMaskName,inTimepointIndex,inZPlaneIndex,inNumpyArray):
        """ Writes a z plane of a mask from a numpy array

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)
        inMaskName: str
            The name of the mask
        inTimepointIndex: int
            The time point
        inZPlaneIndex: int
            The z plane number
        inNumpyArray: numpy array of u2 (unsigned 16 bit integer)

        Returns
        -------
        none
        """
        theBytes = inNumpyArray.tobytes()
        lb = len(theBytes)
        lm = len(inMaskName)

        self.SendCommand('$WriteMaskPlaneBuf(CaptureIndex=i4,MaskName='+str(lm)+':s,TimepointIndex=i4,ZPlaneIndex=i4,ByteArray='+str(lb)+':b)')
        self.SendVal(int(inCaptureIndex),'i4')
        self.SendVal(inMaskName,'s')
        self.SendVal(int(inTimepointIndex),'i4')
        self.SendVal(int(inZPlaneIndex),'i4')
        self.SendByteArray(theBytes);

        theNum,theVals = self.Recv()
        if( theNum != 1 and theVals[0] != 1):
            raise Exception("WriteMaskPlaneBuf: error")


    # Live capture functions

    def StartCapture(self,inScriptName='Default'):
        """ Starts a capture with an optional script name
        Parameters
        ----------
        inScriptName: string
            The script name to load before starting the capture. If blank, the Default script  is loaded

        Returns
        -------
        int
            the capture id. If the capture failed to start, return -1
        """
        l = len(inScriptName)
        self.SendCommand('$StartCapture(ScriptName='+str(l)+':s)')
        self.SendVal(inScriptName,'s')
        theNum,theVals = self.Recv()
        if( theNum != 1 or theVals[0] == -1):
            raise Exception("StartCapture: error")

        return theVals[0]

    def StopCapture(self):
        """ Stops the current capture
        Parameters
        ----------
        inScriptName: int
            The script name to load before starting the capture. If blank, the Default script  is loaded

        Returns
        -------
        int
            0
        """
        self.SendCommand('$StopCapture()')
        theNum,theVals = self.Recv()
        if( theNum != 1 or theVals[0] == -1):
            raise Exception("StopCapture: error")

        return theVals[0]

    def StartStreaming(self):
        """ Starts a streaming acquisition
        Parameters
        ----------

        Returns
        -------
        int
            the capture id. If the streaming failed to start, return -1
        """
        self.SendCommand('$StartStreaming()')
        theNum,theVals = self.Recv()
        if( theNum != 1 or theVals[0] == -1):
            raise Exception("StartStreaming: error")

        return theVals[0]

    def StopStreaming(self):
        """ Starts a streaming acquisition
        Parameters
        ----------

        Returns
        -------
        int
            0
        """
        self.SendCommand('$StopStreaming()')
        theNum,theVals = self.Recv()
        if( theNum != 1 or theVals[0] == -1):
            raise Exception("StopStreaming: error")

        return theVals[0]

    def GetCurrentCaptureId(self,inPositionIndex):
        """ Gets the id of the capture which is currently taking place.

        Parameters
        ----------
        inPositionIndex: int
            The index of the montage position. For non montage capture, use 0

        Returns
        -------
        int
            the capture id
        """
        self.SendCommand('$GetCurrentCaptureId(PositionIndex=i4)')
        self.SendVal(int(inPositionIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetCurrentCaptureId: invalid value")

        return theVals[0]

    def GetCurrentTimepointCaptured(self):
        """ Gets the current timepoint being captured

        Parameters
        ----------

        Returns
        -------
        int
            the index (timepoint) of the current image captured
        """

        self.SendCommand('$GetCurrentTimepointCaptured()')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetCurrentTimepointCaptured: invalid value")

        return theVals[0]


    def GetLastImageCaptured(self,inCaptureIndex):
        """ Gets the index of the last image captured

        Parameters
        ----------
        inCaptureIndex: int
            The index of the capture

        Returns
        -------
        int
            the index (timepoint) of the last image captured
        """

        self.SendCommand('$GetLastImageCaptured(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetLastImageCaptured: invalid value")

        return theVals[0]

    def GetLastImageStreamed(self,inCaptureIndex):
        """ Gets the index of the last image captured in streaming mode

        Parameters
        ----------
        inCaptureIndex: int
            The index of the capture

        Returns
        -------
        int
            the index (timepoint) of the last image captured
        """

        self.SendCommand('$GetLastImageStreamed(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetLastImageStreamed: invalid value")

        return theVals[0]

    def GetCurrentPlaneCaptured(self):
        """ Gets the index of the last plane captured

        Parameters
        ----------

        Returns
        -------
        int
            the index of the plane being captured
        """

        self.SendCommand('$GetCurrentPlaneCaptured()')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetCurrentPlaneCaptured: invalid value")

        return theVals[0]

    def GetLastPlaneCaptured(self,inCaptureIndex):
        """ Gets the index of the last plane captured

        Parameters
        ----------
        inCaptureIndex: int
            The index of the capture

        Returns
        -------
        int
            the index (plane) of the last plane captured
        """

        self.SendCommand('$GetLastPlaneCaptured(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetLastPlaneCaptured: invalid value")

        return theVals[0]


    def GetCurrentChannelCaptured(self):
        """ Gets the index of the current Channel captured

        Parameters
        ----------
        inCaptureIndex: int
            The index of the capture

        Returns
        -------
        int
            thei channel number being captured
        """

        self.SendCommand('$GetCurrentChannelCaptured()')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetCurrentChannelCaptured: invalid value")

        return theVals[0]

    def GetLastChannelCaptured(self,inCaptureIndex):
        """ Gets the index of the last Channel captured

        Parameters
        ----------
        inCaptureIndex: int
            The index of the capture

        Returns
        -------
        int
            the index (plane) of the last plane captured
        """

        self.SendCommand('$GetLastChannelCaptured(CaptureIndex=i4)')
        self.SendVal(int(inCaptureIndex),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetLastChannelCaptured: invalid value")

        return theVals[0]

    def GetCurrentPositionIndexCaptured(self):
        """ Gets the index of the last plane captured

        Parameters
        ----------

        Returns
        -------
        int
            the position index of the current captured image
        """

        self.SendCommand('$GetCurrentPositionIndexCaptured()')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetCurrentPositionIndexCaptured: invalid value")

        return theVals[0]


    def GetCurrentNumPositionsCaptured(self):
        """ Gets the index of the last plane captured

        Parameters
        ----------

        Returns
        -------
        int
            the number of positions in the current experiment bein g captured
        """

        self.SendCommand('$GetCurrentNumPositionsCaptured()')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetCurrentNumPositionsCaptured: invalid value")

        return theVals[0]


    def GetCurrentExperimentCaptured(self):
        """ Gets the index of the last plane captured

        Parameters
        ----------

        Returns
        -------
        int
            the experiment index being captured
        """

        self.SendCommand('$GetCurrentExperimentCaptured()')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetCurrentExperimentCaptured: invalid value")

        return theVals[0]


    def IsCapturing(self):
        """ Checks if there is an active capture

        Parameters
        ----------

        Returns
        -------
        bool
            True if is capturing, false if it is not
        """
        self.SendCommand('$IsCapturing()')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("IsCapturing: failed")
        if(theVals[0] > 0):
            return True
        else:
            return False

    def IsStreaming(self):
        """ Checks if there is an active streaming acquisition

        Parameters
        ----------

        Returns
        -------
        bool
            True if is capturing, false if it is not
        """
        self.SendCommand('$IsStreaming()')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("IsStreaming: failed")
        if(theVals[0] > 0):
            return True
        else:
            return False

    def GetIsHardwareComponentEnabled(self, inComponentID : MicroscopeHardwareComponent):
        """ Checks if the hardware component is enabled

        Parameters
        ----------
        inComponentID: int
            The component ID (0 <= inComponentID <= 46)

        Returns
        -------
        bool
            True if is enabled, false if it is not
        """
        self.SendCommand('$GetIsHardwareComponentEnabled(ComponentIndex=i4)')
        self.SendVal(int(inComponentID.value), 'i4')
        theNum, theVals = self.Recv()
        if (theNum != 1):
            raise Exception("GetIsHardwareComponentEnabled: failed")
        if (theVals[0] > 0):
            return True
        else:
            return False

    def GetHardwareComponentName(self, inComponentID : MicroscopeHardwareComponent):
        """ Returns the device name of a hardware component

        Parameters
        ----------
        inComponentID: MicroscopeHardwareComponent
            The component ID (0 <= inComponentID <= 46)

        Returns
        -------
        list
            Returns the device name of inComponentID. If not enabled returns keyword 'Empty'
        """
        self.SendCommand('$GetHardwareComponentName(ComponentIndex=i4)')
        self.SendVal(int(inComponentID.value),'i4')
        theString = self.Recv()
        return theString

    def GetHardwareComponentMinMax(self, inComponentID : MicroscopeHardwareComponent):
        """ Returns the device minimum and maximum hardware positions

        Parameters
        ----------
        inComponentID: MicroscopeHardwareComponent
            The component ID (0 <= inComponentID <= 46)

        Returns
        -------
        list
            Returns the minimum ([0]) and maximum ([1]) position of device inComponentID
        result
            Returns success (1) or failure (0)
        """
        self.SendCommand('$GetHardwareComponentMinMax(ComponentIndex=i4)')
        self.SendVal(int(inComponentID.value), 'i4')
        theNum, theVals = self.Recv()
        if (theNum != 2):
            raise Exception("GetHardwareComponentMinMax: failed")

        theNum, theResult = self.Recv()
        if (theNum != 1):
            raise Exception("GetHardwareComponentMinMax: failed")

        return theVals, theResult

    def SetHardwareComponentOpen(self, inComponentID : MicroscopeHardwareComponent, inOpen):
        """ Set the open or close position of a hardware device

        Parameters
        ----------
        inComponentID: MicroscopeHardwareComponent
            The component ID (0 <= inComponentID <= 46)
        inOpen: int
            The new position (0 = closed 1 = open)

        Returns
        -------
        bool
            Returns success or failure
        """
        self.SendCommand('$SetHardwareComponentOpen(ComponentIndex=i4,Open=i4)')
        self.SendVal(int(inComponentID.value), 'i4')
        self.SendVal(int(inOpen), 'i4')
        theNum, theVals = self.Recv()
        if (theNum != 1):
            raise Exception("SetHardwareComponentOpen: failed")

        if (theVals[0] > 0):
            return True
        else:
            return False

    def GetHardwareComponentOpen(self, inComponentID : MicroscopeHardwareComponent):
        """ Gets the current position of a hardware device

        Parameters
        ----------
        inComponentID: MicroscopeHardwareComponent
            The component ID (0 <= inComponentID <= 46)

        Returns
        -------
        int
            Returns the current open/close state of device inComponentID (0 = closed 1 = open)
        bool
            Returns success or failure
        """
        self.SendCommand('$GetHardwareComponentOpen(ComponentIndex=i4)')
        self.SendVal(int(inComponentID.value), 'i4')

        theNum,theState = self.Recv()
        if(theNum != 1):
            raise Exception("GetHardwareComponentOpen: invalid state value")

        theNum, theVals = self.Recv()
        if (theNum != 1):
            raise Exception("GetHardwareComponentOpen: failed")

        if (theVals[0] > 0):
            return theState[0], True
        else:
            return theState[0], False

    def SetHardwareComponentPosition(self, inComponentID : MicroscopeHardwareComponent, inPosition):
        """ Set the current position of a hardware device

        Parameters
        ----------
        inComponentID: MicroscopeHardwareComponent
            The component ID (0 <= inComponentID <= 46)
        inPosition: int
            The new position

        Returns
        -------
        bool
            Returns success or failure
        """
        self.SendCommand('$SetHardwareComponentPosition(ComponentIndex=i4,Position=i4)')
        self.SendVal(int(inComponentID.value), 'i4')
        self.SendVal(int(inPosition), 'i4')
        theNum, theVals = self.Recv()
        if (theNum != 1):
            raise Exception("SetHardwareComponentPosition: failed")

        if (theVals[0] > 0):
            return True
        else:
            return False

    def GetHardwareComponentPosition(self, inComponentID : MicroscopeHardwareComponent):
        """ Gets the current position of a hardware device

        Parameters
        ----------
        inComponentID: MicroscopeHardwareComponent
            The component ID (0 <= inComponentID <= 46)

        Returns
        -------
        int
            Returns the current position of device inComponentID
        int
            Returns success (1) or failure (0)
        """
        self.SendCommand('$GetHardwareComponentPosition(ComponentIndex=i4)')
        self.SendVal(int(inComponentID.value), 'i4')
        theNum, theVals = self.Recv()
        if (theNum != 1):
            raise Exception("GetHardwareComponentPosition: failed")

        theNum, theResult = self.Recv()
        if (theNum != 1):
            raise Exception("GetHardwareComponentPosition: failed")

        return theVals[0], theResult

    def SetHardwareComponentLocationMicrons(self, inComponentID : MicroscopeHardwareComponent, inXMicrons, inYMicrons, inZMicrons):
        """ Set the current XYZ position of a hardware device

        Parameters
        ----------
        inComponentID: MicroscopeHardwareComponent
            The component ID (0 <= inComponentID <= 46)
        x: float
            The new x micron position
        y: float
            The new x micron position
        z: float
            The new x micron position

        Returns
        -------
        bool
            Returns success or failure
        """
        try:
            self.SendCommand('$SetHardwareComponentLocationMicrons(ComponentIndex=i4,x=f4,y=f4,z=f4)')
            self.SendVal(int(inComponentID.value), 'i4')
            self.SendVal(float(inXMicrons), 'f4')
            self.SendVal(float(inYMicrons), 'f4')
            self.SendVal(float(inZMicrons), 'f4')

            theNum, theVals = self.Recv()
            if (theNum != 1):
                raise Exception("SetHardwareComponentLocationMicrons: failed")

            if (theVals[0] > 0):
                return True
            else:
                return False
        except:
                return False

    def IncrementHardwareComponentLocationMicrons(self, inComponentID : MicroscopeHardwareComponent, inXMicrons, inYMicrons, inZMicrons):
        """ Increment the current XYZ position of a hardware device

        Parameters
        ----------
        inComponentID: MicroscopeHardwareComponent
            The component ID (0 <= inComponentID <= 46)
        x: float
            The increment x micron position
        y: float
            The increment x micron position
        z: float
            The increment x micron position

        Returns
        -------
        bool
            Returns success or failure
        """
        try:
            self.SendCommand('$IncrementHardwareComponentLocationMicrons(ComponentIndex=i4,x=f4,y=f4,z=f4)')
            self.SendVal(int(inComponentID.value), 'i4')
            self.SendVal(float(inXMicrons), 'f4')
            self.SendVal(float(inYMicrons), 'f4')
            self.SendVal(float(inZMicrons), 'f4')

            theNum, theVals = self.Recv()
            if (theNum != 1):
                raise Exception("IncrementHardwareComponentLocationMicrons: failed")

            if (theVals[0] > 0):
                return True
            else:
                return False
        except:
                return False


    def GetHardwareComponentLocationMicrons(self,inComponentID : MicroscopeHardwareComponent):
        """ Gets the current XYZ location of hardware component inComponentIndex

        Parameters
        ----------
        inComponentID: MicroscopeHardwareComponent
            The component ID (0 <= inComponentID <= 46)

        Returns
        -------
        float
            The X location in um (0 if unsupported)
        float
            The Y location in um (0 if unsupported)
        float
            The Z location in um (0 if unsupported)

        """
        self.SendCommand('$GetHardwareComponentLocationMicrons(ComponentIndex=i4)')
        self.SendVal(int(inComponentID.value),'i4')

        theNum,theX = self.Recv()
        if( theNum != 1):
            raise Exception("GetHardwareComponentLocationMicrons: invalid x value")

        theNum,theY = self.Recv()
        if( theNum != 1):
            raise Exception("GetHardwareComponentLocationMicrons: invalid y value")

        theNum,theZ = self.Recv()
        if( theNum != 1):
            raise Exception("GetHardwareComponentLocationMicrons: invalid z value")

        return theX[0],theY[0],theZ[0]

    def SetVector3ScannerPosition(self, inX_mV, inY_mV, inDisableSpin):
        """ Set the current Vector3 scanner position

        Parameters
        ----------
        inX_mV: int
            The new X position
        inY_mV: int
            The new Y position
        inDisableSpin:
            If true spin TIRF will be disabled

        Returns
        -------
        bool
            Returns success or failure (command will fail if spin TIRF enabled and inDisableSpin is false)
        """
        try:
            self.SendCommand('$SetVector3ScannerPosition(X_mV=i4,Y_mV=i4,DisableSpin=i4)')
            self.SendVal(int(inX_mV), 'i4')
            self.SendVal(int(inY_mV), 'i4')
            self.SendVal(int(inDisableSpin), 'i4')
            theNum, theVals = self.Recv()
            if (theNum != 1):
                raise Exception("SetVector3ScannerPosition: failed")

            if (theVals[0] > 0):
                return True
            else:
                return False
        except:
            return False

    def GetVector3ScannerPosition(self):
        """ Gets the current position of a hardware device

        Parameters
        ----------

        Returns
        -------
        int
            the current X position of stepper motor
        int
            the current Y position of stepper motor
        int
            current spin state (1=spin, 0=not)
        """
        self.SendCommand('$GetVector3ScannerPosition()')
        theNum, theX = self.Recv()
        if (theNum != 1):
            raise Exception("GetVector3ScannerPosition: failed")

        theNum, theY = self.Recv()
        if (theNum != 1):
            raise Exception("GetVector3ScannerPosition: failed")

        theNum, theSpin = self.Recv()
        if (theNum != 1):
            raise Exception("GetVector3ScannerPosition: failed")

        theNum, theResult = self.Recv()
        if (theNum != 1):
             raise Exception("GetVector3ScannerPosition: failed")

        return theX[0], theY[0], theSpin[0]

    def SetVector3StepperPosition(self, inPosition):
        """ Set the current Vector3 stepper motor position

        Parameters
        ----------
        inPosition: int
            The new position

        Returns
        -------
        bool
            Returns success or failure
        """
        try:
            self.SendCommand('$SetVector3StepperPosition(Position=i4)')
            self.SendVal(int(inPosition), 'i4')
            theNum, theVals = self.Recv()
            if (theNum != 1):
                raise Exception("SetVector3StepperPosition: failed")

            if (theVals[0] > 0):
                return True
            else:
                return False
        except:
            return False

    def GetVector3StepperPosition(self):
        """ Gets the current position of a hardware device

        Parameters
        ----------

        Returns
        -------
        int
            Returns the current position of stepper motor
        """
        self.SendCommand('$GetVector3StepperPosition()')
        theNum, theVals = self.Recv()
        if (theNum != 1):
            raise Exception("GetVector3StepperPosition: failed")

        theNum, theResult = self.Recv()
        if (theNum != 1):
            raise Exception("GetVector3StepperPosition: failed")

        return theVals[0]

    def ConfirmFocusWindow(self):
        """ Confirms focus window is open and operational

        Parameters
        ----------

        Returns
        -------
        bool
            Returns True if successful and False if not successful
        """
        self.SendCommand('$ConfirmFocusWindow()')
        theNum, theVals = self.Recv()
        if (theNum != 1):
            raise Exception("ConfirmFocusWindow: failed")

        if (theVals[0] > 0):
            return True
        else:
            return False

    def ClearXYZPoints(self):
        """ Clear all points in XYZ point list

        Parameters
        ----------
       Returns
        -------
        bool
            Returns True if successful and False if not successful
       """

        self.SendCommand('$ClearXYZPoints()')

        theNum, theVals = self.Recv()
        if (theNum != 1):
            raise Exception("ClearXYZPoints: failed")

        if (theVals[0] > 0):
            return True
        else:
            return False

    def GetXYZPointCount(self):
        """ Returns the number of XY points in the XY point list

        Parameters
        ----------
       Returns
        -------
        NumPoints
            Returns the number of XY points in the XY point list
        bool
            Returns True if successful and False if not successful
       """

        self.SendCommand('$GetXYZPointCount()')

        theNum, theNumPoints = self.Recv()
        if (theNum != 1):
            raise Exception("GetXYZPointCount: failed")

        theNum, theVals = self.Recv()
        if (theNum != 1):
            raise Exception("GetXYZPointCount: failed")

        if (theVals[0] > 0):
            return theNumPoints[0], True
        else:
            return theNumPoints[0], False

    def AddXYZPoint(self,inXum,inYum,inZum,inAuxZum=0,inIsAuxZ=False):
        """ Adds a point to the Focus Window XY Tab

        Parameters
        ----------
        inXum: float
            The point X coordinate in microns

        inYum: float
            The point Y coordinate in microns

        inZum: float
            The point Z coordinate in microns

        inAuxZum: float
            The auxiliary Z stage coordinate in microns

        inIsAuxZ: bool
            True if the Auxiliary Z Stage is enabled, False otherwise

       Returns
        -------
            bool
                Returns True if successful and False if not successful

        """

        self.SendCommand('$AddXYZPoint(Xum=f4,Yum=f4,Zum=f4,AuxZum=f4,IsAuxZ=i4)')

        self.SendVal(float(inXum),'f4')
        self.SendVal(float(inYum),'f4')
        self.SendVal(float(inZum),'f4')
        self.SendVal(float(inAuxZum),'f4')
        self.SendVal(int(inIsAuxZ),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("AddXYZPoint: failed")
        if(theVals[0] > 0):
            return True
        else:
            return False


    def GetXYZPointList(self):
        """ Gets a list of all XYZ points in the Focus Window XY Tab

        Parameters
        ----------

        Returns
        -------
        list
            a list of strings . If there is no point list defined in the XY Tab, it returns the keyword 'Empty'
        """
        self.SendCommand('$GetXYZPointList()')

        theStr = self.Recv()

        theList = theStr.split('\n')
        return theList


    def GetMicroscopeState(self, state: MicroscopeStates):
        """ Gets a microscope state
        Parameters
        ----------
        state: an enum from MicroscopeStates,
           for example: GetMicroscopeState(MicroscopeStates.CurrentObjective)

        Returns
        -------
            depends from what is retrieved
            
        """

        self.SendCommand('$GetMicroscopeState(state=i4)')
        self.SendVal(int(state.value),'i4')

        if state == MicroscopeStates.CurrentObjective:
            theStr = self.Recv()
            return theStr
        elif state == MicroscopeStates.CurrentFilter:
            theStr = self.Recv()
            return theStr
        elif state == MicroscopeStates.CurrentMagnification:
            theNum,theVals = self.Recv()
            if( theNum != 1):
                raise Exception("MicroscopeStates.CurrentMagnification: invalid value")
            return theVals[0]
        elif state == MicroscopeStates.CurrentLaserPower:
            theNum,theVals = self.Recv()
            if( theNum != 1):
                raise Exception("MicroscopeStates.CurrentLaserPower: invalid value")
            return theVals[0]
        elif state == MicroscopeStates.CurrentNDPrimary:
            theNum,theVals = self.Recv()
            if( theNum != 1):
                raise Exception("MicroscopeStates.CurrentNDPrimary: invalid value")
            return theVals[0]
            return theStr
        elif state == MicroscopeStates.CurrentNDAux:
            theNum,theVals = self.Recv()
            if( theNum != 1):
                raise Exception("MicroscopeStates.CurrentNDAux: invalid value")
            return theVals[0]
            return theStr
        elif state == MicroscopeStates.CurrentLampVoltage:
            theNum,theVals = self.Recv()
            if( theNum != 1):
                raise Exception("MicroscopeStates.CurrentLampVoltage: invalid value")
            return theVals[0]
        elif state == MicroscopeStates.CurrentFLshutter:
            theNum,theVals = self.Recv()
            if( theNum != 1):
                raise Exception("MicroscopeStates.CurrentFLshutter: invalid value")
            return theVals[0]
        elif state == MicroscopeStates.CurrentBFshutter:
            theNum,theVals = self.Recv()
            if( theNum != 1):
                raise Exception("MicroscopeStates.CurrentBFshutter: invalid value")
            return theVals[0]
        elif state == MicroscopeStates.CurrentAltSource:
            theNum,theVals = self.Recv()
            if( theNum != 1):
                raise Exception("MicroscopeStates.CurrentAltSource: invalid value")
            return theVals[0]
        elif state == MicroscopeStates.CurrentXYstagePosition:
            theNum,theVals = self.Recv()
            if( theNum != 2):
                raise Exception("MicroscopeStates.CurrentXYstagePosition: invalid value")
            return theVals[0],theVals[1]
        elif state == MicroscopeStates.CurrentZstagePosition:
            theNum,theVals = self.Recv()
            if( theNum != 1):
                raise Exception("MicroscopeStates.CurrentZstagePosition: invalid value")
            return theVals[0]
        elif state == MicroscopeStates.CurrentAltZstagePosition:
            theNum,theVals = self.Recv()
            if( theNum != 1):
                raise Exception("MicroscopeStates.CurrentAltZstagePosition: invalid value")
            return theVals[0]
        elif state == MicroscopeStates.CurrentCondenserPrismPosition:
            return 0
        elif state == MicroscopeStates.CurrentVideoOrCameraPosition:
            #returns 0 (Camera) or 1 (Video)
            theNum,theVals = self.Recv()
            if( theNum != 1):
                raise Exception("MicroscopeStates.CurrentVideoOrCameraPosition: invalid value")
            return theVals[0]
        elif state == MicroscopeStates.CurrentCondenserAperture:
            return 0
        elif state == MicroscopeStates.CurrentBin:
            return 0
        elif state == MicroscopeStates.CurrentFilterSet:
            theNum,theVals = self.Recv()
            if( theNum != 1):
                raise Exception("MicroscopeStates.CurrentFilterSet: invalid value")
            return theVals[0]

    def FocusWindowMainSelectBin(self,inStringParam):
        """ Selects a string in the Bin ComboBox of the Focus Window

        Parameters
        ----------
        inStringParam: string
            One of the strings in the Bin ComboBox

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendStringParam('FocusWindowMainSelectBin',inStringParam)

    def FocusWindowMainSelectChannel(self,inStringParam):
        """ Selects a Channel in the Focus Window

        Parameters
        ----------
        inStringParam: string
            The channel name

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendStringParam('FocusWindowMainSelectChannel',inStringParam)

    def FocusWindowMainSelectFilterSet(self,inStringParam):
        """ Selects a string in the Filter Set ComboBox of the Focus Window

        Parameters
        ----------
        inStringParam: string
            One of the strings in the Filter Set ComboBox

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendStringParam('FocusWindowMainSelectFilterSet',inStringParam)

    def FocusWindowMainSelectLaserPower(self,inStringParam):
        """ Selects a string in the Laser Power ComboBox of the Focus Window

        Parameters
        ----------
        inStringParam: string
            One of the strings in the Lser Power ComboBox

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendStringParam('FocusWindowMainSelectLaserPower',inStringParam)

    def FocusWindowMainSelectNDAuxiliary(self,inStringParam):
        """ Selects a string in the Neutral Density Auxiliary ComboBox of the Focus Window

        Parameters
        ----------
        inStringParam: string
            One of the strings in the Neutral Density Auxiliary ComboBox

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendStringParam('FocusWindowMainSelectNDAuxiliary',inStringParam)

    def FocusWindowMainSelectNDPrimary(self,inStringParam):
        """ Selects a string in the Neutral Density Primary ComboBox of the Focus Window

        Parameters
        ----------
        inStringParam: string
            One of the strings in the Neutral Density Primary ComboBox

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendStringParam('FocusWindowMainSelectNDPrimary',inStringParam)

    def FocusWindowMainSetAltClose(self):
        """ Sets the Open Alt/Close Alt button to Close in the Focus Window

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """
        return self.SendNullParam('FocusWindowMainSetAltClose');

    def FocusWindowMainSetAltOpen(self):
        """ Set the Open Alt/Close Alt button to Open in the Focus Window

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendNullParam('FocusWindowMainSetAltOpen');

    def FocusWindowMainSetBrightClose(self):
        """ Sets the Open Bright/Close Bright button to Close in the Focus Window

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendNullParam('FocusWindowMainSetBrightClose');

    def FocusWindowMainSetBrightOpen(self):
        """ Set the Open Bright/Close Bright button to Open in the Focus Window

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendNullParam('FocusWindowMainSetBrightOpen');

    def FocusWindowMainSetExposure(self,inIntParam):
        """ Sets the Exposure value in the Focus Window

        Parameters
        ----------
        inIntParam: int
            The Exposure value

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """


        return self.SendIntParam('FocusWindowMainSetExposure',inIntParam)

    def FocusWindowMainSetFluorClose(self):
        """ Sets the Open Fluor/Close Fluor button to Close in the Focus Window

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendNullParam('FocusWindowMainSetFluorClose');

    def FocusWindowMainSetFluorOpen(self):
        """ Sets the Open Fluor/Close Fluor button to Open in the Focus Window

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendNullParam('FocusWindowMainSetFluorOpen');

    def FocusWindowMainSetLive(self):
        """ Sets the Live/Stop button to Live in the Focus Window

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendNullParam('FocusWindowMainSetLive');

    def FocusWindowMainSetSnap(self):
        """ Snaps an image from the Live Window of the Focus Window

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """


        return self.SendNullParam('FocusWindowMainSetSnap');

    def FocusWindowMainSetStop(self):
        """ Sets the Live/Stop button to Stop in the Focus Window

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendNullParam('FocusWindowMainSetStop');

    def FocusWindowMainMoveX(self,inFloatParam):
        """ Moves the XY stage in the X direction in the Focus Window

        Parameters
        ----------
        inFloatParam: float
            The movement in microns in the X direction

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendFloatParam('FocusWindowMainMoveX',inFloatParam)

    def FocusWindowMainMoveY(self,inFloatParam):
        """ Moves the XY stage in the Y direction in the Focus Window

        Parameters
        ----------
        inFloatParam: float
            The movement in microns in the Y direction

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendFloatParam('FocusWindowMainMoveY',inFloatParam)

    def FocusWindowMainSelectZStage(self,inStringParam):
        """ Selects a string in the Z Stage ComboBox of the Focus Window

        Parameters
        ----------
        inStringParam: string
            One of the strings in the Z Stage ComboBox

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendStringParam('FocusWindowMainSelectZStage',inStringParam)

    def FocusWindowMainMoveZPrimary(self,inFloatParam):
        """ Moves the Z primary stage in the Z direction in the Focus Window

        Parameters
        ----------
        inFloatParam: float
            The movement in microns of the primary stage in the Z direction

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendFloatParam('FocusWindowMainMoveZPrimary',inFloatParam)

    def FocusWindowMainMoveZAuxilary(self,inFloatParam):
        """ Moves the Z auxiliary stage in the Z direction in the Focus Window

        Parameters
        ----------
        inFloatParam: float
            The movement in microns of the auxiliary stage in the Z direction

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendFloatParam('FocusWindowMainMoveZAuxilary',inFloatParam)

    def FocusWindowScopeSelectCameraOrVideo(self,inIntParam):
        """ Selects the Camera or the Video button in the Scope tab of the Focus Window

        Parameters
        ----------
        inIntParam: int
            The value of 0 selects Camera
            The value of 1 selects Video

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendIntParam('FocusWindowScopeSelectCameraOrVideo',inIntParam)

    def FocusWindowScopeSelectCondenserPosition(self,inStringParam):
        """ Selects a string in the Condenser Position ComboBox of the Scope tab of the Focus Window

        Parameters
        ----------
        inStringParam: string
            One of the strings in the Condenser Position ComboBox

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendStringParam('FocusWindowScopeSelectCondenserPosition',inStringParam)

    def FocusWindowScopeSelectEmissionSelection(self,inIntParam):
        """ Selects the 100% Camera or the 50%-50% or 100% Eyes button in the Scope tab of the Focus Window

        Parameters
        ----------
        inIntParam: int
            The value of 0 selects 100% Camera
            The value of 1 selects 50%-50%
            The value of 2 selects 100% Eyes

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """


        return self.SendIntParam('FocusWindowScopeSelectEmissionSelection',inIntParam)

    def FocusWindowScopeSelectMagnificationChanger(self,inStringParam):
        """ Selects a string in the Magnification Changer ComboBox of the Scope tab of the Focus Window

        Parameters
        ----------
        inStringParam: string
            One of the strings in the Magnification Changer ComboBox

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendStringParam('FocusWindowScopeSelectMagnificationChanger',inStringParam)

    def FocusWindowScopeSelectObjective(self,inStringParam):
        """ Selects one of the Objectives button in the Scope tab of the Focus Window. This function causes SlideBook to open an information popup

        Parameters
        ----------
        inStringParam: string
            The name of the Objective to select


        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendStringParam('FocusWindowScopeSelectObjective',inStringParam)

    def FocusWindowScopeSetLampVoltage(self,inIntParam):
        """ Sets the Lamp Voltage in the Scope tab of the Focus Window

        Parameters
        ----------
        inIntParam: int
            The voltage value

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendIntParam('FocusWindowScopeSetLampVoltage',inIntParam)

    def FocusWindowScopeSetCondenserAperture(self,inIntParam):
        """ Sets the Condenser Aperture in the Scope tab of the Focus Window

        Parameters
        ----------
        inIntParam: int
            The condenser aperture value

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendIntParam('FocusWindowScopeSetCondenserAperture',inIntParam)

    def FocusWindowStreamSetNumberFrames(self,inIntParam):
        """ Sets the Number of Frames to capture in the Stream tab of the Focus Window

        Parameters
        ----------
        inIntParam: int
            The number of frames to capture

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """


        return self.SendIntParam('FocusWindowStreamSetNumberFrames',inIntParam)

    def FocusWindowStreamSetNumberFramesToAverage(self,inStringParam):
        """ Selects a string in the Number of frames to average ComboBox in the Stream tab of the Focus Window

        Parameters
        ----------
        inStringParam: string
            One of the strings in the Number of frames to average ComboBox

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendStringParam('FocusWindowStreamSetNumberFramesToAverage',inStringParam)

    def FocusWindowSupportsARCSliceTIRF(self):
        """ Check if Arc/Slice TIRF is supported
        Parameters
        ----------
        Returns
        -------
        bool
            Returns supported
        """

        try:
            self.SendCommand('$FocusWindowSupportsARCSliceTIRF()')
            theNum, theVals = self.Recv()
            if (theNum != 1):
                raise Exception("FocusWindowSupportsARCSliceTIRF: failed")

            if (theVals[0] > 0):
                return True
            else:
                return False

        except:
            return False

    def FocusWindowSetARCSliceTIRFParameters(self, Position, Arcs, Slices, Save):
        """ Set the current arc / time slice parameters for TIRF filter Position

        Parameters
        ----------
        Position: int
            The filter position (0-20)
        Arcs: str
           Comma-separated angles denoting start and stop angle (0.1 degrees) pairs. 0-3600 is a full circle.
           450,900,1800,3600 defines two arc segments: 45-90 and then 180 to 360.
           Minimum arc length is one-tenth degree.
        Slices: str
            Comma-separated list of filters to be concatenated together to create a virtual time-sliced TIRF channel.
            Can include any number of specified TIRF channels (including the current position) and will use the duration
            of Position (the specified filter) to create time-slice TIRF illumination.
        Save: int
            save as default settings (0=false 1=true)

        Returns
        -------
        bool
            Returns success or failure
        """
        try:
            l = len(Arcs)
            m = len(Slices)


            self.SendCommand('$FocusWindowSetARCSliceTIRFParameters(Position=i4,ArcInfo='+str(l)+':s,SliceInfo='+str(m)+':s,Save=i4)')
            self.SendVal(int(Position), 'i4')
            self.SendVal(Arcs, 's')
            self.SendVal(Slices, 's')
            self.SendVal(int(Save), 'i4')

            theNum, theVals = self.Recv()
            if (theNum != 1):
                raise Exception("FocusWindowSetTIRFParameters: failed")

            if (theVals[0] > 0):
                return True
            else:
                return False

        except:
            return False

    def FocusWindowGetARCSliceTIRFParameters(self, Position):
        """ Gets the current arc / time-slice TIRF parameters for filter Position

        Parameters
        ----------
        Position: int
            The filter position (0-20)

        Returns
        -------
        Arcs: int
           arcs (see FocusWindowSetARCSliceTIRFParameters for parameter format)
        Slices: int
            slices (see FocusWindowSetARCSliceTIRFParameters for parameter format)
        int
            Returns success or failure
        """

        self.SendCommand('$FocusWindowGetARCSliceTIRFParameters(Position=i4)')
        self.SendVal(int(Position), 'i4')

        arcs = self.Recv()

        slices = self.Recv()

        theNum, result = self.Recv()
        if (theNum != 1):
            raise Exception("GetHardwareComponentLocationMicrons: invalid y value")

        return arcs, slices, result[0]

    def FocusWindowSetTIRFParameters(self, Position, Radius_mV, X_mV, Y_mV, Duration_ms, MotorPos, MotorEnable,
                                     SpinEnable, Save):
        """ Set the current parameters for TIRF filter Position

        Parameters
        ----------
        Position: int
            The filter position (0-20)
        radius: int
           spin radius (mV)
        x: int
            x center (mV)
        y: int
            y center (mV)
        duration: float
            spin duration (ms)
        motor pos: int
           stepper position
        motor enable: int
            enable stepper (0=false 1=true)
        spin enable: int
            enable spin (0=false 1=true)
        inSave: int
            save as default settings (0=false 1=true)

        Returns
        -------
        bool
            Returns success or failure
        """
        try:
            self.SendCommand('$FocusWindowSetTIRFParameters(Position=i4,Radius_mV=i4,X_mV=i4,Y_mV=i4,Duration_ms=f4,MotorPos=i4,MotorEnable=i4,SpinEnable=i4,Save=i4)')
            self.SendVal(int(Position), 'i4')
            self.SendVal(int(Radius_mV), 'i4')
            self.SendVal(int(X_mV), 'i4')
            self.SendVal(int(Y_mV), 'i4')
            self.SendVal(float(Duration_ms), 'f4')
            self.SendVal(int(MotorPos), 'i4')
            self.SendVal(int(MotorEnable), 'i4')
            self.SendVal(int(SpinEnable), 'i4')
            self.SendVal(int(Save), 'i4')

            theNum, theVals = self.Recv()
            if (theNum != 1):
                raise Exception("FocusWindowSetTIRFParameters: failed")

            if (theVals[0] > 0):
                return True
            else:
                return False

        except:
            return False


    def FocusWindowGetTIRFParameters(self, Position):
        """ Gets the current TIRF parameters for filter Position

        Parameters
        ----------
        Position: int
            The filter position (0-20)

        Returns
        -------
        radius: int
           spin radius (mV)
        x: int
            x center (mV)
        y: int
            y center (mV)
        duration: float
            spin duration (ms)
        motor pos: int
           stepper position
        motor enable: int
            enable stepper (0=false 1=true)
        spin enable: int
            enable spin (0=false 1=true)
        int
            1 if is succesful, 0 otherwise
        """

        self.SendCommand('$FocusWindowGetTIRFParameters(Position=i4)')
        self.SendVal(int(Position), 'i4')

        theNum, Radius_mV = self.Recv()
        if (theNum != 1):
            raise Exception("GetHardwareComponentLocationMicrons: invalid radius value")

        theNum, X_mV = self.Recv()
        if (theNum != 1):
            raise Exception("GetHardwareComponentLocationMicrons: invalid x value")

        theNum, Y_mV = self.Recv()
        if (theNum != 1):
            raise Exception("GetHardwareComponentLocationMicrons: invalid y value")

        theNum, Duration_ms = self.Recv()
        if (theNum != 1):
            raise Exception("GetHardwareComponentLocationMicrons: invalid duration value")

        theNum, MotorPos = self.Recv()
        if (theNum != 1):
            raise Exception("GetHardwareComponentLocationMicrons: invalid motor pos value")

        theNum, MotorEnable = self.Recv()
        if (theNum != 1):
            raise Exception("GetHardwareComponentLocationMicrons: invalid motor enable value")

        theNum, SpinEnable = self.Recv()
        if (theNum != 1):
            raise Exception("GetHardwareComponentLocationMicrons: invalid spin enable value")

        return Radius_mV[0], X_mV[0], Y_mV[0], Duration_ms[0], MotorPos[0], MotorEnable[0], SpinEnable[0]

    def LiveWindowAddRectangleRegion(self,inWindowIndex,inX,inY,inWidth,inHeight,inIsStimulation=False):
        """ Adds a rectangular region the a given Live Window

        Parameters
        ----------
        inWindowIndex: int
            The live window index
        inXum: int
            The rectangle X left corner in pixels
        inYum: int
            The rectangle Y top corner in pixels
        inWidth: int
            The rectangle width in pixels
        inHeight:int
            The rectangle height in pixels
        inIsStimulation: bool
            True if is a stimulation region, False otherwise
        """

        self.SendCommand('$LiveWindowAddRectangleRegion(WindowIndex=i4,X=i4,Y=i4,Width=i4,Height=i4,IsStimulation=i4)')

        self.SendVal(int(inWindowIndex),'i4')
        self.SendVal(int(inX),'i4')
        self.SendVal(int(inY),'i4')
        self.SendVal(int(inWidth),'i4')
        self.SendVal(int(inHeight),'i4')
        self.SendVal(int(inIsStimulation),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("LiveWindowAddRectangleRegion: failed")
        if(theVals[0] > 0):
            return True
        else:
            return False

    def LiveWindowAddEllipseRegion(self,inWindowIndex,inX,inY,inWidth,inHeight,inIsStimulation=False):
        """ Adds a elliptical region the a given Live Window

        Parameters
        ----------
        inWindowIndex: int
            The live window index
        inXum: int
            The ellipse X left corner in pixels
        inYum: int
            The ellipse Y top corner in pixels
        inWidth: int
            The ellipse width in pixels
        inHeight:int 
            The ellipse height in pixels
        inIsStimulation: bool
            True if is a stimulation region, False otherwise
        """

        self.SendCommand('$LiveWindowAddEllipseRegion(WindowIndex=i4,X=i4,Y=i4,Width=i4,Height=i4,IsStimulation=i4)')

        self.SendVal(int(inWindowIndex),'i4')
        self.SendVal(int(inX),'i4')
        self.SendVal(int(inY),'i4')
        self.SendVal(int(inWidth),'i4')
        self.SendVal(int(inHeight),'i4')
        self.SendVal(int(inIsStimulation),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("LiveWindowAddEllipseRegion: failed")
        if(theVals[0] > 0):
            return True
        else:
            return False

    def LiveWindowAddLineRegion(self,inWindowIndex,inX,inY,inWidth,inHeight,inIsStimulation=False):
        """ Adds a line region the a given Live Window

        Parameters
        ----------
        inWindowIndex: int
            The live window index
        inXum: int
            The line X first point in pixels
        inYum: int
            The line Y first point in pixels
        inWidth: int
            The line X second point in pixels
        inHeight:int 
            The line Y second point in pixels
        inIsStimulation: bool
            True if is a stimulation region, False otherwise
        """

        self.SendCommand('$LiveWindowAddLineRegion(WindowIndex=i4,X=i4,Y=i4,Width=i4,Height=i4,IsStimulation=i4)')

        self.SendVal(int(inWindowIndex),'i4')
        self.SendVal(int(inX),'i4')
        self.SendVal(int(inY),'i4')
        self.SendVal(int(inWidth),'i4')
        self.SendVal(int(inHeight),'i4')
        self.SendVal(int(inIsStimulation),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("LiveWindowAddLineRegion: failed")
        if(theVals[0] > 0):
            return True
        else:
            return False


    def LiveWindowAddPolygonRegion(self,inWindowIndex,inXYPointList,inIsStimulation=False):
        """ Adds a rectangular region the a given Live Window

        Parameters
        ----------
        inWindowIndex: int
            The live window index
        inXYPointList: list of int
            a list of the polygon corners xy pixel coordinates
        inIsStimulation: bool
            True if is a stimulation region, False otherwise
        """
        theNumPairs = len(inXYPointList) / 2
        theB = np.uint32(inXYPointList)
        theBytes = theB.tobytes();
        l = len(theBytes)

        self.SendCommand('$LiveWindowAddPolygonRegion(WindowIndex=i4,NumPairs=i4,XYPointList='+str(l)+':b,IsStimulation=i4)')

        self.SendVal(int(inWindowIndex),'i4')
        self.SendVal(int(theNumPairs),'i4')
        self.SendByteArray(theBytes);
        self.SendVal(int(inIsStimulation),'i4')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("LiveWindowAddRectangleRegion: failed")
        if(theVals[0] > 0):
            return True
        else:
            return False

    # FOCUS SURFACE section
    def FocusSurface_Open(self,inIntParam=0):
        """ Open the Focus Surface window

        Parameters
        ----------
        inIntParam: int
            Flag: 0 to open for XY tab, 1 to open for MultiWell Tab

        Returns
        -------
        int
            1 if is succesful, 0 otherwise
        
        """

        return self.SendIntParam('FocusSurface_Open',inIntParam)


    def FocusSurface_AddCalibrationPoint(self,inXum,inYum,inZum,inAuxZum=0,inIsAuxZ=False):
        """ Adds a calibration point to the Focus Surface

        Parameters
        ----------
        inXum: float
            The point X coordinate in microns

        inYum: float
            The point Y coordinate in microns

        inZum: float
            The point Z coordinate in microns

        inAuxZum: float
            The auxiliary Z stage coordinate in microns

        inIsAuxZ: bool
            True if the Auxiliary Z Stage is enabled, False otherwise

        Returns
        -------
            bool
                Returns True if successful and False if not successful

        """

        #first move stage, then call the AddCalibrationPoint
        res = self.SetHardwareComponentLocationMicrons(MicroscopeHardwareComponent.XYStage,inXum,inYum,0)
        if(res == 0):
            return False
        if(not inIsAuxZ):
            res = self.SetHardwareComponentLocationMicrons(MicroscopeHardwareComponent.ZStage,0,0,inZum)
            if(res == 0):
                return False
        else:
            res = res = self.SetHardwareComponentLocationMicrons(MicroscopeHardwareComponent.AuxZStage,0,0,inAuxZum);
            if(res == 0):
                return False

        self.SendCommand('$FocusSurface_AddCalibrationPoint()')

        theNum,theVals = self.Recv()

        if( theNum != 1):
            raise Exception("FocusSurface_AddCalibrationPoint: failed")
        if(theVals[0] > 0):
            return True
        else:
            return False

    def FocusSurface_ClearCalibrationPoints(self):
        """ Clear all calibration point of the Focus Surface

        Parameters
        ----------

        Returns
        -------
            bool
                Returns True if successful and False if not successful

        """

        self.SendCommand('$FocusSurface_ClearCalibrationPoints()')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("FocusSurface_ClearCalibrationPoints: failed")
        if(theVals[0] > 0):
            return True
        else:
            return False

    def FocusSurface_FitSurface(self):
        """ Fits a surface in the Focus Surface window

        Parameters
        ----------

        Returns
        -------
            bool
                Returns True if successful and False if not successful

        """

        self.SendCommand('$FocusSurface_FitSurface()')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("FocusSurface_FitSurface: failed")
        if(theVals[0] > 0):
            return True
        else:
            return False


    def FocusSurface_IsSurfaceFit(self):
        """ Fits a surface in the Focus Surface window

        Parameters
        ----------

        Returns
        -------
            bool
                Returns True if successful and False if not successful

        """

        self.SendCommand('$FocusSurface_IsSurfaceFit()')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("FocusSurface_IsSurfaceFit: failed")
        if(theVals[0] > 0):
            return True
        else:
            return False

    def FocusSurface_FitPoint(self,inXum,inYum):
        """ Fits a point with the Focus Surface

        Parameters
        ----------
        inXum: float
            The point X coordinate in microns

        inYum: float
            The point Y coordinate in microns

        Returns
        -------
            bool
                Returns True if successful and False if not successful
            float
                The Z1 fitted coordinate
            float
                The Z2 fitted coordinate

        """
        self.SendCommand('$FocusSurface_FitPoint(XCoord=f4,YCoord=f4)')
        self.SendVal(float(inXum), 'f4')
        self.SendVal(float(inYum), 'f4')
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("FocusSurface_IsSurfaceFit: failed")
        return theVals[0];

    def RunSavedScript(self,inStringParam):
        """ Runs a script file
        Parameters
        ----------
        inStringParam: string
            The pathname of the script file

        Returns
        -------
            bool
                Returns True if successful and False if not successful
        """

        theRes = self.SendStringParam('RunSavedScript',inStringParam)

        if(theRes > 0):
            return True
        else:
            return False

    def RunUserScript(self,inStringParam):
        """ Runs a script file
        Parameters
        ----------
        inStringParam: string
            The multiline script to be run. Lines are sparated by a \n  or a \n\r

        Returns
        -------
            bool
                Returns True if successful and False if not successful
        """

        theRes = self.SendStringParam('RunUserScript',inStringParam)

        if(theRes > 0):
            return True
        else:
            return False


    def GetXYZSavedExperimentName(self,inIndex):
        """ Gets the name of a saved experiment
        Parameters
        ----------
        inIndex: int
            the experiment index
        Returns
        ----------
            string, bool
                Returns the experiment name as a string and true/false for success (bounds checking)
                If the experiment is not set, the returned string is 'Default'
        """

        self.SendCommand('$GetXYZSavedExperimentName(Index=i4)')
        self.SendVal(int(inIndex),'i4')
        theStr = self.Recv()
        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("GetXYZSavedExperimentName: failed")
        if(theVals[0] > 0):
            return theStr,True
        else:
            return 'Default',False

        
    def SetXYZSavedExperimentName(self,inIndex,inExperimentName):
        """ Sets the name of an experiment at given index in the 6D tab, experiment list
        Parameters
        ----------
        inIndex: int
            the experiment index
        string
            the experiment name
        Returns
        ----------
        bool
            Return True/False based on bounds checking AND confirmation that the ExperimentName exists
        """

        l = len(inExperimentName)
        self.SendCommand('$SetXYZSavedExperimentName(Index=i4,ExperimentName='+str(l)+':s)')
        self.SendVal(int(inIndex),'i4')
        self.SendVal(inExperimentName,'s')

        theNum,theVals = self.Recv()
        if( theNum != 1):
            raise Exception("SetXYZSavedExperimentName: failed")
        if(theVals[0] > 0):
            return True
        else:
            return False

        
