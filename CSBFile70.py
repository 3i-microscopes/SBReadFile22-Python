__copyright__  = "Copyright (c) 2022, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."

import re
import os

class CSBFile70(object):
    """ generated source for class CSBFile70 """
    kSlideSuffix = ".sldy"
    kZSlideSuffix = ".sldyz"
    kRootDirSuffix = ".dir"
    kImageDirSuffix = ".imgdir"
    kBinaryFileSuffix = ".npy"
    kZBinaryFileSuffix = ".npyz";
    kImageRecordFilename = "ImageRecord.yaml"
    kChannelRecordFilename = "ChannelRecord.yaml"
    kAnnotationRecordFilename = "AnnotationRecord.yaml"
    kMaskRecordFilename = "MaskRecord.yaml"
    kAuxDataFilename = "AuxData.yaml"
    kElapsedTimesFilename = "ElapsedTimes.yaml"
    kSAPositionDataFilename = "SAPositionData.yaml"
    kStagePositionDataFilename = "StagePositionData.yaml"
    kNumDigitsInTimepoint = 7
    mSlidePath = str()
    mIsCompressed = False

    def __init__(self, inSlidePath):
        """ generated source for method __init__ """
        self.mSlidePath = inSlidePath
        self.mDebugPrint = False
        if(self.mSlidePath.endswith(self.kZSlideSuffix)):
            self.mIsCompressed = True

    def GetSlideRootDirectory(self):
        """ generated source for method GetSlideRootDirectory """
        if(not self.mIsCompressed):
            theRootDirectory = re.sub(self.kSlideSuffix + "$", self.kRootDirSuffix,self.mSlidePath)
        else:
            theRootDirectory = re.sub(self.kZSlideSuffix + "$", self.kRootDirSuffix,self.mSlidePath)
        return theRootDirectory

    def GetListOfImageGroupTitles(self):
        """ generated source for method GetListOfImageGroupTitles """
        theRootDirectory = self.GetSlideRootDirectory()
        theTitles = []
        theMap = {}
        for entry in os.scandir(theRootDirectory):
            if not entry.is_dir():
                continue
            if entry.name.endswith(self.kImageDirSuffix) == False:
                continue
            #check the directory is not empty
            theImageRecordPath = entry.path + os.sep + self.kImageRecordFilename
            if os.path.isfile(theImageRecordPath) == False:
                continue
            #scan this directory for .npy files
            found = False
            for subentry in os.scandir(entry.path):
                if subentry.name.endswith(self.kBinaryFileSuffix):
                    found = True
                    break
                if subentry.name.endswith(self.kZBinaryFileSuffix):
                    found = True
                    break
            if found == False: 
                continue
                

            theTitle = re.sub(self.kImageDirSuffix,"",entry.name)
            statinfo = os.stat(entry.path)
            theModTimNS = statinfo.st_mtime_ns
            theInserted = False
            while theInserted == False:
                theKey = "{:025d}".format(theModTimNS)
                if theKey in theMap:
                    theModTimNS = theModTimNS + 1
                else:
                    theInserted = True

            theMap[theKey]  = theTitle

        for theModTim, theTitle in sorted(theMap.items()):

            theTitles.append(theTitle)


        return theTitles

    def GetImageGroupDirectory(self, inTitle):
        """ generated source for method GetImageGroupDirectory """
        if inTitle == None:
            return None
        theRootDirectory = self.GetSlideRootDirectory()
        theImageGroupDirectory = theRootDirectory + os.sep + inTitle + self.kImageDirSuffix + os.sep
        return theImageGroupDirectory

    def GetImageDataFile(self, inTitle, inChannel, inTimepoint):
        """ generated source for method GetImageDataFile """
        if inTitle == None:
            return None
        theImageGroupDirectory = self.GetImageGroupDirectory(inTitle)
        # buf = "A = %d\n , B = %s\n" % (a, b)

        theSuffix = self.kBinaryFileSuffix
        if(self.mIsCompressed):
            theSuffix = self.kZBinaryFileSuffix

        thePath = "%s%s%s_Ch%1d_TP%07d%s" %( theImageGroupDirectory, os.sep, "ImageData", inChannel, inTimepoint, theSuffix)
        return thePath

    def GetMaskDataFile(self, inTitle, inTimepoint):
        """ generated source for method GetMaskDataFile """
        if inTitle == None:
            return None
        theImageGroupDirectory = self.GetImageGroupDirectory(inTitle)
        thePath = "%s%s%s_TP%07d%s" % ( theImageGroupDirectory, os.sep, "MaskData", inTimepoint, self.kBinaryFileSuffix)
        return thePath

    def GetHistogramDataFile(self, inTitle, inChannel, inTimepoint):
        """ generated source for method GetHistogramDataFile """
        theImageGroupDirectory = self.GetImageGroupDirectory(inTitle)
        thePath = str()
        if inTimepoint >= 0:
            thePath = "%s%s%s_Ch%1d_TP%07d%s" % ( theImageGroupDirectory, os.sep, "HistogramData", inChannel, inTimepoint, self.kBinaryFileSuffix)
        else:
            thePath = "%s%s%s_Ch%1d%s" % ( theImageGroupDirectory, os.sep, "HistogramSummary", inChannel, self.kBinaryFileSuffix)
        return thePath

    def GetChannelIndexOfPath(self, inPath):
        """ generated source for method GetChannelIndexOfPath """
        thePos = inPath.lastIndexOf("_Ch")
        if thePos == -1:
            return -1
        theDigit = inPath.substring(thePos + 3, 1)
        theChannel = Integer.valueOf(theDigit)
        return theChannel

    def GetTimepointOfPath(self, inPath):
        """ generated source for method GetTimepointOfPath """
        thePos = inPath.lastIndexOf("_TP")
        if thePos == -1:
            return -1
        theDigit = inPath.substring(thePos + 3, self.kNumDigitsInTimepoint)
        theTimepoint = Integer.valueOf(theDigit)
        return theTimepoint

    def RenamePathToTimepoint0(self,inPath):
        ouPath = inPath
        thePos = inPath.rfind("_TP")
        if thePos == -1:
            return False,ouPath
        ouPath = "{f1}{f2}{f3}".format(f1=inPath[:thePos],f2='_TP0000000',f3=inPath[thePos + 3 + self.kNumDigitsInTimepoint:])
        return True,ouPath

    def getListOfNpyDataFiles(self, inTitle, inStartWith):
        """ generated source for method getListOfNpyDataFiles """
        theImageGroupDirectory = self.GetImageGroupDirectory(inTitle)
        if self.mDebugPrint:
            print ("getListOfNpyDataFiles: theImageGroupDirectory " + theImageGroupDirectory)
        theFilePaths = []
        for entry in os.scandir(theImageGroupDirectory):
            if not entry.name.endswith(self.kBinaryFileSuffix) and not entry.name.endswith(self.kZBinaryFileSuffix):
                continue
            if not entry.name.startswith(inStartWith):
                continue
            theFilePaths.append(entry.path)
            if self.mDebugPrint:
                print ("getListOfNpyDataFiles: found: " + entry.path)

        return theFilePaths


    def GetListOfImageDataFiles(self, inTitle):
        """ generated source for method GetListOfImageDataFiles """
        return self.getListOfNpyDataFiles(inTitle, "ImageData")

    def GetListOfMaskDataFiles(self, inTitle):
        """ generated source for method GetListOfMaskDataFiles """
        return self.getListOfNpyDataFiles(inTitle, "MaskData")

    def GetListOfHistogramDataFiles(self, inTitle):
        """ generated source for method GetListOfHistogramDataFiles """
        return self.getListOfNpyDataFiles(inTitle, "HistogramData")

    def GetListOfHistogramSummaryFiles(self, inTitle):
        """ generated source for method GetListOfHistogramSummaryFiles """
        return self.getListOfNpyDataFiles(inTitle, "HistogramSummary")


