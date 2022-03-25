from CMetadataLib import *
from CSBFile70 import *
from CImageGroup import *
import numpy as np
import yaml

class DataLoader(object):

    def __init__(self, inSlidePath):
        self.mSlidePath = inSlidePath
        self.mFile = CSBFile70(inSlidePath)
        self.mErrorMessage = str()
        self.mSlideRecord = CSlideRecord70()
        self.mCImageGroupList = []
        self.mPathToStreamMap = dict()
        self.mCounterToPathMap = dict()
        self.kMaxNumberOpenFiles = 100
        self.mCurrentFileCounter = 0
        self.mDebugPrint = False

    def CheckCaptureIndex(self,inCaptureIndex):
        if len(self.mCImageGroupList) == 0:
            raise Exception('No Image Groups exist')

        if inCaptureIndex >= len(self.mCImageGroupList):
            raise Exception('Capture Index value to big: {}'.format(inCaptureIndex))

    def ByteArrayToShort(self, byteArray, offset):
        theVal = ((byteArray[offset + 1] & 0xFF) << 8) | ((byteArray[offset + 0] & 0xFF) << 0)
        return int(theVal)

        
    def ReadSldFromStream(self, inInputStream):
        theNode = yaml.compose(inInputStream)
        self.mSlideRecord = CSlideRecord70()
        try:
            theLastIndex = self.mSlideRecord.Decode(theNode);
            #print("ReadSld(stream): theLastIndex: " , theLastIndex)
            #print("ReadSld(stream): mByteOrdering: " , self.mSlideRecord.mByteOrdering)
            return True
        except:
            self.mErrorMessage += "Could not load file: " + self.mSlidePath
            return False

    def ReadSld(self):
        inputStream = open(self.mSlidePath,"r")
        res = self.ReadSldFromStream(inputStream)
        inputStream.close()
        return res

    def LoadMetadata(self):
        try:
            theResult = self.ReadSld()

            if not theResult:
                print ("LoadMetadata: ReadSld result: ", theResult)
                return False
            # if you are using this while slide book is running and modifying the slide
            # then you should lock the file SB7Lock.lck in the slide root directory
            # (self.mFile.GetSlideRootDirectory())
            # and release the lock when done
            # probably this can be done with open(theLockFilePath,'x') and looping until it succeed
            theImageTitles = self.mFile.GetListOfImageGroupTitles()
            theImageGroupIndex = 0
            for theImageTitle in  theImageTitles:
                theImageGroup = CImageGroup(self.mFile,theImageTitle)
                theResult = theImageGroup.Load()
                if theResult:
                    self.mCImageGroupList.append(theImageGroup)
                else:
                    print ("LoadMetadata: theImageGroupIndex: " , theImageGroupIndex , " Load:  result: " , theResult)
                theImageGroupIndex += 1
            return True
        except:
            print ("Could not load file: " + self.mSlidePath)
            return False


    def GetNumCaptures(self):
        return len(self.mCImageGroupList)

    def GetImageGroup(self, inCaptureId):
        return self.mCImageGroupList[inCaptureId]

    def ReadPlane(self, inCaptureId,  inPositionIndex, inTimepointIndex, inZPlaneIndex, inChannelIndex, inAs2D=False):
        #print("ReadPlane: inPositionIndex: " , inPositionIndex)
        #print("ReadPlane: inTimepointIndex: " , inTimepointIndex)
        #print("ReadPlane: inZPlaneIndex: " , inZPlaneIndex)
        #print("ReadPlane: inChannelIndex: " , inChannelIndex)
        theImageGroup = self.GetImageGroup(inCaptureId)
        theSbTimepointIndex = inTimepointIndex
        thePath = theImageGroup.mFile.GetImageDataFile(theImageGroup.mImageTitle, inChannelIndex, theSbTimepointIndex)
        if thePath not in self.mPathToStreamMap:
            if len(self.mCounterToPathMap) > self.kMaxNumberOpenFiles:
                theKeyValue = next(iter(mCounterToPathMap.values()))  # gets the first value
                theKeyPath = mCounterToPathMap.get(theKeyValue)
                if theKeyPath != None:
                    theKeyStream = mPathToStreamMap.get(theKeyPath)
                    if theKeyStream != None:
                        theKeyStream.close()
                        del self.mCounterToPathMap[theKeyValue]
                        del self.mPathToStreamMap[theKeyPath]
            theStream = open(thePath,"rb")
            if theImageGroup.mNpyHeader == None:
                theImageGroup.mNpyHeader = CNpyHeader()
                theRes = theImageGroup.mNpyHeader.ParseNpyHeader( theStream)
                if not theRes:
                    return False
            self.mPathToStreamMap[thePath] = theStream
            self.mCounterToPathMap[self.mCurrentFileCounter] = thePath
            self.mCurrentFileCounter += 1
        else:
            theStream = self.mPathToStreamMap[thePath]

        theNumRows = theImageGroup.GetNumRows()
        theNumColumns = theImageGroup.GetNumColumns()
        thePlaneSize = theNumColumns * theNumRows * theImageGroup.mNpyHeader.mBytesPerPixel
        if self.mDebugPrint:
            print ("ReadPlane: thePlaneSize: " , thePlaneSize)
        theSeekOffset = theImageGroup.mNpyHeader.mHeaderSize + thePlaneSize * inZPlaneIndex
        if self.mDebugPrint:
            print ("ReadPlane: theSeekOffset: " , theSeekOffset)
        theStream.seek(theSeekOffset,0)

        ouBuf = theStream.read(thePlaneSize)

        theNpBuf = np.frombuffer(ouBuf,dtype=np.uint16)
        if inAs2D:
            theNpBuf = theNpBuf.reshape(theNumRows,theNumColumns)


        return theNpBuf

    def CloseFile(self):
        return True
