#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import tensorflow.compat.v2 as tf
from PIL import Image


# In[2]:


model = tf.keras.models.load_model('age_model.h5')


# In[3]:


X = []
width = 100
height = 200

image = Image.open('jy.jpg')
image = image.convert('RGB')
image = image.resize((width, height))
X.append(np.array(image))


# In[4]:


X = np.array(X)
X = X.astype('float32')
X /= 255.0


# In[5]:


result = model.predict(X)


# In[6]:


result


# In[ ]:




