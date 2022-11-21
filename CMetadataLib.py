__copyright__  = "Copyright (c) 2022, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."

from BaseDecoder import BaseDecoder
from CSBPoint import CSBPoint
import yaml

class CAlignManipRecord70(BaseDecoder):
    """ generated source for class CAlignManipRecord70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mManipID = int()
        self.mXOffset = float()
        self.mYOffset = float()
        self.mZOffset = float()

class CAnnotation70(BaseDecoder):
    """ generated source for class CAnnotation70 """
    def __init__(self):
        """ generated source for method __init__ """
        super().__init__()

        self.mGraphicType70 = int()
        self.mDependencyType70 = int()
        self.mText = str()
        self.mChannelMask = [False]
        self.mGroupId = int()
        self.mPlaneId = int()
        self.mSequenceId = int()
        self.mObjectId = int()
        self.mDependencyRef = int()
        self.mVersion = int()
        self.mByteOrdering = int()
        self.mFieldOffsetMicrons = CSBPoint(0.0)
        self.mFieldMicronsPerPixel = float()
        self.mFieldOffsetSet = bool()
        self.mStageOffsetMicrons = CSBPoint(0.0)
        self.mStageOffsetSet = bool()
        self.mZStageIncreaseTowardsSample = bool()
        self.mAuxZStageMicrons = float()
        self.mAuxZStageMicronsSet = bool()
        self.mAuxZStageIncreaseTowardsSample = bool()
        self.mZStageDirectionsValid = bool()
        self.mStoreMicronPositions = bool()
        self.mRelativePower = float()
        self.mBorderFillPixels = int()
        self.mVertexes = []


    def DecodeUnknownString(self, inUnknownString, inAttrKeyNode):
        if isinstance(inAttrKeyNode[1], yaml.nodes.ScalarNode):
            theAttrValue = inAttrKeyNode[1].value
            if inUnknownString == "mStageOffsetMicrons.mX":
                self.mStageOffsetMicrons.mX = float(theAttrValue)
            elif inUnknownString == "mStageOffsetMicrons.mY":
                self.mStageOffsetMicrons.mY = float(theAttrValue)
            elif inUnknownString == "mFieldOffsetMicrons.mX":
                self.mFieldOffsetMicrons.mX = float(theAttrValue)
            elif inUnknownString == "mFieldOffsetMicrons.mY":
                self.mFieldOffsetMicrons.mY = float(theAttrValue)
            else:
                return False
            return True
        elif isinstance(inAttrKeyNode[1], yaml.nodes.SequenceNode):
            self.mVertexes = []
            thePoints = self.GetIntArray(inAttrKeyNode[1],"inUnknownString",False)
            for theP in range(0, len(thePoints),3):
                thePoint = CSBPoint(0)
                thePoint.mX = thePoints[theP]
                thePoint.mY = thePoints[theP + 1]
                thePoint.mZ = thePoints[theP + 2]
                self.mVertexes.append(thePoint)
            return True
        else:
            return False


class CFluorDef70(BaseDecoder):
    """ generated source for class CFluorDef70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mName = str()
        self.mLaserPowerPos = int()
        self.mCameraBitDepth = int()
        self.mAuxFilterWheel8Pos = int()
        self.mAuxFilterWheel9Pos = int()
        self.mAuxFilterWheel10Pos = int()
        self.mAuxFilterWheel7Pos = int()
        self.mNumExposuresAverage = int()
        self.mExcitationLambda = float()
        self.mAuxFilterWheel5Pos = int()
        self.mAuxFilterWheel6Pos = int()
        self.mLambda = float()
        self.mTurretPosition = int()
        self.mUV = bool()
        self.mImagingMode = int()
        self.mExcitationWheelPos = int()
        self.mEmissionWheelPos = int()
        self.mLightSource = int()
        self.mTransmittedModePrompt = bool()
        self.mLambdaOptions = int()
        self.mAuxFilterWheel4Pos = int()
        self.mDefaultColor = int()
        self.mChannelType = int()
        self.mLCDPos = int()
        self.mTIRFPos = int()
        self.mRGBFactor = [0]
        self.mFilterSet = int()
        self.mCamera = int()
        self.mOcularPhotoTurretPos = int()
        self.mCameraVideoTurretPos = int()
        self.mIlluminationMode = int()
        self.mAltSourcePosition = int()
        self.mCameraGain = int()
        self.mCameraSpeed = int()
        self.mCameraIntensification = int()
        self.mCameraPort = int()
        self.mCameraParameter1 = int()
        self.mNDPos = int()
        self.mHue = int()
        self.mSaturation = int()
        self.mValue = int()
        self.mAuxFilterWheelPos = int()
        self.mDefaultColorDisplay = int()
        self.mAuxNDPos = int()
        self.mAuxFilterWheel2Pos = int()
        self.mAuxFilterWheel3Pos = int()

class CExposureRecord70(BaseDecoder):
    """ generated source for class CExposureRecord70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mAuxZStartPosition = float()
        self.mExposureTime = int()
        self.mXOffset = int()
        self.mYOffset = int()
        self.mXExtent = int()
        self.mYExtent = int()
        self.mBinning = bool()
        self.mTimeLapse = bool()
        self.mCaptureType = int()
        self.mXFactor = int()
        self.mYFactor = int()
        self.mNumPlanes = int()
        self.mNuTSACSampleSize = int()
        self.mScanning = bool()
        self.mInterplaneSpacing = float()
        self.mInitialOffset = float()
        self.mTimeLapseInterval = int()
        self.mCaptureSetId = int()
        self.mXStartPosition = float()
        self.mYStartPosition = float()
        self.mZStartPosition = float()
        self.mCaptureFlags = int()
        self.mAuxCaptureFlags = int()
        self.mMoveFieldRightSign = int()
        self.mMoveFieldDownSign = int()

class CLensDef70(BaseDecoder):
    """ generated source for class CLensDef70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mName = str()
        self.mNA = float()
        self.mdf = float()
        self.mMicronPerPixel = float()
        self.mDeprecatedMagnification = int()
        self.mMedium = int()
        self.mUV = bool()
        self.mTurretPosition = int()
        self.mParfocalOffset = int()
        self.mDefault = bool()
        self.mParfocalOffset2 = int()
        self.mParcentricOffsetX = float()
        self.mParcentricOffsetY = float()
        self.mBrightfieldPos = int()
        self.mDarkfieldPos = int()
        self.mDICPos = int()
        self.mPhasePos = int()
        self.mTLFieldDiaphramPos = int()
        self.mTLApertureDiaphramPos = int()
        self.mDICPrismPos = int()
        self.mTopLensPos = int()
        self.mPolarizerPos = int()
        self.mCameraName = str()
        self.mCameraPixelSize = float()
        self.mCameraMagnificationChange = float()
        self.mActualMagnification = float()

class CMainViewRecord70(BaseDecoder):
    """ generated source for class CMainViewRecord70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mViewID = int()
        self.mRedChannel = int()
        self.mGreenChannel = int()
        self.mBlueChannel = int()
        self.mBkgndChannel = int()
        self.mLow = [0]
        self.mHigh = [0]
        self.mColorDisplay = int()
        self.mPseudoFrom = float()
        self.mPseudoTo = float()
        self.mThumbPlane = int()
        self.mViewOptions = int()
        self.mGamma = [0]
        self.mHue = [0]
        self.mSaturation = [0]
        self.mValue = [0]
        self.mChannelEnabled = [0]
        self.mBitDepth = [0]
        self.mBlendFraction = float()
        self.mThumbTimePoint = int()

class CMaskRecord70(BaseDecoder):
    """ generated source for class CMaskRecord70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mName = str()
        self.mNumManip = int()
        self.mManipPtr = int()
        self.mMaskDataTablePtr = int()
        self.mPersistentSubmasks = int()
        self.mCentroidFeature = str()
        self.mCentroidChannel = int()

class COptovarDef70(BaseDecoder):
    """ generated source for class COptovarDef70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mName = str()
        self.mMagnification = float()
        self.mDefault = bool()
        self.mTurretPosition = int()

class CRatioManipRecord70(BaseDecoder):
    """ generated source for class CRatioManipRecord70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mManipID = int()
        self.mKd = float()
        self.mRmin = float()
        self.mRmax = float()
        self.mBeta = float()
        self.mRlow = float()
        self.mRhigh = float()
        self.mNumBackground = int()
        self.mDenBackground = int()
        self.mExposureFactor = float()
        self.mBackX1 = int()
        self.mBackY1 = int()
        self.mBackX2 = int()
        self.mBackY2 = int()
        self.mNumMin = int()
        self.mNumMax = int()
        self.mDenMin = int()
        self.mDenMax = int()

class CRemapChannelLUT70(BaseDecoder):
    """ generated source for class CRemapChannelLUT70 """
    def __init__(self):
        self.mCoefficients = [1.0]  #TODO is a vector
        self.mValues = [1.0]  #TODO is a vector
        self.mInsideRange = [False]  #TODO is a vector
        self.mLowDesired = float()
        self.mHighDesired = float()
        self.mLowGiven = int()
        self.mHighGiven = int()
        self.mBuiltTable = bool()
        self.mRemapType = int()
        self.mEquationString = str()
        self.mPoints = [] # a RemapPointsVector

class CRemapManipRecord70(BaseDecoder):
    """ generated source for class CRemapManipRecord70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mManipID = int()
        self.mRemapType = int()
        self.mNumCalibPoints = int()
        self.mReserved2 = int()
        self.mCalibDataPtrLow = int()
        self.mCalibDataPtrHigh = int()

class CCube(BaseDecoder):
    """ generated source for class CCube """
    def __init__(self):
        self.mTopX = int()
        self.mTopY = int()
        self.mTopZ = int()
        self.mBottomX = int()
        self.mBottomY = int()
        self.mBottomZ = int()


class CRemapPoint(BaseDecoder):
    """ generated source for class CRemapPoint """
    def __init__(self):
        self.mGivenValue = float()
        self.mDesiredValue = float()
        self.mSamplingStdDev = float()
        self.mCube = CCube()

class CSlideRecord70(BaseDecoder):
    """ generated source for class CSlideRecord70 """
    def __init__(self):
        self.mStructVersion = int()
        self.mStructID = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mNotesLen = int()
        self.mNumImages = int()
        self.mNotesPtr = int()
        self.mImagePtr = int()
        self.mPrefsFileLen = int()
        self.mPrefsOffset = int()
        self.mHardwareFileOffset = int()
        self.mHighestCount = int()
        self.mUncompactedSpace = int()
        self.mCheckpointNumImages = int()
        self.mCheckpointImagePtr = int()
        self.mCheckpointMaxImages = int()
        self.mHardwareFileLen = int()
        self.mCaptureStatus = int()
        self.mDemoFlag = int()
        self.mName = str()
        self.mProjectFolder = str()
        self.mSpecialBuildStr = str()
        self.mFileVersion = [0]


class CChannelDef70(BaseDecoder):
    """ generated source for class CChannelDef70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mName = str()
        self.mCameraName = str()
        self.mFluorDef = CFluorDef70()

    def Decode(self, inNode, inStartIndex):
        """ generated source for method Decode """
        self.mFluorDef = CFluorDef70()
        theLastIndex = super().Decode(inNode, inStartIndex)
        theLastIndex = self.mFluorDef.Decode(inNode, theLastIndex)
        return theLastIndex

class CChannelRecord70(BaseDecoder):
    """ generated source for class CChannelRecord70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mNumPlanes = int()
        self.mNumManip = int()
        self.mManipPtr = int()
        self.mDataType = int()
        self.mDataTablePtr = int()
        self.mHistogramTablePtr = int()
        self.mHistogramSummaryPtr = int()
        self.mExposureRecord = CExposureRecord70()
        self.mChannelDef = CChannelDef70()

    def Decode(self, inNode, inStartIndex):
        """ generated source for method Decode """
        self.mExposureRecord = CExposureRecord70()
        self.mChannelDef = CChannelDef70()
        theLastIndex = super().Decode(inNode, inStartIndex)
        theLastIndex = self.mExposureRecord.Decode(inNode, theLastIndex)
        theLastIndex = self.mChannelDef.Decode(inNode, theLastIndex)
        return theLastIndex

class CCubeAnnotation70(BaseDecoder):
    """ generated source for class CCubeAnnotation70 """
    def __init__(self):
        self.mIsBackground = bool()
        self.mRegionIndex = int()
        self.mIsFRAP = bool()
        self.mFRAPDevice = str()
        self.mIsStimulation = bool()
        self.mIsLLS = bool()
        self.mIsNoLabel = bool()
        self.mReservedBuf = str()
        self.mIsIntSet = bool()
        self.mIsFloatSet = bool()
        self.mIntData = int()
        self.mFloatData = float()
        self.mAnn = CAnnotation70()

    def Decode(self, inNode, inStartIndex):
        """ generated source for method Decode """
        self.mAnn = CAnnotation70()
        theLastIndex = super().Decode(inNode, inStartIndex)
        theLastIndex = self.mAnn.Decode(inNode, theLastIndex)
        return theLastIndex

class CDataTableHeaderRecord70(BaseDecoder):
    """ generated source for class CDataTableHeaderRecord70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mParentRecordPtr = int()
        self.mChannelIndex = int()
        self.mRows = int()
        self.mColumns = int()
        self.mPlanes = int()
        self.mValueType = int()
        self.mTableType = int()
        self.mTimeBasis = int()
        self.mDescriptorVersion = int()
        self.mDescriptorSize = int()
        self.mDescriptorFileOffset = int()
        self.mStartTime = int()
        self.mTimeInterval = int()
        self.mTimePointsWritten = int()
        self.mTimePointsTableSize = int()
        self.mNextTableFileOffset = int()

class CFRAPRegionAnnotation70(BaseDecoder):
    """ generated source for class CFRAPRegionAnnotation70 """
    def __init__(self):
        self.mXML = str()
        self.mRegions = [] #TODO std::vector<CCubeAnnotation> mRegions
        self.mAnn = CAnnotation70()

    def Decode(self, inNode, inStartIndex):
        """ generated source for method Decode """
        self.mAnn = CAnnotation70()
        theLastIndex = super().Decode(inNode, inStartIndex)
        theLastIndex = self.mAnn.Decode(inNode, theLastIndex)
        theIIPair = GetIntegerValue(inNode, theLastIndex, "theNumRegions")
        theNumRegions = theIIPair.mInt1
        theLastIndex = theIIPair.mInt2
        self.mRegions = []
        theRegionIndex = 0
        while theRegionIndex < theNumRegions:
            theLastIndex = theCubeAnnotation70.Decode(inNode, theLastIndex)
            self.mRegions.add(theCubeAnnotation70)
            theRegionIndex += 1
        return theLastIndex

class CFRETManipRecord70(BaseDecoder):
    """ generated source for class CFRETManipRecord70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mManipID = int()
        self.mFRETParadigm = int()
        self.mFdDd = float()
        self.mFaAa = float()
        self.mDisplayLow = float()
        self.mDisplayHigh = float()
        self.mDisplayNormalization = int()
        self.mSignalThreshold = float()
        self.mPhaseZero = float()
        self.mModZero = float()
        self.mDonor1Lifetime = float()
        self.mDonor1X = float()
        self.mDonor1Y = float()
        self.mDonor2Lifetime = float()
        self.mTwoLifetimeRatio = float()
        self.mMainFrequency = float()
        self.mPhaseFlatFieldCorrected = bool()
        self.mModulationFlatFieldCorrected = bool()
        self.mNumPhases = int()
        self.mDarkValue = int()
        self.mFRETMethod = int()
        self.mFRETAddParameter = float()

class CHistogramRecord70(BaseDecoder):
    """ generated source for class CHistogramRecord70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mMin = int()
        self.mMax = int()
        self.mMean = float()
        self.mHistogramType = int()
        self.mNumBins = int()
        self.mDataBlockSize = int()
        self.mChannelIndex = int()
        self.mImageIndex = int()

class CImageRecord70(BaseDecoder):
    """ generated source for class CImageRecord70 """
    def __init__(self):
        self.mStructID = int()
        self.mStructVersion = int()
        self.mByteOrdering = int()
        self.mStructLen = int()
        self.mYear = int()
        self.mMonth = int()
        self.mDay = int()
        self.mHour = int()
        self.mMinute = int()
        self.mSecond = int()
        self.mImported = bool()
        self.mNotesLen = int()
        self.mNotesPtr = int()
        self.mWidth = int()
        self.mHeight = int()
        self.mNumPlanes = int()
        self.mNumChannels = int()
        self.mChannelPtr = int()
        self.mNumTimepoints = int()
        self.mNumMasks = int()
        self.mMaskPtr = int()
        self.mNumViews = int()
        self.mViewPtr = int()
        self.mXYInterpolationFactor = int()
        self.mZInterpolationFactor = int()
        self.mImageGroupIndex = int()
        self.mAnnotationTablePtr = int()
        self.mElapsedTimeTablePtr = int()
        self.mSAPositionTablePtr = int()
        self.mStagePositionTablePtr = int()
        self.mAuxDataTablePtr = int()
        self.mNumAuxDataTables = int()
        self.mThumbNail = [0]
        self.mElapsedTimeOffset = int()
        self.mName = str()
        self.mInfo = str()
        self.mUniqueId = str()
        self.mLensDef = CLensDef70()
        self.mMainViewRecord = CMainViewRecord70()
        self.mOptovarDef = COptovarDef70()

    def Decode(self, inNode):
        """ generated source for method Decode """
        self.mLensDef = CLensDef70()
        self.mMainViewRecord = CMainViewRecord70()
        self.mOptovarDef = COptovarDef70()
        theLastIndex = super().Decode(inNode, 0)
        theLastIndex = self.mLensDef.Decode(inNode, theLastIndex)
        theLastIndex = self.mOptovarDef.Decode(inNode, theLastIndex)
        theLastIndex = self.mMainViewRecord.Decode(inNode, theLastIndex)
        return theLastIndex

class CUnknownAnnotation70(BaseDecoder):
    """ generated source for class CUnknownAnnotation70 """
    def __init__(self):
        self.mAnn = CAnnotation70()

    def Decode(self, inNode, inStartIndex):
        """ generated source for method Decode """
        self.mAnn = CAnnotation70()
        theLastIndex = super().Decode(inNode, inStartIndex)
        theLastIndex = self.mAnn.Decode(inNode, theLastIndex)
        return theLastIndex
