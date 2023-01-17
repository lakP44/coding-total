import numpy as np
import pandas as pd
from itertools import *
import itertools

import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as spst
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer

import os

import warnings # 경고메세지 무시
warnings.simplefilter(action='ignore', category=FutureWarning)

import rock.corr    # calcpkg 패키지의 operation 모듈을 가져옴
import rock.plots     # calcpkg 패키지의 geometry 모듈을 가져옴
import rock.useful