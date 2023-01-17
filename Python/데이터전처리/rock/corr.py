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