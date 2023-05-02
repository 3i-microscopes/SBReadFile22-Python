__copyright__  = "Copyright (c) 2022, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."

from BaseDecoder import BaseDecoder
from CMetadataLib import *
from CNpyHeader import *
from CSBFile70 import *
from CCompressionBase import *
from CSBPoint import *
import os
import yaml
import numpy as np

class CMaskPositions(object):
    mCompressedSizes = []
    mFileOffsets = []

class CAnnotations(object):
    mCubeAnnotationList = []
    mBaseAnnotationList = []
    mFRAPRegionAnnotationList = []
    mUnknownAnnotationList = []

class CBaseAuxData(object):
    def __init__(self):
        mTableHeaderRecord = CDataTableHeaderRecord70()
        mXmlDescriptor = str()
    
class CAuxFloatData(CBaseAuxData):
    def __init__(self):
        super().__init__()
        mFloatData = []

class CAuxDoubleData(CBaseAuxData):
    def __init__(self):
        super().__init__()
        mDoubleData = []

class CAuxSInt32Data(CBaseAuxData):
    def __init__(self):
        super().__init__()
        mIntegerData = []

class CAuxSInt64Data(CBaseAuxData):
    def __init__(self):
        super().__init__()
        mLongData = []

class CAuxXmlData(CBaseAuxData):
    def __init__(self):
        super().__init__()
        mXmlData = str()

class CImageGroup(BaseDecoder):
    def __init__(self, inFile, inImageTitle):
        super(CImageGroup, self).__init__()
        self.mImageDataList = []
        self.mMaskPosList = []
        self.mAnnotationList = []
        self.mImageRecord = CImageRecord70()
        self.mChannelRecordList = []
        self.mRemapChannelLUTList = []
        self.mAlignManipRecordList = []
        self.mRatioManipRecordList = []
        self.mFRETManipRecList = []
        self.mRemapManipRecList = []
        self.mHistogramRecordList = []
        self.mMaskRecordList = []
        self.mElapsedTimes = []
        self.mSAPositionList = []
        self.mStagePositions = []
        self.mAuxFloatDataList = []
        self.mAuxDoubleDataList = []
        self.mAuxSInt32DataList = []
        self.mAuxSInt64DataList = []
        self.mAuxXmlDataList = []
        self.mNpyHeader = None
        self.mFile = inFile
        self.mImageTitle = inImageTitle
        self.mSingleTimepointFile = False
        self.mCompressor = CCompressionBase()
        self.mCompressionFlag = self.mCompressor.eCompressionNone
        self.mDebugPrint = False
        self.mLastTimepoint = -1;
        self.mLastChannel = -1;

    def IsSFMT(self,inPath):
        theStream = open(inPath,"rb")
        theNpyHeader = CNpyHeader()
        theRes = theNpyHeader.ParseNpyHeader(theStream)
        self.mSingleTimepointFile = False
        if not theRes:
            return False,0
        if len(theNpyHeader.mShape) == 3:
            theNumTimepoints = theNpyHeader.mShape[0]
            theRes = True
            self.mSingleTimepointFile = True
            if theNumTimepoints == 0:
                theRes = False
                self.mSingleTimepointFile = False
            return theRes, theNumTimepoints
        return False,0


    def CountImageDataFiles(self):
        theImageFileNames = self.mFile.GetListOfImageDataFiles(self.mImageTitle)
        if self.mDebugPrint:
            print ("theImageFileNames length: " , len(theImageFileNames))
            print ("CountImageDataFiles: mImageRecord.mNumChannels " , self.mImageRecord.mNumChannels)
            print ("CountImageDataFiles: mImageRecord.mNumTimepoints " , self.mImageRecord.mNumTimepoints)
        if len(theImageFileNames) == self.mImageRecord.mNumChannels * self.mImageRecord.mNumTimepoints:
            if not self.mImageRecord.mNumPlanes == 1:
                # all in order
                return True

        #check for single file containing multi time points
        if len(theImageFileNames) == self.mImageRecord.mNumChannels and self.mImageRecord.mNumPlanes == 1:
            theNumTimepoints = 0
            for theImageFile in theImageFileNames:
                theShapeTP = 0
                (theRes,theShapeTP) =  self.IsSFMT(theImageFile)
                if not theRes:
                    continue
                if theShapeTP <= 0:
                    continue
                # we are using min in case a channel has less timepoints than another one (crashed between channels)
                if theNumTimepoints < theShapeTP:
                    theNumTimepoints = theShapeTP
            if theNumTimepoints == 0:
                theNumTimepoints = 1
            self.mImageRecord.mNumTimepoints = theNumTimepoints
            return True
        # end of check for single file containing multi time points

        #discrepancy

        theMaxChannel = 0
        theMaxTimepoint = 0
        for theImageFile in theImageFileNames:
            theChannel = self.mFile.GetChannelIndexOfPath(theImageFile)
            theTimepoint = self.mFile.GetTimepointOfPath(theImageFile)

            theMaxChannel = max(theMaxChannel, theChannel + 1)
            theMaxTimepoint = max(theMaxTimepoint, theTimepoint + 1)

        if self.mDebugPrint:
            print ("CountImageDataFiles: theMaxChannel + theMaxTimepoint " , theMaxChannel , " " , theMaxTimepoint)
        if theMaxChannel == 0 or theMaxTimepoint == 0:
            print ("CountImageDataFiles: theMaxChannel + theMaxTimepoint " , theMaxChannel , theMaxTimepoint)
            return False
        self.mImageRecord.mNumTimepoints = theMaxTimepoint
        self.mImageRecord.mNumChannels = theMaxChannel
        self.mImageDataList = []
        theTimepoint = 0
        while theTimepoint < self.mImageRecord.mNumTimepoints:
            self.mImageDataList.append(CImageData())
            theTimepoint += 1
        if self.mDebugPrint:
            print ("CountImageDataFiles: mImageDataList.length " , len(self.mImageDataList))
        return True

    def LoadImageRecord(self):
        try:
            self.mImageRecord = CImageRecord70()
            thePath = self.mFile.GetImageGroupDirectory(self.mImageTitle) + os.sep +  self.mFile.kImageRecordFilename
            inputStream = open(thePath,"r")
            theNode = yaml.compose(inputStream)
            theLastIndex = self.mImageRecord.Decode(theNode)
            if self.mDebugPrint:
                print ("LoadImageRecord: theLastIndex " , theLastIndex)
            if not self.CountImageDataFiles():
                print ("CountImageDataFiles: Did not succeed ")
                return False
            if self.mDebugPrint:
                print ("CountImageDataFiles: OK ")
        except: 
            print ("LoadImageRecord: Did not succeed ")
        return True

    def LoadChannelRecord(self):
        try:
            thePath = self.mFile.GetImageGroupDirectory(self.mImageTitle) + os.sep +  self.mFile.kChannelRecordFilename
            inputStream = open(thePath,"r")
            theNode = yaml.compose(inputStream)

            self.mChannelRecordList = []
            self.mRemapChannelLUTList = []
            self.mAlignManipRecordList = []
            self.mRatioManipRecordList = []
            self.mFRETManipRecList = []
            self.mRemapManipRecList = []
            self.mHistogramRecordList = []
            theLastIndex = 0
            for theChannel in range(self.mImageRecord.mNumChannels):
                theChannelRecord = CChannelRecord70()
                self.mChannelRecordList.append(theChannelRecord)

                theRemapChannelLUT = CRemapChannelLUT70()
                theAlignManipRecord70 =  CAlignManipRecord70()  
                theRatioManipRecord70 =  CRatioManipRecord70()
                theFRETManipRec70 =  CFRETManipRecord70()
                theRemapManipRec70 =  CRemapManipRecord70()
                theHistogramRecord70 =  CHistogramRecord70()

                theLastIndex = theChannelRecord.Decode(theNode, theLastIndex)
                if self.mDebugPrint:
                    print ("theLastIndex: " , theLastIndex)
                while True:
                    theStr, theInt = super().FindNextClass(theNode, theLastIndex)
                    if theInt >= 0:
                        if theStr == theChannelRecord.GetSBClassName():
                            theLastIndex = theInt
                            break
                        elif theStr == theRemapChannelLUT.GetSBClassName():
                            theLastIndex = theRemapChannelLUT.Decode(theNode, theInt)
                            self.mRemapChannelLUTList.append(theRemapChannelLUT)
                        elif theStr == theAlignManipRecord70.GetSBClassName():
                            theLastIndex = theAlignManipRecord70.Decode(theNode, theInt)
                            self.mAlignManipRecordList.append(theAlignManipRecord70)
                        elif theStr == theRatioManipRecord70.GetSBClassName():
                            theLastIndex = theRatioManipRecord70.Decode(theNode, theInt)
                            self.mRatioManipRecordList.append(theRatioManipRecord70)
                        elif theStr == theFRETManipRec70.GetSBClassName():
                            theLastIndex = theFRETManipRec70.Decode(theNode, theInt)
                            self.mFRETManipRecList.append(theFRETManipRec70)
                        elif theStr == theRemapManipRec70.GetSBClassName():
                            theLastIndex = theRemapManipRec70.Decode(theNode, theInt)
                            self.mRemapManipRecList.append(theRemapManipRec70)
                        elif theStr == theHistogramRecord70.GetSBClassName():
                            theLastIndex = theHistogramRecord70.Decode(theNode, theInt)
                            self.mHistogramRecordList.append(theHistogramRecord70)
                    else:
                        break

                theChannel += 1
        except:
            print ("CImageGroup::LoadChannelRecord error")
        return True

    def LoadMaks(self):
        try:
            thePath = self.mFile.GetImageGroupDirectory(self.mImageTitle) + os.sep +  self.mFile.kMaskRecordFilename
            inputStream = open(thePath,"r")
            theNode = yaml.compose(inputStream)

            theNodeList = theNode.value
            theTuple = theNodeList[0]
            theKey = theTuple[0].value
            if theKey == "theNumMasks":
                theValue = theTuple[1].value
                theNumMasks = int(theValue)
                self.mMaskRecordList = []
                if theNumMasks > 0:
                    theLastIndex = 1
                    for theMask in range(theNumMasks):
                        theMaskRecord = CMaskRecord70()
                        theLastIndex = theMaskRecord.Decode(theNode, theLastIndex)
                        self.mMaskRecordList.append(theMaskRecord)
                        theMask += 1
                else:
                    return True
                self.mMaskPosList = []
                while theLastIndex < len(theNodeList):
                    theTimePointIndex,theLastIndex = self.GetIntValue(theNode,theLastIndex,"theTimepointIndex")
                    if theLastIndex < 0:
                        break
                    theTuple = theNodeList[theLastIndex]
                    theKey = theTuple[0].value
                    if not theKey == "theMaskCompressedSizes":
                        break
                    theCurrentNode = theTuple[1]
                    thePos = CMaskPositions()
                    thePos.mCompressedSizes = self.GetIntArray(theCurrentNode, "theMaskCompressedSizes", True)
                    theLastIndex += 1
                    theTuple = theNodeList[theLastIndex]
                    theKey = theTuple[0].value
                    if not theKey == "theMaskFileOffsets":
                        break
                    theCurrentNode = theTuple[1]
                    thePos.mFileOffsets = self.GetIntArray(theCurrentNode, "theMaskFileOffsets", True)
                    theLastIndex += 1
                    self.mMaskPosList.append(thePos)

        except:
            print ("CImageGroup::LoadMaks error")
        return True

    def LoadAnnotations(self):
        try:
            thePath = self.mFile.GetImageGroupDirectory(self.mImageTitle) + os.sep +  self.mFile.kAnnotationRecordFilename
            inputStream = open(thePath,"r")
            theNode = yaml.compose(inputStream)

            theDataTableHeaderRecord70 = CDataTableHeaderRecord70()
            theLastIndex = theDataTableHeaderRecord70.Decode(theNode)
            self.mAnnotationList = []
            while True:
                theTimePointIndex,theLastIndex = self.GetIntValue(theNode,theLastIndex,"theTimepointIndex")
                if theLastIndex < 0:
                    break

                theAnno = CAnnotations()
                theCubeAnnotation70ListSize, theLastIndex = self.GetIntValue(theNode, theLastIndex, "theCubeAnnotation70ListSize")
                for theAnnotationIndex in range(theCubeAnnotation70ListSize):
                    theCubeAnnotation70 = CCubeAnnotation70()
                    theLastIndex = theCubeAnnotation70.Decode(theNode, theLastIndex)
                    theAnno.mCubeAnnotationList.append(theCubeAnnotation70)
                    theAnnotationIndex += 1
                
                theAnnotation70ListSize, theLastIndex = self.GetIntValue(theNode, theLastIndex, "theAnnotation70ListSize")
                for theAnnotationIndex in range(theAnnotation70ListSize):
                    theAnnotation70 = CAnnotation70()
                    theLastIndex = theAnnotation70.Decode(theNode, theLastIndex)
                    theAnno.mBaseAnnotationList.append(theAnnotation70)
                    theAnnotationIndex += 1

                theFRAPRegionAnnotation70ListSize, theLastIndex = self.GetIntValue(theNode, theLastIndex, "theFRAPRegionAnnotation70ListSize")
                for theAnnotationIndex in range(theFRAPRegionAnnotation70ListSize):
                    theFRAPRegionAnnotation70 = CFRAPRegionAnnotation70()
                    theLastIndex = theFRAPRegionAnnotation70.Decode(theNode, theLastIndex)
                    theAnno.mFRAPRegionAnnotationList.append(theFRAPRegionAnnotation70)
                    theAnnotationIndex += 1

                theUnknownAnnotation70ListSize, theLastIndex = self.GetIntValue(theNode, theLastIndex, "theUnknownAnnotation70ListSize")
                for theAnnotationIndex in range (theUnknownAnnotation70ListSize):
                    theUnknownAnnotation70 = CUnknownAnnotation70()
                    theLastIndex = theUnknownAnnotation70.Decode(theNode, theLastIndex)
                    theAnno.mUnknownAnnotationList.append(theUnknownAnnotation70)
                    theAnnotationIndex += 1
                self.mAnnotationList.append(theAnno)

        except:
            print ("CImageGroup::LoadAnnotations error")
        return True

    def LoadElapsedTimes(self):
        try:
            thePath = self.mFile.GetImageGroupDirectory(self.mImageTitle) + os.sep +  self.mFile.kElapsedTimesFilename
            inputStream = open(thePath,"r")
            theNode = yaml.compose(inputStream)

            theNodeList = theNode.value
            theTuple = theNodeList[0]
            theKey = theTuple[0].value
            if not theKey == "theElapsedTimes":
                return False
            theCurrentNode = theTuple[1]
            self.mElapsedTimes = self.GetIntArray(theCurrentNode, "theElapsedTimes", True)
        except:
            print ("CImageGroup::LoadElapsedTimes error")
        return True

    def LoadSAPositions(self):
        try:
            thePath = self.mFile.GetImageGroupDirectory(self.mImageTitle) + os.sep +  self.mFile.kSAPositionDataFilename
            inputStream = open(thePath,"r")
            theNode = yaml.compose(inputStream)

            theNodeList = theNode.value
            theLastIndex = 0
            theImageCount, theLastIndex = self.GetIntValue(theNode, theLastIndex, "theImageCount")

            self.mSAPositionList = []
            for theImageIndex in range(theImageCount):
                theTuple = theNodeList[theLastIndex]
                theKey = theTuple[0].value
                if not theKey == "theSAPositions":
                    break
                theCurrentNode = theTuple[1]
                theSAPositionsvector = self.GetIntArray(theCurrentNode,"theSAPositions",True);
                self.mSAPositionList.append(theSAPositionsvector)
                theLastIndex += 1
                theImageIndex += 1
        except:
            print ("CImageGroup::LoadSAPositions error")
        return True

    def LoadStagePosition(self):
        try:
            thePath = self.mFile.GetImageGroupDirectory(self.mImageTitle) + os.sep +  self.mFile.kStagePositionDataFilename
            inputStream = open(thePath,"r")
            theNode = yaml.compose(inputStream)
            theNodeList = theNode.value

            theLastIndex = 0
            theStructSize, theLastIndex = self.GetIntValue(theNode, theLastIndex, "StructArraySize")

            if theLastIndex < 0:
                return True
            self.mStagePositions = []
            theTuple = theNodeList[theLastIndex]
            theKey = theTuple[0].value
            if not theKey == "StructArrayValues":
                return False
            theCurrentNode = theTuple[1]
            thePoints = self.GetFloatArray(theCurrentNode,"StructArrayValues",False);

            for theP in range(0,len(thePoints),3):
                thePoint = CSBPoint(0.0)
                thePoint.mX = thePoints[theP]
                thePoint.mY = thePoints[theP + 1]
                thePoint.mZ = thePoints[theP + 2]
                self.mStagePositions.append(thePoint)
        except:
            print ("CImageGroup::LoadStagePosition error")
        return True

    def LoadAuxData(self):
        try:
            thePath = self.mFile.GetImageGroupDirectory(self.mImageTitle) + os.sep +  self.mFile.kAuxDataFilename
            inputStream = open(thePath,"r")
            theNode = yaml.compose(inputStream)
            theNodeList = theNode.value

            # FLOAT
            theLastIndex = 0
            theTableCount,theLastIndex = self.GetIntValue(theNode, theLastIndex, "theAuxFloatDataTablesSize")
            if theLastIndex < 0:
                return True
            self.mAuxFloatDataList = []
            for theTableIndex in range(theTableCount):
                theAux = CAuxFloatData()
                theAux.mTableHeaderRecord = CDataTableHeaderRecord70()

                theLastIndex = theAux.mTableHeaderRecord.Decode(theNode, theLastIndex)
                theAux.mXmlDescriptor,theLastIndex  =  self.GetStringValue(theNode,theLastIndex,"theXMLDescriptor",True);

                theKeyNode = theNodeList[theLastIndex]

                theKey = theKeyNode[0].value
                if not theKey == "theAuxData":
                    return False
                theCurrentNode = theKeyNode[1]
                theAux.mFloatData = self.GetFloatArray(theCurrentNode, "theAuxFloatData", True)
                theLastIndex += 1
                self.mAuxFloatDataList.append(theAux)

            # DOUBLE
            theTableCount,theLastIndex = self.GetIntValue(theNode, theLastIndex, "theAuxDoubleDataTablesSize")
            if theLastIndex < 0:
                return True
            self.mAuxDoubleDataList = []
            for theTableIndex in range(theTableCount):
                theAux = CAuxDoubleData()
                theAux.mTableHeaderRecord = CDataTableHeaderRecord70()

                theLastIndex = theAux.mTableHeaderRecord.Decode(theNode, theLastIndex)
                theAux.mXmlDescriptor,theLastIndex  =  self.GetStringValue(theNode,theLastIndex,"theXMLDescriptor",True);

                theKeyNode = theNodeList[theLastIndex]

                theKey = theKeyNode[0].value
                if not theKey == "theAuxData":
                    return False
                theCurrentNode = theKeyNode[1]
                theAux.mDoubleData = self.GetFloatArray(theCurrentNode, "theAuxDoubleData", True)
                theLastIndex += 1
                self.mAuxDoubleDataList.append(theAux)

            # SINT32
            theTableCount,theLastIndex = self.GetIntValue(theNode, theLastIndex, "theAuxSInt32DataTablesSize")
            if theLastIndex < 0:
                return True
            self.mAuxSInt32DataList = []
            for theTableIndex in range(theTableCount):
                theAux = CAuxSInt32Data()
                theAux.mTableHeaderRecord = CDataTableHeaderRecord70()

                theLastIndex = theAux.mTableHeaderRecord.Decode(theNode, theLastIndex)
                theAux.mXmlDescriptor,theLastIndex  =  self.GetStringValue(theNode,theLastIndex,"theXMLDescriptor",True);

                theKeyNode = theNodeList[theLastIndex]

                theKey = theKeyNode[0].value
                if not theKey == "theAuxData":
                    return False
                theAux.mSInt32Data = self.GetIntArray(theCurrentNode, "theAuxSInt32Data", True)
                theCurrentNode = theKeyNode[1]
                theLastIndex += 1
                self.mAuxSInt32DataList.append(theAux)

            # SINT64
            theTableCount,theLastIndex = self.GetIntValue(theNode, theLastIndex, "theAuxSInt64DataTablesSize")
            if theLastIndex < 0:
                return True
            self.mAuxSInt64DataList = []
            for theTableIndex in range(theTableCount):
                theAux = CAuxSInt64Data()
                theAux.mTableHeaderRecord = CDataTableHeaderRecord70()

                theLastIndex = theAux.mTableHeaderRecord.Decode(theNode, theLastIndex)
                theAux.mXmlDescriptor,theLastIndex  =  self.GetStringValue(theNode,theLastIndex,"theXMLDescriptor",True);

                theKeyNode = theNodeList[theLastIndex]

                theKey = theKeyNode[0].value
                if not theKey == "theAuxData":
                    return False
                theCurrentNode = theKeyNode[1]
                theAux.mSInt64Data = self.GetIntArray(theCurrentNode, "theAuxSInt64Data", True)
                theLastIndex += 1
                self.mAuxSInt64DataList.append(theAux)

            # XML
            theTableCount,theLastIndex = self.GetIntValue(theNode, theLastIndex, "theAuxSerializedDataTablesSize")
            if theLastIndex < 0:
                return True
            self.mAuxXmlDataList = []
            for theTableIndex in range(theTableCount):
                theAux = CAuxXmlData()
                theAux.mTableHeaderRecord = CDataTableHeaderRecord70()

                theLastIndex = theAux.mTableHeaderRecord.Decode(theNode, theLastIndex)
                theAux.mXmlDescriptor,theLastIndex  =  self.GetStringValue(theNode,theLastIndex,"theXMLDescriptor",True);
                if theLastIndex < 0:
                    return True
                theXmlAuxDataSize,theLastIndex  =  self.GetIntValue(theNode,theLastIndex,"theXmlAuxDataSize");
                if theLastIndex < 0:
                    return True
                theAux.mXmlData,theLastIndex  = self.GetStringValue(theNode, theLastIndex, "theXmlAuxData", True)
                if theLastIndex < 0:
                    return True
                self.mAuxXmlDataList.append(theAux)
        except:
            print ("CImageGroup::LoadAuxData error")
        return True

    def GetNumChannels(self):
        return self.mImageRecord.mNumChannels

    def GetNumColumns(self):
        return self.mImageRecord.mWidth

    def GetNumRows(self):
        return self.mImageRecord.mHeight

    def GetNumPlanes(self):
        return self.mImageRecord.mNumPlanes

    def GetNumPositions(self):
        theNumStagePositions = len(self.mStagePositions)
        if theNumStagePositions <= 1:
            return 1
        thePoint0 = self.mStagePositions[0]
        if self.mDebugPrint:
            print ("GetNumPositions: thePoint0 mX=" , thePoint0.mX , ", mY=" , thePoint0.mY)
        theNumUniquePositions = 1
        thePosition = 1
        for thePosition in range(1,theNumStagePositions):
            thePoint1 = self.mStagePositions[thePosition]
            if self.mDebugPrint:
                print ("GetNumPositions: thePoint1 mX=" , thePoint1.mX , ", mY=" , thePoint1.mY)
            if thePoint0.mX == thePoint1.mX and thePoint0.mY == thePoint1.mY:
                break
            theNumUniquePositions += 1
        if self.mDebugPrint:
            print ("GetNumPositions: theNumUniquePositions=" , theNumUniquePositions)
        return theNumUniquePositions

    def GetNumTimepoints(self):
        return self.mImageRecord.mNumTimepoints

    def GetElapsedTime(self, inTimepoint):
        return self.mElapsedTimes[inTimepoint]

    def GetBytesPerPixel(self):
        return 2

    def GetName(self):
        return self.mImageRecord.mName

    def GetInfo(self):
        return self.mImageRecord.mInfo

    def GetChannelName(self, inChannel):
        return self.mChannelRecordList[inChannel].mChannelDef.mName

    def GetLensName(self):
        return self.mImageRecord.mLensDef.mName

    def GetMagnification(self):
        return self.mImageRecord.mLensDef.mActualMagnification * self.mImageRecord.mOptovarDef.mMagnification

    def GetVoxelSize(self):
        theSize = self.mImageRecord.mLensDef.mMicronPerPixel
        if self.mImageRecord.mOptovarDef.mMagnification > 0:
            theSize /= self.mImageRecord.mOptovarDef.mMagnification
        theXFactor = self.mChannelRecordList[0].mExposureRecord.mXFactor
        if theXFactor > 0:
            theSize *= theXFactor
        return theSize

    def GetInterplaneSpacing(self):
        return self.mChannelRecordList[0].mExposureRecord.mInterplaneSpacing

    def GetExposureTime(self, inChannel):
        return self.mChannelRecordList[inChannel].mExposureRecord.mExposureTime

    def GetXPosition(self, inPosition):
        thePoint = self.mStagePositions[inPosition]
        return thePoint.mX

    def GetYPosition(self, inPosition):
        thePoint = self.mStagePositions[inPosition]
        return thePoint.mY

    def GetZPosition(self, inPosition, zplane):
        thePoint = self.mStagePositions[inPosition]
        return thePoint.mZ + self.GetInterplaneSpacing() * zplane

    def GetImageName(self):
        return self.mImageRecord.mName

    def GetImageComments(self):
        return self.mImageRecord.mInfo

    def GetCaptureDate(self):
        return self.mImageRecord.mYear, self.mImageRecord.mMonth, self.mImageRecord.mDay, self.mImageRecord.mHour, self.mImageRecord.mMinute, self.mImageRecord.mSecond

    def GetThumbnail(self):
        return self.mImageRecord.mThumbNail[1:len(self.mImageRecord.mThumbNail)]

    def GetAuxDataXMLDescriptor(self,inChannelIndex):
        mXmlDescriptor = ""

        for theAux in self.mAuxFloatDataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                mXmlDescriptor = theAux.mXmlDescriptor
                break

        for theAux in self.mAuxDoubleDataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                mXmlDescriptor = theAux.mXmlDescriptor
                break

        for theAux in self.mAuxSInt32DataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                mXmlDescriptor = theAux.mXmlDescriptor
                break

        for theAux in self.mAuxSInt64DataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                mXmlDescriptor = theAux.mXmlDescriptor
                break

        for theAux in self.mAuxXmlDataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                mXmlDescriptor = theAux.mXmlDescriptor
                break

        return mXmlDescriptor

    def GetAuxDataNumElements(self,inChannelIndex):
        for theAux in self.mAuxFloatDataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                return len(theAux.mFloatData),'float'
                break

        for theAux in self.mAuxDoubleDataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                return len(theAux.mDoubleData),'double'
                break

        for theAux in self.mAuxSInt32DataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                return len(theAux.mSInt32Data),'int32'
                break

        for theAux in self.mAuxSInt64DataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                return len(theAux.mSInt64Data),'int64'
                break

        for theAux in self.mAuxXmlDataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                return len(theAux.mXmlData),'str'
                break

        return 0,""


    def GetAuxFloatData(self,inChannelIndex):
        for theAux in self.mAuxFloatDataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                return theAux.mFloatData
        return []

    def GetAuxDoubleData(self,inChannelIndex):
        for theAux in self.mAuxDoubleDataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                return theAux.mDoubleData
        return []

    def GetAuxSInt32Data(self,inChannelIndex):
        for theAux in self.mAuxSInt32DataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                return theAux.mSInt32Data
        return []

    def GetAuxSInt64Data(self,inChannelIndex):
        for theAux in self.mAuxSInt64DataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                return theAux.mSInt64Data
        return []

    def GetAuxSerializedData(self,inChannelIndex,inElementIndex):
        theCount = 0
        for theAux in self.mAuxXmlDataList:
            if theAux.mTableHeaderRecord.mChannelIndex == inChannelIndex:
                if theCount == inElementIndex:
                    return theAux.mXmlData
                theCount += 1
        return []



    def Load(self):
        theResult = False
        if self.mDebugPrint:
            print ("CImageGroup: Load")
        theResult = self.LoadImageRecord()
        if not theResult:
            print ("LoadImageRecord: result " , theResult)
            return False
        theResult = self.LoadChannelRecord()
        if not theResult:
            print ("LoadChannelRecord: result " , theResult)
            return False
        theResult = self.LoadMaks()
        if not theResult:
            print ("LoadMaks: result " , theResult)
            return False
        theResult = self.LoadAnnotations()
        if not theResult:
            print ("LoadAnnotations: result " , theResult)
            return False
        theResult = self.LoadElapsedTimes()
        if not theResult:
            print ("LoadElapsedTimes: result " , theResult)
            return False
        theResult = self.LoadSAPositions()
        if not theResult:
            print ("LoadSAPositions: result " , theResult)
            return False
        theResult = self.LoadStagePosition()
        if not theResult:
            print ("LoadStagePosition: result " , theResult)
            return False
        theResult = self.LoadAuxData()
        if not theResult:
            print ("LoadAuxData: result " , theResult)
            return False
        return True


