import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import os
import warnings # 경고메세지 무시
warnings.simplefilter(action='ignore', category=FutureWarning)

def createFolder(directory):
    '''
    directory = 폴더명
    폴더 생성 코드, string 형태로 설정한 값을 이름으로 갖는 폴더가 생성됨
    '''
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def make_corr_heatmap(df):
    '''
    df = data
    data를 넣으면 자동으로 깔끔한 상관계수 히트맵을 그려줍니다.
    '''
    plt.figure(figsize = (8, 8))
    mask = np.zeros_like(df.corr(), dtype=bool) # corr을 다른 것으로 바꾸면 다른 상관계수 그래프를 그릴 수도 있음
    mask[np.triu_indices_from(mask)] = True
    sns.heatmap(df.corr(), annot = True, fmt = '.3f', mask = mask, cmap = 'RdYlBu_r',  vmin = -1, vmax = 1)
    plt.show()
        
##############################################################################################################
# distplot 자동 생성기

def make_distplots(data, feature_list):
    '''
    data = data, feature_list = distplot을 그리고 싶은 모든 feature
    feature_list의 모든값을 distplot으로 그려주고, 이미지 파일을 저장합니다.
    '''
    dist_feature_list = feature_list

    createFolder('distplot')

    rcm = 1

    while True:
        if len(dist_feature_list) <= rcm ** 2:
            break
        else:
            rcm += 1

    count_index = 1

    for i in dist_feature_list:
        plt.subplot(rcm, rcm, count_index)
        
        sns.distplot(data[i], hist = True, bins = 16)

        plt.title(i)
        plt.tight_layout()
        plt.savefig('distplot\\dist')
            
        count_index += 1
    plt.show()
    
##############################################################################################################
# boxplot 자동 생성기

def make_boxplots(data, feature_list):
    '''
    data = data, feature_list = boxplot을 그리고 싶은 모든 feature
    feature_list의 모든값을 boxplot으로 그려주고, 이미지 파일을 저장합니다.
    '''
    dist_feature_list = feature_list

    createFolder('boxplot')

    rcm = 1

    while True:
        if len(dist_feature_list) <= rcm ** 2:
            break
        else:
            rcm += 1

    count_index = 1

    for i in dist_feature_list:
        plt.subplot(rcm, rcm, count_index)
        
        sns.boxplot(data = data, x = data[i])

        plt.title(i)
        plt.tight_layout()
        plt.savefig('boxplot\\box')
            
        count_index += 1
    plt.show()
    
def make_barplots(data, feature_list, target):
    '''
    data = data, feature_list = barplot을 그리고 싶은 모든 feature, target = y축
    feature_list의 모든값을 barplot으로 그려주고, 이미지 파일을 저장합니다.
    
    회색줄 = 신뢰구간이 서로 안겹칠수록 둘사이의 연관이 큼, ex) sc는 훌륭함, cq는 그냥 그럼
    '''
    dist_feature_list = feature_list

    createFolder('barplot')

    rcm = 1

    while True:
        if len(dist_feature_list) <= rcm ** 2:
            break
        else:
            rcm += 1

    count_index = 1

    for i in dist_feature_list:
        plt.subplot(rcm, rcm, count_index)
        
        sns.barplot(x = i, y = target, data = data)

        plt.title(i)
        plt.tight_layout()
        plt.savefig('barplot\\bar')
            
        count_index += 1
    plt.show()