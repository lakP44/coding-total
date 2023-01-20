import os
import pandas as pd
from sklearn.impute import KNNImputer

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
def check_unique(data, feature, num1):
    '''
    data = data, feature = 원하는 feature 리스트를 넣을 수 있습니다, 0으로 설정하면 모든 feature가 들어갑니다, num1 = 출력할 nunique의 개수 기준을 지정합니다 ex) 3이면 3이상의 nunique를 가진 feature만 출력됨
    '''
    if feature == 0:
        feature = list(data.columns)

    name = []
    num = []
    real_name = []

    for i in feature:
        if data[i].nunique() >= num1:
            real_name.append(i)
            name.append(data[i].unique())
            num.append(data[i].nunique())
    unique_df1 = pd.DataFrame({'real_name' : real_name , 'name' : name, 'num' : num})
    unique_df1.sort_values(by = 'num', inplace = True)
    return unique_df1