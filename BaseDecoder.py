__copyright__  = "Copyright (c) 2022-2025, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."

import yaml
import re
import base64
import struct


class BaseDecoder(object):
    kEncodingAscii = "ascii"
    kEncodingBase64 = "base64"
    Encoding = kEncodingAscii

    def __init__(self):
        self.ClassName = self.__class__.__name__
        #print ("Base is: ", self.__class__.__name__)

    def DetectYamlEncoding(self,inPath):
        with open(inPath, "rt", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()

                if not stripped or stripped == "---":
                    continue

                if line.startswith("Encoding:"):
                    value = line[len("Encoding:"):].strip().lower()
                    value = value.strip('"')
                    print("DetectYamlEncoding: value is ",value)
                    if value in ("base64", "ascii"):
                        BaseDecoder.Encoding = value
                        return
                    raise ValueError(f"Unknown Encoding value: {value!r}")

                BaseDecoder.Encoding = "ascii"
                return

        BaseDecoder.Encoding = "ascii"
        return

    def DecodeBase64ToBytes(self,s: str) -> bytes:
        if s is None:
            raise ValueError("Input is None")
        return base64.b64decode(s.strip())

    def DecodeBase64ToString(self,s: str, encoding: str = "utf-8") -> str:
        return self.DecodeBase64ToBytes(s).decode(encoding)

    def DecodeBase64Scalar(self,s: str, fmt: str):
        """
        fmt:
          b  int8
          B  uint8
          h  int16
          Hp   uint16
          i  int32
          I  uint32
          q  int64
          Q  uint64
          f  float
          d  double
        Assumes little-endian.
        """
        data = self.DecodeBase64ToBytes(s)
        expected = struct.calcsize("<" + fmt)
        if len(data) != expected:
            raise ValueError(f"Expected {expected} bytes, got {len(data)}")
        return struct.unpack("<" + fmt, data)[0]

    def DecodeBase64Integer(self,s: str, signed: bool = True) -> int:
        data = base64.b64decode(s.strip())
        n = len(data)

        if n not in (1, 2, 4, 8):
            raise ValueError(f"Unsupported integer size: {n} bytes")

        return int.from_bytes(data, byteorder="little", signed=signed)

    def DecodeBase64Real(self,s: str) -> float:
        data = base64.b64decode(s.strip())
        n = len(data)

        if n == 4:
            return struct.unpack("<f", data)[0]
        elif n == 8:
            return struct.unpack("<d", data)[0]
        else:
            raise ValueError(f"Unsupported floating-point size: {n} bytes")

    def DecodeBase64Array(self,s: str, fmt: str):
        data = self.DecodeBase64ToBytes(s)
        item_size = struct.calcsize("<" + fmt)
        if len(data) % item_size != 0:
            raise ValueError(f"Byte count {len(data)} is not a multiple of {item_size}")
        count = len(data) // item_size
        return list(struct.unpack("<" + fmt * count, data))

    def EncodeBytesToBase64(self,data: bytes) -> str:
        return base64.b64encode(data).decode("ascii")

    def EncodeStringToBase64(self,s: str, encoding: str = "utf-8") -> str:
        return self.EncodeBytesToBase64(s.encode(encoding))

    def EncodeIntegerToBase64(self,value: int, num_bytes: int, signed: bool = True) -> str:
        """
        Encode a Python int into base64 using little-endian byte order.

        num_bytes must be 1, 2, 4, or 8.
        """
        if num_bytes not in (1, 2, 4, 8):
            raise ValueError(f"Unsupported integer size: {num_bytes} bytes")

        data = value.to_bytes(num_bytes, byteorder="little", signed=signed)
        return self.EncodeBytesToBase64(data)

    def EncodeFloatToBase64(self,value: float) -> str:
        """
        Encode as 4-byte IEEE float (little-endian).
        """
        data = struct.pack("<f", value)
        return self.EncodeBytesToBase64(data)

    def EncodeDoubleToBase64(self,value: float) -> str:
        """
        Encode as 8-byte IEEE double (little-endian).
        """
        data = struct.pack("<d", value)
        return self.EncodeBytesToBase64(data)

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

    def EncodeStringToString(self,inString):
        if(BaseDecoder.Encoding == self.kEncodingAscii):
            return inString
        elif(BaseDecoder.Encoding == self.kEncodingBase64):
            val = self.DecodeBase64ToString(inString)
            return val

    def EncodeStringToInt(self,inString):
        if(BaseDecoder.Encoding == self.kEncodingAscii):
            return int(inString)
        elif(BaseDecoder.Encoding == self.kEncodingBase64):
            val = self.DecodeBase64Integer(inString)
            return int(val)

    def EncodeStringToReal(self,inString):
        if(BaseDecoder.Encoding == self.kEncodingAscii):
            return float(inString)
        elif(BaseDecoder.Encoding == self.kEncodingBase64):
            val = self.DecodeBase64Real(inString)
            return float(val)

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
            theVal = self.EncodeStringToInt(theValueString)
            return int(theVal), theNextIndex

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
                #if not int(self.EncodeStringToInt(theAttrValue)) == len(theList)-1:
                if not int(self.EncodeStringToInt(theAttrValue)) == len(theList)-1:
                    print("Error: List Size mismatch")
                continue
            if inRestoreSpecialValues:
                if(BaseDecoder.Encoding == self.kEncodingAscii):
                    theAttrValue = self.RestoreSpecialCharacters(theAttrValue)
            #theAttrValue = self.EncodeStringToString(theAttrValue)
            theArray.append(theAttrValue)

        return theArray
        
    def GetIntArray(self, inNode, inLogName, inFirstIsSize):

        theIntArray = []
        theStringArray = self.GetStringArray(inNode,inLogName,inFirstIsSize,False)
        if len(theStringArray) == 0:
            return theIntArray
        for theString in theStringArray:
            theIntArray.append(int(self.EncodeStringToInt(theString)))

        return theIntArray

    def GetFloatArray(self, inNode, inLogName, inFirstIsSize):

        theFloatArray = []
        theStringArray = self.GetStringArray(inNode,inLogName,inFirstIsSize,False)
        if len(theStringArray) == 0:
            return theFloatArray
        for theString in theStringArray:
            theFloatArray.append(float(self.EncodeStringToReal(theString)))

        return theFloatArray

    def SetAttrInt(self, inAttrName, inAttrValue):
        if(BaseDecoder.Encoding == self.kEncodingAscii):
            setattr(self,inAttrName,int(inAttrValue))
        elif(BaseDecoder.Encoding == self.kEncodingBase64):
            val = self.DecodeBase64Integer(inAttrValue)
            setattr(self,inAttrName,int(val))

    def SetAttrFloat(self, inAttrName, inAttrValue):
        if(BaseDecoder.Encoding == self.kEncodingAscii):
            setattr(self,inAttrName,float(inAttrValue))
        elif(BaseDecoder.Encoding == self.kEncodingBase64):
            val = self.DecodeBase64Real(inAttrValue)
            setattr(self,inAttrName,float(val))

    def SetAttrString(self, inAttrName, inAttrValue):
        if(BaseDecoder.Encoding == self.kEncodingAscii):
            theAttrValue = self.RestoreSpecialCharacters(inAttrValue)
            setattr(self,inAttrName,theAttrValue)
        elif(BaseDecoder.Encoding == self.kEncodingBase64):
            val = self.DecodeBase64ToString(inAttrValue)
            setattr(self,inAttrName,val)

    def SetAttrBool(self, inAttrName, inAttrValue):
        if(BaseDecoder.Encoding == self.kEncodingAscii):
            if inAttrValue == 'true':
                setattr(self,inAttrName,True)
            else:
                setattr(self,inAttrName,False)
        elif(BaseDecoder.Encoding == self.kEncodingBase64):
            val = self.DecodeBase64Integer(inAttrValue)
            if val != 0:
                setattr(self,inAttrName,True)
            else:
                setattr(self,inAttrName,False)

    def ConvertToInt(self, inValue):
        if(BaseDecoder.Encoding == self.kEncodingAscii):
            return int(inValue)
        elif(BaseDecoder.Encoding == self.kEncodingBase64):
            val = self.DecodeBase64Integer(inValue)
            return int(val)

    def ConvertToFloat(self, inValue):
        if(BaseDecoder.Encoding == self.kEncodingAscii):
            return float(inValue)
        elif(BaseDecoder.Encoding == self.kEncodingBase64):
            val = self.DecodeBase64Real(inValue)
            return float(val)

    def ConvertToBool(self, inValue):
        if(BaseDecoder.Encoding == self.kEncodingAscii):
            if inValue == 'true':
                return True
            else:
                return False
        elif(BaseDecoder.Encoding == self.kEncodingBase64):
            val = self.DecodeBase64Integer(inValue)
            if val != 0:
                return True
            else:
                return False


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
            #s = theKeyNode.value

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
                        self.SetAttrInt(theAttrName,theAttrValue)
                    elif theType == 'float':
                        if debugDecode:
                            print ("is an float")
                        self.SetAttrFloat(theAttrName,theAttrValue)
                    elif theType == 'bool':
                        if debugDecode:
                            print ("is an bool")
                        self.SetAttrBool(theAttrName,theAttrValue)
                    elif theType == 'str':
                        if debugDecode:
                            print ("is a string")
                        self.SetAttrString(theAttrName,theAttrValue)

                    elif theType == 'list':
                        #l = len(theAttrValue)
                        m = getattr(self,theAttrName)
                        theType = type(m[0]).__name__
                        theTempList = []
                        for theListVal in theAttrValue:
                            if theType == 'int':
                                theTempList.append(int(self.ConvertToInt(theListVal.value)))
                            elif theType == 'float':
                                theTempList.append(float(self.ConvertToFloat(theListVal.value)))
                            elif theType == 'bool':
                                theTempList.append((self.ConvertToBool(theListVal.value)))

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

    def Encode(self,inClassName=None):
        str = '---\n'
        str = str + self.EncodeClass(inClassName)
        str = str + '...\n'
        return str


    def EncodeClass(self,inClassName=None):

        if inClassName is None:
            inClassName = self.__class__.__name__

        debugDecode = False
        v =  vars(self).items()
        #print ("v is: ",v)
        theDict = {"":""}
        theParts = []
        theIndent = '  '

        str = 'StartClass:'
        theParts.append(str)
        theParts.append("\n")

        theParts.append(theIndent)
        str = 'ClassName: ' + inClassName
        theParts.append(str)
        theParts.append("\n")

        for x,y in v:
            theDict[x] = type(y).__name__

        if debugDecode:
            print("theDict is: ",theDict)
        for theAttrName,theAttrType in v:
            theParts.append(theIndent)
            theParts.append(theAttrName+': ')

            theType = type(theAttrType).__name__
            theValue = getattr(self,theAttrName)
            if theType == 'int':
                str = self.EncodeIntegerToBase64(theValue,8)
            elif theType == 'float':
                str = self.EncodeFloatToBase64(theValue)
            elif theType == 'bool':
                if(theValue):
                    i = int(1)
                    str = self.EncodeIntegerToBase64(i,2)
                else:
                    i = int(0)
                    str = self.EncodeIntegerToBase64(i,2)
            elif theType == 'str':
                    str = self.EncodeStringToBase64(theValue)
            elif theType == 'list':
                print("Encode type is list, And now what???")
                str = "list"

            theParts.append(str)
            theParts.append("\n")

        str = 'EndClass:'
        theParts.append(str)
        theParts.append("\n")

        theOutputStr = "".join(theParts)
        return theOutputStr

