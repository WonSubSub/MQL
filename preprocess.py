import pandas as pd
from collections import defaultdict
from scipy.stats import boxcox
from sklearn.preprocessing import StandardScaler


def str_value_preprocess(data: str) -> str:
    '''
    [description]
    categorical column의 데이터 전처리
    ex) End-customer, end_Customer --> endcostumer

    [arguments]
    data : 데이터
    '''
    if pd.isna(data):
        return data
    elif type(data)==int:
        return data
    return ''.join(data.lower().replace('/', '').replace('-', '').replace('_', '').replace('.', '').split())


def preprocess_ldlen(length: int, med: float) -> float:
    '''
    [description]
    lead_desc_length(고객 요구사항의 길이) 컬럼의 전처리를 위한 함수
    EDA.ipynb 참고

    [arguments]
    length : 고객 요구사항의 길이
    med : 중간값
    '''
    if length == 14:
        length = 0
    elif length == 3:
        length = med
    return length


def preprocess_categorical(dataset: pd.DataFrame, 
                           categorial_columns: list, 
                           is_train: bool, 
                           cnt: int, 
                           column_maps=defaultdict(dict), 
                           ) -> [pd.DataFrame, defaultdict(dict)]:
    '''
    [description]
    categorical column을 인코딩하는 함수
    ['customer_type', 'customer_position', 'expected_timeline'] --> ordinal encoding
    나머지는 컬럼에 대해서는 출연 빈도가 cnt 이상인 값에 대해서만 label encoding

    [arguments]
    dataset : 데이터셋
    categorical_columns : 해당 데이터셋의 범주형 컬럼들
    is_train : 해당 데이터셋이 학습 데이터셋인지
    cnt : label encoding을 위한 최소 출연 빈도
    column_maps : 컬럼의 인코딩을 위한 {column_name : dictionary} 형태의 딕셔너리
    '''
    if is_train:
        mapping_values=defaultdict(list)
        mapping_values['customer_type'] = ['endcustomer', 'specifierinfluencer', 'channelpartner', 'servicepartner', 'solutionecopartner', 'others']
        mapping_values['customer_position'] = ['manager', 'ceofounder', 'director', 'associateanalyst', 'partner', 'entrylevel', 'clevelexecutive', 'intern', 'vicepresident', 'trainee', 'others']
        mapping_values['expected_timeline'] = ['lessthan3months', '3months~6months', 'morethanayear', '6months~9months', '9months~1year', 'others']
        for column in categorial_columns:
            dataset[column] = dataset[column].apply(lambda x: str_value_preprocess(x))

            if not mapping_values[column]:
                column_vc = dataset[column].value_counts()
                
                # if len(mapping_values) > 15:
                value_for_map = column_vc[column_vc>cnt].index
                mapping_values[column] = list(value_for_map)
                # else:
                    # mapping_values[column] = list(dataset[column].unique())
            
            dataset[column] = dataset[column].apply(lambda x: x if x in mapping_values[column] else 'others')
            dataset[column] = dataset[column].apply(lambda x: 'others' if x in ['other', 25096] else x)

            column_maps[column] = {v:i for i,v in enumerate(dataset[column].unique())}
            dataset[column] = dataset[column].map(column_maps[column])

    else:
        for column in categorial_columns:
            dataset[column] = dataset[column].apply(lambda x: str_value_preprocess(x))
            if 'others' in column_maps[column].keys():
                dataset[column] = dataset[column].map(column_maps[column]).fillna(column_maps[column]['others'])
            else:
                dataset[column] = dataset[column].map(column_maps[column])
            
    return dataset, column_maps


def preprocess_continuous(dataset: pd.DataFrame, 
                        continuous_columns: list, 
                        is_train: bool, 
                        optimal_lambdas=defaultdict(float), 
                        scaler=StandardScaler()
                        ) -> [pd.DataFrame, defaultdict(float), StandardScaler()]:
    '''
    [description]
    categorical column을 인코딩하는 함수
    ['customer_type', 'customer_position', 'expected_timeline'] --> ordinal encoding
    나머지는 컬럼에 대해서는 출연 빈도가 cnt 이상인 값에 대해서만 label encoding

    [arguments]
    dataset : 데이터셋
    continuous_columns : 해당 데이터셋의 연속형 컬럼들
    is_train : 해당 데이터셋이 학습 데이터셋인지
    optimal_lambdas : 컬럼의 분포 변환 lambda값 저장을 위한 {column_name : float} 형태의 딕셔너리
    scaler : 정규화를 위한 standard scaler
    '''
    if is_train:
        med = dataset['lead_desc_length'].median()
        dataset['lead_desc_length'] = dataset['lead_desc_length'].apply(lambda x: preprocess_ldlen(x, med))

        for column in continuous_columns:
            dataset[column] = dataset[column].fillna(0).apply(lambda x: x+1)

            dataset[column], op_lambda = boxcox(dataset[column])
            optimal_lambdas[column] = op_lambda
        
        scaled_dataset = pd.DataFrame(scaler.fit_transform(dataset[continuous_columns]))
        for idx, col in enumerate(continuous_columns):
            dataset[col] = list(scaled_dataset[idx])

    else:
        med = dataset['lead_desc_length'].median()
        dataset['lead_desc_length'] = dataset['lead_desc_length'].apply(lambda x: preprocess_ldlen(x, med))

        for column in continuous_columns:
            dataset[column] = dataset[column].fillna(0).apply(lambda x: x+1)

            dataset[column] = boxcox(dataset[column], lmbda=optimal_lambdas[column])
        
        scaled_dataset = pd.DataFrame(scaler.transform(dataset[continuous_columns]))
        for idx, col in enumerate(continuous_columns):
            dataset[col] = list(scaled_dataset[idx])

    return dataset, optimal_lambdas, scaler


def select_columns(dataset: pd.DataFrame) -> pd.DataFrame:
    '''
    [description]
    학습에 사용될 컬럼을 제외한 나머지 컬럼을 drop하는 함수

    [arguments]
    dataset : 데이터셋
    '''
    dataset = dataset.drop(columns=[
                              'bant_submit',
                              # 'business_unit',
                              # 'inquiry_type',
                              # 'customer_position',
                              # 'expected_timeline',
                              # 'business_area',
                              # 'historical_existing_cnt',
                              # 'lead_desc_length',
                              # 'response_corporate',
                              # 'product_category',
                              'product_subcategory',
                              'product_modelname',
                            #   'customer_idx',
                              # 'customer_job',
                            #   'lead_owner',
                              # 'budget',
                              'customer_type',
                              ])
    
    return dataset


def preprocess_dataset(args, train_set: pd.DataFrame, test_set: pd.DataFrame) -> [pd.DataFrame, pd.DataFrame]:
    '''
    [description]
    학습에 활용할 데이터셋의 전체 전처리를 처리하는 함수

    [arguments]
    train_set : 학습 데이터셋
    test_set : 평가 데이터셋
    '''
    train_set, test_set = select_columns(train_set), select_columns(test_set)

    all_columns = train_set.columns
    continuous_columns = args.continuous_columns
    categorical_columns = [col for col in all_columns if col not in continuous_columns]

    train_set, column_maps = preprocess_categorical(train_set, categorical_columns, is_train=True, cnt=args.cnt)
    test_set, _= preprocess_categorical(test_set, categorical_columns, is_train=False, cnt=args.cnt, column_maps=column_maps)

    train_set, optimal_lambdas, scaler = preprocess_continuous(train_set, continuous_columns, is_train=True)
    test_set, _, _ = preprocess_continuous(test_set, continuous_columns, is_train=False, optimal_lambdas=optimal_lambdas, scaler=scaler)

    return train_set, test_set