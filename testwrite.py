# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:53:15 2015

@author: Owen
"""

import scipy.io.wavfile as wavfile
import numpy as np
[rate,sample] = wavfile.read("sample.wav")
data = np.array(sample, dtype=np.float64)
print(data[0])