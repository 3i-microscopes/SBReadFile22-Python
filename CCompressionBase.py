__copyright__  = "Copyright (c) 2022-2025, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."

import numpy as np
import pyzstd 

class CCompressionBase(object):
    def __init__(self):
        self.eCompressionNone = 0       # none
        self.eCompressionZstd = 1       # facebook
        self.eCompressionZlib = 2       # gzip
        self.eCompressionLz4 = 3        # lz4
        self.eCompressionJetRaw = 4
        self.eCompressionRLE = 5        # Run length Encoded

        self.mErrorMessage = str()
        self.mAlgorythm = self.eCompressionNone
        self.mNumX = 0
        self.mNumY = 0
        self.mNumZ = 0
        self.mNumBlocks = 0
        self.mBufLenBY = 0
        self.mDictionaryRead = False
        self.mBlockDictionarySize = 16
        self.mUint16Size = 2
        self.mBlockDictionary = np.zeros(1,dtype=np.uint64)

    def GetErrorMessage(self):
        return self.mErrorMessage

    def Initialize(self,inDictionaryPosition,inAlgorythm,inNumX,inNumY,inNumZ,inNumberOfThreads):

        self.mAlgorythm = inAlgorythm
        self.mNumX = inNumX
        self.mNumY = inNumY
        self.mNumZ = inNumZ
        self.mNumBlocks = self.mNumZ;
        self.mNumberOfThreads = inNumberOfThreads
        self.mDictionaryPosition = inDictionaryPosition
        self.mDataPosition = self.mDictionaryPosition + self.mNumZ * self.mBlockDictionarySize
        self.mDataLenBY = self.mNumX * self.mNumY * self.mUint16Size

    def InitializeEx(self,inDictionaryPosition,inAlgorythm,inNumX,inNumY,inNumZ,inNumBlocks,inNumberOfThreads):

        self.mAlgorythm = inAlgorythm
        self.mNumX = inNumX
        self.mNumY = inNumY
        self.mNumZ = inNumZ
        self.mNumBlocks = inNumBlocks;
        self.mNumberOfThreads = inNumberOfThreads
        self.mDictionaryPosition = inDictionaryPosition
        self.mDataPosition = self.mDictionaryPosition + self.mNumBlocks * self.mBlockDictionarySize
        self.mDataLenBY = self.mNumX * self.mNumY * self.mNumZ * self.mUint16Size

    def ReadDictionary(self,inStream):
        ouBuf = inStream.read(self.mNumZ*self.mBlockDictionarySize)

        self.mBlockDictionary = np.frombuffer(ouBuf,dtype=np.uint64)
        self.mDictionaryRead = True

    def GetDataOffsetForBlock(self,inBlock):
        if inBlock == 0:
            return self.mDataPosition
        thePos = self.mBlockDictionary[(inBlock-1)*2]
        theLen = self.mBlockDictionary[(inBlock-1)*2+1]

        return thePos + theLen

    def GetDataSizeForBlock(self,inBlock):
       theLen = self.mBlockDictionary[inBlock*2+1]
       return theLen

    def DecompressBuffer(self,inBuffer):
        if self.mAlgorythm == self.eCompressionZstd:
            theDecompressedBuf = pyzstd.decompress(inBuffer)
            return theDecompressedBuf
        elif self.mAlgorythm == self.eCompressionRLE:
            theUncompressedSize = int(self.mDataLenBY/self.mUint16Size)
            theDataP = np.frombuffer(inBuffer,dtype=np.uint16)
            theCompressedSize = theDataP.size

            theDecompressedBuf = np.empty(theUncompressedSize, dtype=np.uint16)
            j = 0
            i = 0
            while True:
                theValue = theDataP[j]
                j += 1

                # Is this a count?
                if theValue & 0x8000:
                    theCount = theValue & 0x7fff
                    theValue = theDataP[j]
                    j += 1
                else:
                    theCount = 1

                while theCount > 0 and i < theUncompressedSize:
                    theDecompressedBuf[i] = theValue
                    i += 1
                    theCount -= 1

                if i >= theUncompressedSize or j >= theCompressedSize:
                    break
            return theDecompressedBuf

        else:
            raise Exception("Invalid compression type")

    def ReadData(self,inStream,inBlock):

        if not self.mDictionaryRead:
            self.ReadDictionary(inStream)
        
        theDataPos = self.GetDataOffsetForBlock(inBlock)
        theCompressedLengthBY = self.GetDataSizeForBlock(inBlock)

        inStream.seek(theDataPos,0)

        ouBuf = inStream.read(theCompressedLengthBY)

        #decompress
        theUncompressedBuf = self.DecompressBuffer(ouBuf)


        if len(theUncompressedBuf) != self.mNumX * self.mNumY *self.mUint16Size :
            raise NameError("Error in decoding")

        return theUncompressedBuf
