import numpy as np

def uint16_to_bytes(inVal):
    theArray = np.array([inVal],np.uint16)
    theBytes = theArray.tobytes()
    return theBytes

def int16_to_bytes(inVal):
    theArray = np.array([inVal],np.int16)
    theBytes = theArray.tobytes()
    return theBytes

def uint32_to_bytes(inVal):
    theArray = np.array([inVal],np.uint32)
    theBytes = theArray.tobytes()
    return theBytes

def int32_to_bytes(inVal):
    theArray = np.array([inVal],np.int32)
    theBytes = theArray.tobytes()
    return theBytes

def uint64_to_bytes(inVal):
    theArray = np.array([inVal],np.uint64)
    theBytes = theArray.tobytes()
    return theBytes

def int64_to_bytes(inVal):
    theArray = np.array([inVal],np.int64)
    theBytes = theArray.tobytes()
    return theBytes

def float32_to_bytes(inVal):
    theArray = np.array([inVal],np.float32)
    theBytes = theArray.tobytes()
    return theBytes

def float64_to_bytes(inVal):
    theArray = np.array([inVal],np.float64)
    theBytes = theArray.tobytes()
    return theBytes

def string_to_bytes(inString):
    theBytes = str.encode(inString)
    return theBytes

def bytes_to_string(inBytes):
    theString = inBytes.decode()
    #print('inBytes ',inBytes, flush=True)
    #print('theString',theString, flush=True)
    return theString

def bytes_to_int32(inBytes):
    theArr = np.frombuffer(inBytes,np.int32)
    return theArr

def bytes_to_float32(inBytes):
    theArr = np.frombuffer(inBytes,np.float32)
    return theArr

def type_to_bytes(inVal,inType):
    if(inType == 'u2'):
        theBytes = uint16_to_bytes(inVal)
    elif(inType == 'i2'):
        theBytes = int16_to_bytes(inVal)
    elif(inType == 'u4'):
        theBytes = uint32_to_bytes(inVal)
    elif(inType == 'i4'):
        theBytes = int32_to_bytes(inVal)
    elif(inType == 'u8'):
        theBytes = uint64_to_bytes(inVal)
    elif(inType == 'i8'):
        theBytes = int64_to_bytes(inVal)
    elif(inType == 'f4'):
        theBytes = float32_to_bytes(inVal)
    elif(inType == 'f8'):
        theBytes = float64_to_bytes(inVal)
    elif(inType == 's'):
        theBytes = string_to_bytes(inVal)

    return theBytes
    
def bytes_to_type(inBytes,inType):
    if(inType == 'u2'):
        theArr = np.frombuffer(inBytes,np.uint16)
    elif(inType == 'i2'):
        theArr = np.frombuffer(inBytes,np.int16)
    elif(inType == 'u4'):
        theArr = np.frombuffer(inBytes,np.uint32)
    elif(inType == 'i4'):
        theArr = np.frombuffer(inBytes,np.int32)
    elif(inType == 'u8'):
        theArr = np.frombuffer(inBytes,np.uint64)
    elif(inType == 'i8'):
        theArr = np.frombuffer(inBytes,np.int64)
    elif(inType == 'f4'):
        theArr = np.frombuffer(inBytes,np.float32)
    elif(inType == 'f8'):
        theArr = np.frombuffer(inBytes,np.float64)
    elif(inType == 's'):
        theArr = bytes_to_string(inBytes)

    return theArr
