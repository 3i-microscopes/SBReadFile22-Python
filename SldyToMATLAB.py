__copyright__  = "Copyright (c) 2022-2025, Intelligent Imaging Innovations, Inc. All rights reserved.  All rights reserved."
__license__  = "This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree."

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import os
import matlab.engine


# In[25]:


def open_npy_file(path, cap_number, channel):
    for i in os.listdir(path):
        #finding the .imgdir for the capture you are interested in 
        if cap_number and ".imgdir" in i:
            b=i
    new_path=os.path.join(path, str(b))
    for q in os.listdir(new_path):
        #finding the npy file for the channel you are interested in 
        if channel and "ImageData" in q:
            c=q
    newer_path=os.path.join(new_path, str(c))
    #opens the npy file that has your channel data in it 
    print("Opening ",newer_path)
    im=np.load(newer_path)
    return (im)


# In[29]:


test_see=open_npy_file('C:\Data\Slides_msi\QweekTour.dir',"Metaphase B-Cell - 1-1646218556-536","Ch0")
#directory of the sldy file
#the capture you are interested in 
#the channel that your data is on
np.shape(test_see)


# In[ ]:


eng = matlab.engine.connect_matlab()


# In[28]:
#in matlab, crate share session 
# >>matlab.engine.shareEngine('Python')
# from matlab connect a shared secssion
# name=matlab.engine.find_matlab()
# eng.workspace[name[0]] = array

eng.workspace['MATLAB_10144'] = test_see
#send array to matlab workspace 

