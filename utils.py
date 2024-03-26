from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
import pandas as pd
import random
import os
import numpy as np
from collections import deque


def seed_everything(seed):
    '''
    [description]
    seed 값을 고정시키는 함수

    [arguments]
    seed : seed 값
    '''
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)


def als_proba(als_rec: dict, dataset: pd.DataFrame, weight: float) -> list:
    '''
    [description]
    ALS 모델을 활용하여 예측된 확률값을 데이터셋의 각 인덱스별로 불러오는 함수

    [arguments]
    als_rec : ALS 모델의 예측값 {response_corporate: product_category} 형태의 딕셔너리
    dataset : 데이터셋
    weight : ALS 확률의 가중치
    '''
    als_pred = []
    for idx, row in dataset.iterrows():
        if (row['response_corporate'] in als_rec.keys()) and (row['product_category'] in als_rec[row['response_corporate']].keys()):
            als_pred.append(als_rec[row['response_corporate']][row['product_category']] * weight)
        else:
            als_pred.append(0)

    return als_pred


def proba_to_target(pred_proba: list, threshold=0.5, als_pred=None) -> list:
    '''
    [description]
    Classifier에서 예측한 확률값을 특정 임계값을 기준으로 타겟을 구하는 함수 (ALS 모델의 결과도 혼합 가능)

    [arguments]
    pred_proba : Classifier에서 예측한 확률값
    threshold : 임계값
    als_pred : ALS 모델의 확률값
    '''

    if not als_pred:
        als_pred = [0] * len(pred_proba)
        
    new_pred = []
    for result, als_result in zip(pred_proba, als_pred):
        false_proba, true_proba = result
        if (true_proba + als_result) >= threshold:
            new_pred.append(True)
        else:
            new_pred.append(False)
        
    return new_pred


def get_clf_eval(y_test: list, y_pred: list) -> [float, float]:
    '''
    [description]
    오차행렬, 정확도, precision, recall, f1_score을 구하는 함수

    [arguments]
    y_test : 실제 y값
    y_pred : 모델을 통해 예측한 값
    '''
    confusion = confusion_matrix(y_test, y_pred, labels=[True, False])
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, labels=[True, False])
    recall = recall_score(y_test, y_pred)
    F1 = f1_score(y_test, y_pred, labels=[True, False])

    # print("오차행렬:\n", confusion)
    # print("\n정확도: {:.4f}".format(accuracy))
    # print("정밀도: {:.4f}".format(precision))
    # print("재현율: {:.4f}".format(recall))
    # print("F1: {:.4f}".format(F1))

    return F1, recall


def ensemble(dataset1: pd.DataFrame, dataset2: pd.DataFrame) -> pd.DataFrame:
    dataset1.sort_values(by='idx', inplace=True)
    dataset2.sort_values(by='idx', inplace=True)

    pred1, pred2 = list(dataset1['is_converted']), deque(dataset2['is_converted'])
    id1, id2 = list(dataset1['idx']), deque(dataset2['idx'])

    print(f'Dataset1 True Count : {sum(pred1)}, Dataset2 True count : {sum(pred2)}')
    for idx, z in enumerate(zip(id1, pred1)):
        id, target = z
        if (id == id2[0]):
            pred1[idx] = any([pred1[idx], pred2[0]])
            pred2.popleft()
            id2.popleft()
        if not id2:
            break
    print(f'Total True Count After Ensemble : {sum(pred1)}')

    dataset1['is_converted'] = pred1

    return dataset1
