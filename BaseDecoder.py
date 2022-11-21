__copyright__  = "Copyright (c) 2022, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."

import yaml
import re

class BaseDecoder(object):
    def __init__(self):
        self.ClassName = self.__class__.__name__
        #print ("Base is: ", self.__class__.__name__)


    def RestoreSpecialCharacters(self, inString):
        ouString = inString
        ouString = re.sub("_#9;", "\t",ouString)
        ouString = re.sub("_#10;", "\n",ouString)
        ouString = re.sub("_#13;", "\r",ouString)
        ouString = re.sub("_#34;", "\"",ouString)
        ouString = re.sub("_#58;", ":",ouString)
        ouString = re.sub("_#92;", '/',ouString) # I am getting an escape error if I give "\\" ?????
        ouString = re.sub("_#91;", "[",ouString)
        ouString = re.sub("_#93;", "]",ouString)
        ouString = re.sub("_#124;", "|",ouString)
        ouString = re.sub("_#60;", "<",ouString)
        ouString = re.sub("_#62;", ">",ouString)
        ouString = re.sub("_#32;", " ",ouString)
        ouString = re.sub("__empty", "",ouString)
        return ouString

    def GetStringValue(self, inNode, inStartIndex, inKeyname, inRestoreSpecialValues):

        theValueClassList = inNode.value
        for theNodeIndex in range(inStartIndex, len(theValueClassList)):
            theTuple = theValueClassList[theNodeIndex]
            if theTuple[0].value == inKeyname:
                theValue = theTuple[1].value
                if inRestoreSpecialValues:
                    theValue = self.RestoreSpecialCharacters(theValue)
                return theValue, theNodeIndex + 1
            theNodeIndex += 1
        return "", -1

    def GetIntValue(self, inNode, inStartIndex, inKeyname):
        theValueString, theNextIndex = self.GetStringValue(inNode, inStartIndex, inKeyname, False)
        if not theNextIndex == -1:
            return int(theValueString), theNextIndex

        return -1,-1

    def GetStringArray(self, inNode, inLogName, inFirstIsSize, inRestoreSpecialValues):
        theArray = []
        if not isinstance(inNode,yaml.nodes.SequenceNode):
            return theArray
        theList = inNode.value
        if len(theList) < 1:
            return theArray
        #theOff = 1 if inFirstIsSize else 0
        for theListNode in range(len(theList)):
            theAttrValue = theList[theListNode].value
            if theListNode == 0 and inFirstIsSize:
                if not int(theAttrValue) == len(theList)-1:
                    print("Error: List Size mismatch")
                continue
            if inRestoreSpecialValues:
                theAttrValue = self.RestoreSpecialCharacters(theAttrValue)
            theArray.append(theAttrValue)

        return theArray
        
    def GetIntArray(self, inNode, inLogName, inFirstIsSize):

        theIntArray = []
        theStringArray = self.GetStringArray(inNode,inLogName,inFirstIsSize,False)
        if len(theStringArray) == 0:
            return theIntArray
        for theString in theStringArray:
            theIntArray.append(int(theString))

        return theIntArray

    def GetFloatArray(self, inNode, inLogName, inFirstIsSize):

        theFloatArray = []
        theStringArray = self.GetStringArray(inNode,inLogName,inFirstIsSize,False)
        if len(theStringArray) == 0:
            return theFloatArray
        for theString in theStringArray:
            theFloatArray.append(float(theString))

        return theFloatArray

    def DecodeUnknownString(self, inUnknownString, inAttrKeyNode):
        return False

    def Decode(self,inNode, inStartIndex = 0):
        debugDecode = False
        v =  vars(self).items()
        #print ("v is: ",v)
        theDict = {"":""}
        for x,y in v:
            theDict[x] = type(y).__name__

        if debugDecode:
            print("theDict is: ",theDict)

        theValueClassList = inNode.value
        if debugDecode:
            print("\n\ntheValueClassList size ",len(theValueClassList) )
        if debugDecode:
            print("\n\ntheValueClassList[0] ",theValueClassList[0] )
        if debugDecode:
            print("\n\ntheValueClassList[1] ",theValueClassList[1] )
        theClassIndex = -1
        for theIter in theValueClassList:
            theClassIndex += 1
            if theClassIndex < inStartIndex : 
                continue

            if debugDecode:
                print ("theIter : ",theIter)
            theKeyNode = theIter[0]
            if debugDecode:
                print ("tuple len: ",len(theIter))
            s = theKeyNode.value

            if theKeyNode.value == 'EndClass':
                break
            if theKeyNode.value != 'StartClass':
                continue
            theValueMappingNode = theIter[1]
            theValueAttributeList = theValueMappingNode.value
            theAttrIndex = -1;
            for theAttrKeyNode in theValueAttributeList:
                theAttrIndex += 1
                theAttrValueNode = theAttrKeyNode[0]
                theAttrName = theAttrValueNode.value
                if debugDecode:
                    print ("theAttrName is: ",theAttrName)
                if theAttrName not in theDict and theAttrIndex > 0:
                    res = self.DecodeUnknownString(theAttrName,theAttrKeyNode);
                    if not res:
                        if not theAttrName.startswith("Struct"):
                            print ("theAttrName not in theDictionary: ",theAttrName)
                    continue
                if isinstance(theAttrValueNode,yaml.nodes.ScalarNode):
                    if debugDecode:
                        print ("is a Scalar Node")
                    if theAttrIndex == 0:
                        if theAttrName != "ClassName":
                            break;
                        continue
                    theAttrValue = theAttrKeyNode[1].value
                    if debugDecode:
                        print ("theAttrValue is: ",theAttrValue)
                    theType = theDict[theAttrName]
                    if theType == 'int':
                        if debugDecode:
                            print ("is an int")
                        setattr(self,theAttrName,int(theAttrValue))
                    elif theType == 'float':
                        if debugDecode:
                            print ("is an float")
                        setattr(self,theAttrName,float(theAttrValue))
                    elif theType == 'bool':
                        if debugDecode:
                            print ("is an bool")
                        if theAttrValue == 'true':
                            setattr(self,theAttrName,True)
                        else:
                            setattr(self,theAttrName,False)
                        pass
                    elif theType == 'str':
                        if debugDecode:
                            print ("is a string")
                        theAttrValue = self.RestoreSpecialCharacters(theAttrValue)
                        setattr(self,theAttrName,theAttrValue)

                    elif theType == 'list':
                        l = len(theAttrValue)
                        m = getattr(self,theAttrName)
                        theType = type(m[0]).__name__
                        theTempList = []
                        for theListVal in theAttrValue:
                            if theType == 'int':
                                theTempList.append(int(theListVal.value))
                            elif theType == 'float':
                                theTempList.append(float(theListVal.value))
                            elif theType == 'bool':
                                if theListVal.value == 'true':
                                    theTempList.append(True)
                                else:
                                    theTempList.append(False)

                        setattr(self,theAttrName,theTempList)

                elif isinstance(theAttrValueNode,yaml.nodes.SequenceNode):
                    if debugDecode:
                        print ("is a Sequence Node")
                pass
            pass
        pass
        if debugDecode:
            print ("v is: ",v)
        return theClassIndex +1

    def FindNextClass(self, inNode, inStartIndex):
        theValueClassList = inNode.value
        for theClassIndex in range(inStartIndex, len(theValueClassList)):
            theKeyNode = theValueClassList[theClassIndex]

            theStr = theKeyNode[0].value

            if theStr == "EndClass":
                break
            if not theStr == "StartClass":
                continue 
            theMappingNode = theKeyNode[1]
            theNodeList = theMappingNode.value
            theNodeName = theNodeList[0][0].value
            theNodeValue = theNodeList[0][1].value
            if not theNodeName == "ClassName":
                #is an error
                break
            return theNodeValue, theClassIndex
        return "", -1


    def GetSBClassName(self):
        sbName = self.__class__.__name__
        sbName = re.sub(".*\\$", "",sbName)
        sbName = re.sub(".*\\.", "",sbName)
        return sbName


