
from sklearn.model_selection import StratifiedKFold
from lightgbm import LGBMClassifier
from imblearn.over_sampling import SMOTE # preprocess에 넣을까?
from utils import als_proba, proba_to_target, get_clf_eval
from preprocess import preprocess_dataset
import pandas as pd
from collections import defaultdict


def train_stratifiedkfold(args, train_set):
    X, Y = train_set.drop(columns=['is_converted']), train_set['is_converted']

    f1_scores = defaultdict(list)
    recall_scores = defaultdict(list)
    skf = StratifiedKFold(n_splits=args.n_splits, random_state=args.seed, shuffle=args.shuffle)
    print(f"--------------------------------------Training StratifiedKFold--------------------------------------")
    for i, (train_index, test_index) in enumerate(skf.split(X, Y)):
        print(f"Fold {i+1}: Training..")

        x_train, x_val = X.iloc[train_index], X.iloc[test_index]
        y_train, y_val = Y.iloc[train_index], Y.iloc[test_index]

        x_train, x_val = preprocess_dataset(args, x_train, x_val)
        # print(x_train, x_val)

        model = LGBMClassifier(n_estimators=args.n_estimators, 
                               max_depth=args.max_depth, 
                               num_leaves=args.num_leaves, 
                               n_jobs=args.n_jobs,
                               learning_rate=args.learning_rate, 
                               boost_from_average=args.boost_from_average)
        
        model.fit(x_train, y_train)
        for threshold in args.thresholds:
            f1, recall, _ = valid(threshold, model, x_val, y_val)
            f1_scores[threshold].append(f1)
            recall_scores[threshold].append(recall)

        print(f"Fold {i+1}: Done!")
        print('---------------------------------------------------------------------------------------------------')

    best_f1_recall, best_threshold = 0, 0
    print('Threshold별 (F1_score, Recall) 평균')
    for key in f1_scores.keys():
        f1_mean = sum(f1_scores[key]) / (i+1)
        recall_mean = sum(recall_scores[key]) / (i+1)
        print(f'{key} : ({f1_mean:.3f}, {recall_mean:.3f})')

        if (f1_mean*2 + recall_mean)/3 > best_f1_recall:
            best_f1_recall = max(best_f1_recall, (f1_mean*2 + recall_mean)/3)
            best_threshold = key
    
    print(f'------------ Best Threshold = {best_threshold} --------------')

    return f1_scores, recall_scores, best_threshold


def train_full_dataset(args, train_set, test_set, best_threshold):
    X, Y = train_set.drop(columns=['is_converted']), train_set['is_converted']
    X_test, Y_test = test_set.drop(columns=['is_converted']), test_set['is_converted']
    f1_scores = defaultdict(list)
    recall_scores = defaultdict(list)

    print(f"--------------------------------------Training Full Dataset--------------------------------------")
    X, X_test = preprocess_dataset(args, X, X_test)
    

    model = LGBMClassifier(n_estimators=args.n_estimators, 
                           max_depth=args.max_depth, 
                           num_leaves=args.num_leaves, 
                           n_jobs=args.n_jobs,
                           learning_rate=args.learning_rate, 
                           boost_from_average=args.boost_from_average)
    
    model.fit(X, Y)
    print(f"---------------------------------------Training Complete-----------------------------------------")

    if not args.is_inference:
        print(f"---------------------------------------Validation Start-----------------------------------------")
        for threshold in args.thresholds:
            f1, recall, pred = valid(threshold, model, X_test, Y_test, args.is_inference)
            f1_scores[threshold].append(f1)
            recall_scores[threshold].append(recall)

        f1, recall, pred = valid(best_threshold, model, X_test, Y_test, args.is_inference)
        print(f'F1_score : {f1:.3f}, Recall : {recall:.3f}  ==>  Threshold - {best_threshold}')
        print(f"--------------------------------------Validation Complete----------------------------------------")
    else:
        print(f"---------------------------------------Inference Start-----------------------------------------")
        pred = valid(best_threshold, model, X_test, Y_test, args.is_inference)
        print(f"--------------------------------------Inference Complete----------------------------------------")

    return f1_scores, recall_scores, pred


def valid(threshold, model, x_test, y_test, is_inference=False):
    if not is_inference:
        pred_proba = model.predict_proba(x_test)
        pred = proba_to_target(pred_proba, threshold)

        f1, recall = get_clf_eval(y_test, pred)
        return f1, recall, pred
    
    else:
        pred_proba = model.predict_proba(x_test)
        pred = proba_to_target(pred_proba, threshold)

        return pred

