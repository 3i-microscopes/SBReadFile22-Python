__copyright__  = "Copyright (c) 2022-2025, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."

from CNpyHeader import *
from CCompressionBase import *
from matplotlib import pyplot as plt
import numpy as np
import sys, getopt

def main(argv):
    # change it to use your file
    #theFileName = "C:/Data/Slides_msi/Masks/NewMask1.dir/Capture 11660836293.imgdir/MaskData_TP0000000.npyz")
    if len(sys.argv) < 3:
        print ('usage: python ReadCompressedNpyzFile.py -i <inputfile.npyz>')
        sys.exit(2)

    theFileName = ''
    theBlock = 0
    try:
        opts, args = getopt.getopt(argv,"hi:n:",["ifile=","number="])
    except getopt.GetoptError:
        print ('usage: python ReadCompressedNpyzFile.py -i <inputfile.npyz> -n plane_or_mask_number')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('usage: python ReadCompressedNpyzFile.py -i <inputfile.npyz> -n plane_or_mask_number')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            theFileName = arg
        elif opt in ("-n", "--number"):
            theBlock = int(arg)
    print ('Input file is ', theFileName)

    theStream = open(theFileName,"rb")
    theNpyHeader = CNpyHeader()
    theRes = theNpyHeader.ParseNpyHeader( theStream)
    if not theRes:
        raise("Could not parse header")

    theNumDim = len(theNpyHeader.mShape)
    theNumBlocks = 0
    j = 0
    if theNumDim == 4:
        theNumBlocks = theNpyHeader.mShape[j]
        j += 1

    theNumPlanes = theNpyHeader.mShape[j]
    theNumRows = theNpyHeader.mShape[j+1]
    theNumColumns = theNpyHeader.mShape[j+2]

    theCompressor = CCompressionBase()
    if theNumDim == 4:
        theCompressor.InitializeEx(theNpyHeader.mHeaderSize,theNpyHeader.mCompressionFlag,theNumColumns,theNumRows,theNumPlanes,theNumBlocks,0)
        theCompressor.ReadDictionary(theStream)
    else:
        theCompressor.Initialize(theNpyHeader.mHeaderSize,theNpyHeader.mCompressionFlag,theNumColumns,theNumRows,theNumPlanes,0)
        theCompressor.ReadDictionary(theStream)

    theSeekOffset = theCompressor.GetDataOffsetForBlock(theBlock)
    theCompressedSize = theCompressor.GetDataSizeForBlock(theBlock)

    theStream.seek(theSeekOffset,0)
    theCompressedBuffer = theStream.read(theCompressedSize)
    theUncompressedBuffer = theCompressor.DecompressBuffer(theCompressedBuffer)
    if theNumDim == 4:
        theUncompressedBuffer = theUncompressedBuffer.reshape(theNumPlanes,theNumRows,theNumColumns)
        #plot midplane
        theZplane = int(theNumPlanes/2)
        image = theUncompressedBuffer[theZplane,:,:]

    else:
        theUncompressedBuffer = theUncompressedBuffer.reshape(theNumRows,theNumColumns)
        image = theUncompressedBuffer


    plt.imshow(image)
    plt.pause(0.001)

    data = input("Please hit Enter to exit:\n")

if __name__ == "__main__":
    main(sys.argv[1:])
    


