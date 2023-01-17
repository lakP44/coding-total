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

##############################################################################################################

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

##############################################################################################################

def checkNAN(df):
    '''
    df = data
    data의 nan 상태 DataFrame을 만들어 return함
    '''
    train_nan = list(df.isna().sum())
    num_nan = list(filter(lambda x:x >= 1, train_nan)) # nan값이 1개 이상인 친구만 보여줌

    index_nan = list(filter(lambda e:train_nan[e] >= 1, range(len(train_nan)))) # 이건 인덱스

    nan_df = pd.DataFrame({'index_in_train' : index_nan, 'column_name' : df.iloc[:, index_nan].columns, 'NAN_number' : num_nan})
    
    return nan_df

##############################################################################################################
# 간단한 결측치 처리 자동화 코드

def handle_NAN(df, list_lists, fill_na, fill_value, back_fill, front_fill, linear, KNN):
    '''
    df = data, list_lists = 결측치 처리를 원하는 컬럼을 이중 리스트로 넣어줌 ex) [['Age'], ['Embarked', 'Cabin']]
    fill_na = [처리할 순서, 채울 값], fill_value = [처리할 순서, 채울 값들 ex) ['S', 'S']], back_fill = 처리할 순서
    front_fill = 처리할 순서, linear = 처리할 순서, KNN = [처리할 순서, n_neighbors 값]
    '''
    imputer = KNNImputer(n_neighbors = KNN[1])

    fill_val_dict = {}
    if fill_value[0] != -1:
        for i in range(len(fill_value[1])):
            fill_val_dict[list_lists[fill_value[0]][i]] = fill_value[1][i]
        
    sequence = {fill_na[0] : "df[" + str(list_lists[fill_na[0]]) + "].fillna(" + str(fill_na[1]) + ")", 
                fill_value[0] : "df[" + str(list_lists[fill_value[0]]) + "].fillna(" + str(fill_val_dict) + ")", 
                back_fill : "df[" + str(list_lists[back_fill]) + "].fillna( method='bfill' )",
                front_fill : "df[" + str(list_lists[front_fill]) + "].fillna( method='ffill' )",
                linear : "df[" + str(list_lists[linear]) + "].interpolate(method='linear')",
                KNN[0] : "imputer.fit_transform(df[" + str(list_lists[KNN[0]]) + "])",
                }
    
    del sequence[-1]

    sequence_sort = dict(sorted(sequence.items()))

    for n in range(len(sequence_sort)):
        if "KNN" in sequence_sort[n]:
            df[list_lists[KNN[0]]]=pd.DataFrame(eval(sequence_sort[n]), columns=list_lists[KNN[0]])
        else:
            df[list_lists[n]] = eval(sequence_sort[n])
    return df

##############################################################################################################
# 간단한 결측치 자동 처리기 미리보기

##########################################################################################
# 아래의 숫자는 파라미터입니다. 0부터 코드가 시작되며 결측치가 처리됩니다.
# fill_na의 [0]은 순서, [1]은 채워지는 값입니다.
# fill_value의 [0]은 순서, [1]은 정해주는 컬럼마다 채워지는 값입니다. ex) ['Age'. 'Fare'], [1, 2]이면 // Age는 1, Fare은 2로 채워짐
# col_list에는 리스트 형태로 컬럼명을 넣어주면 됩니다.
##########################################################################################

def NAN_preview(data, col_list, fill_na, fill_value, back_fill, front_fill, linear, KNN):
    '''
    df = data, list_lists = 결측치 처리를 원하는 컬럼을 이중 리스트로 넣어줌 ex) [['Age'], ['Embarked', 'Cabin']]
    fill_na = [처리할 순서, 채울 값], fill_value = [처리할 순서, 채울 값들 ex) ['S', 'S']], back_fill = 처리할 순서
    front_fill = 처리할 순서, linear = 처리할 순서, KNN = [처리할 순서, n_neighbors 값]
    
    handle_NAN의 미리보기 코드입니다. 위의 방식대로 값을 넣으면 어떤 방식으로 처리되는지 프로세스를 DataFrame으로 반환합니다.
    '''
    nan_df = checkNAN(data)
    display(nan_df)
    print('=='*20)

    sequence_view = [data, col_list, fill_na, fill_value, back_fill, front_fill]
    sequence_num = sequence_view[2 : len(sequence_view)]

    sequence_dic = pd.DataFrame({'func' : [fill_na[0], fill_value[0], back_fill, front_fill, linear, KNN[0]], 
                                'func_list' : ['fill_na', 'fill_value', 'backfill', 'front_fill', 'linear', 'KNN'], 
                                'parameter' : [fill_na[1], fill_value[1], 'none', 'none', 'none', KNN[1]]})
    sequence_dic = sequence_dic.sort_values('func')


    display(sequence_dic)

    sequence_dic = sequence_dic[sequence_dic['func'] >= 0]
    sequence_dic['columns'] = col_list
    print('=='*20)
    display(sequence_dic)
    
##############################################################################################################
def check_features(data):
    '''
    data = data
    first is categorical, second is numerical <== 범주형 변수와 수치형 변수의 리스트를 순서대로 반환합니다.
    '''
    cat = list(set(list(data.select_dtypes("object").columns) + list(data.select_dtypes("bool").columns) + list(data.select_dtypes("category").columns)))
    num = list(set(list(data.select_dtypes("int").columns) + list(data.select_dtypes("float").columns)))
    # include_word_feats1 = [s for s in data if "변수에 포함된 단어" in s]
    # include_word_feats2 = [s for s in data if "변수에 포함된 단어" in s]
    print(cat)
    print(num)
    
    return cat, num

##############################################################################################################

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
    
##############################################################################################################
# p-value df 생성 코드, (p-value는 보통 0.05 이하이면 신뢰성이 있다고 본다, 0.05이하라는건 신뢰도가 95% 이상이라는 것)

def make_pvalue_df(data, feature_list, p_value_v, target):
    '''
    data = data, feature_list = 원하는 피쳐들, p_value_v = p_value의 값 설정 (보통 0.05), target = target_feature에 대해서만 구하고 싶다면 ex) 'Survived
    그게 아니라면 0으로 설정
    
    p-value df 생성 코드, (p-value는 보통 0.05 이하이면 신뢰성이 있다고 본다, 0.05이하라는건 신뢰도가 95% 이상이라는 것)
    '''
    printList = list(combinations(feature_list, 2))

    name1 = []
    name2 = []
    corr = []
    pval = []

    if target == 0:
        for i in printList:
            test1 = spst.pearsonr(data[i[0]], data[i[1]])
            name1.append(i[0])
            name2.append(i[1])
            corr.append(float(format(test1[0], '.6f')))
            pval.append(float(format(test1[1], '.6f')))
    else:
        for n in feature_list:
            for ad in target:
                test2 = spst.pearsonr(data[n], data[ad])
                name1.append(n)
                name2.append(ad)
                corr.append(float(format(test2[0], '.6f')))
                pval.append(float(format(test2[1], '.6f')))
    pval_df = pd.DataFrame({'name1' : name1, 'name2' : name2, 'corr' : corr, 'p-value' : pval})
    pval_df = pval_df.loc[pval_df['p-value'] <= p_value_v]
    pval_df = pval_df.sort_values('corr')
            
    return pval_df

##############################################################################################################
# 회색줄 = 신뢰구간이 서로 안겹칠수록 둘사이의 연관이 큼, ex) sc는 훌륭함, cq는 그냥 그럼

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
    
##############################################################################################################
# t-test df 생성 코드, (t score는 보통 -2 이하, 2 이상이면 변수간의 연관성이 있다고 본다)

def make_ttest_df(data, nume, p_value_v, cat):
    '''
    data = data, nume = 수치형 변수들, p_value_v = p_value의 값 설정 (보통 0.05), cat =  범주형 변수 하나 <== 둘 이상 넣지 말것 ex) Survived
    
    t-test df 생성 코드, (t score는 보통 -2 이하, 2 이상이면 변수간의 연관성이 있다고 본다)
    '''
    if cat in nume:
        nume.remove(cat)
    
    name1 = []
    name2 = []
    corr = []
    pval = []

    for n in nume:
        tt1 = data.loc[data[cat] == data[cat].unique()[0], n]
        tt2 = data.loc[data[cat] == data[cat].unique()[1], n]
        test2 = spst.ttest_ind(tt1, tt2)
        name1.append(n)
        name2.append(cat)
        corr.append(float(format(test2[0], '.6f')))
        pval.append(float(format(test2[1], '.6f')))
        
    ttest_df = pd.DataFrame({'name1' : name1, 'name2' : name2, 'statistic' : corr, 'p-value' : pval})
    ttest_df = ttest_df.loc[ttest_df['p-value'] <= p_value_v]
    ttest_df = ttest_df.sort_values('statistic')

    return ttest_df

##############################################################################################################
# ANOVA df 생성 코드, (f score는 보통 2~3 이상이면 변수간의 연관성이 있다고 본다)

def make_ANOVA_df(data, nume, p_value_v, cat):
    '''
    data = data, nume = 수치형 변수들, p_value_v = p_value의 값 설정 (보통 0.05), cat =  범주형 변수들 <== 둘 이상 넣기 가능
    
    ANOVA df 생성 코드, (f score는 보통 2~3 이상이면 변수간의 연관성이 있다고 본다)
    '''
    if cat in nume:
        nume.remove(cat)
    
    name1 = []
    name2 = []
    x = []
    anova = []
    pval = []

    for n in nume:
        for asd in cat:
            count = 0
            for a in range(data[asd].nunique()):
                globals()["an{}".format(count)] = data.loc[data[asd] == list(data[asd].unique())[count], n]
                count += 1
            x = "an0"
            for od in range(1, len(data[asd].unique())):
                x = x + ", an" + str(od)
            x1 = "spst.f_oneway(" + x + ")"
            test2 = eval(x1)
            name1.append(n)
            name2.append(asd)
            anova.append(float(format(test2[0], '.6f')))
            pval.append(float(format(test2[1], '.6f')))
        
    anova_df = pd.DataFrame({'name1' : name1, 'name2' : name2, 'anova-statistic' : anova, 'p-value' : pval})
    anova_df = anova_df.loc[anova_df['p-value'] <= p_value_v]
    anova_df = anova_df.sort_values('anova-statistic')

    return anova_df
