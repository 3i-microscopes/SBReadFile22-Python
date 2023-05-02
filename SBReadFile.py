__copyright__  = "Copyright (c) 2022, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."

from DataLoader import *
from CImageGroup import *

class SBReadFile(object):
    
    """ A Class to Read Slide Book Format 7 Files """

    # All access functions as in SBReadFile.h

    def Open(self,inPath):
        """Open a SlideBook file and loads the Metadata

        Parameters
        ----------
        inPath : str
            The path of the SlideBook file to open
        Returns
        -------
        bool
            true if file opeend succesfully, else false
        """

        self.mDL = DataLoader(inPath)
        res = self.mDL.LoadMetadata()
        return res


    def GetNumCaptures(self):
        """ Gets the number of captures (image groups) in the file

        Returns
        -------
        int
            The number of captures
        """

        return self.mDL.GetNumCaptures()

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetNumPositions()

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetNumColumns()

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


        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetNumRows()

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



        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetNumPlanes()

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetNumTimepoints()

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetNumChannels()

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


        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetExposureTime(inChannelIndex)

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        theXSize = theImageGroup.GetVoxelSize()
        theYSize = theXSize
        theZSize = theImageGroup.GetInterplaneSpacing()

        return theXSize,theYSize,theZSize

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetXPosition(inPositionIndex)

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


        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetYPosition(inPositionIndex)

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetZPosition(inPositionIndex,inZPlaneIndex)

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return 0  #TODO

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return 0  #TODO

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetElapsedTime(inTimepointIndex)

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetChannelName(inChannelIndex)

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetLensName()

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetMagnification()

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetImageName()

    def GetImageComments(self,inCaptureIndex):
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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetImageComments()

    def GetCaptureDate(self,inCaptureIndex):
        """ Gets the date of acquisition of an image group

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        -------
        int
            The year
        int
            The month
        int
            The day
        int
            The hour
        int
            The minute
        int
            The second
        """

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetCaptureDate()

    def GetThumbnail(self,inCaptureIndex):
        """ Gets the thumbnail

        Parameters
        ----------
        inCaptureIndex: int
            The index of the image group. Must be in range(0,number of captures)

        Returns
        numpy uint32 array 
            The thumbnail is returned as list of 1024 integers values. Each value is a 32 bit color value. The thumbnail is 32x32 pixels ordered by rows.
        """

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetThumbnail()

    def ReadImagePlaneBuf(self,inCaptureIndex,inPositionIndex,inTimepointIndex,inZPlaneIndex,inChannelIndex,inAs2D=False):
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
        inAs2D: bool, optional
            if True, returna 2D array, otheiws (default) returna 1D array

        Returns
        -------
        numpy uint16 array 
            The image is returned as 1D numpy uint16 array if inAs2D is false
            Otherwise is returned as a 2D array of (NumRows,NumColumns)

        """

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        return self.mDL.ReadPlane(inCaptureIndex,  inPositionIndex, inTimepointIndex, inZPlaneIndex, inChannelIndex,inAs2D)

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetAuxDataXMLDescriptor(inChannelIndex)

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
        
        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetAuxDataNumElements(inChannelIndex)

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetAuxFloatData(inChannelIndex)

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetAuxDoubleData(inChannelIndex)

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetAuxSInt32Data(inChannelIndex)

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetAuxSInt64Data(inChannelIndex)

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

        self.mDL.CheckCaptureIndex(inCaptureIndex)
        theImageGroup = self.mDL.GetImageGroup(inCaptureIndex)
        return theImageGroup.GetAuxSerializedData(inChannelIndex,inElementIndex)

