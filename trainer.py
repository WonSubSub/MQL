
from sklearn.model_selection import StratifiedKFold
from lightgbm import LGBMClassifier
from imblearn.over_sampling import SMOTE # preprocess에 넣을까?
from utils import als_proba, proba_to_target, get_clf_eval
from preprocess import preprocess_dataset
import pandas as pd


def train_stratifiedkfold(args, train_set):
    X, Y = train_set.drop(columns=['is_converted']), train_set['is_converted']

    f1_scores = []
    recall_scores = []
    skf = StratifiedKFold(n_splits=args.n_splits, random_state=args.seed, shuffle=args.shuffle)
    print(f"--------------------------------------Training StratifiedKFold--------------------------------------")
    for i, (train_index, test_index) in enumerate(skf.split(X, Y)):
        print(f"Fold {i+1}: Training..")

        x_train, x_val = X.iloc[train_index], X.iloc[test_index]
        y_train, y_val = Y.iloc[train_index], Y.iloc[test_index]

        x_train, x_val = preprocess_dataset(args, x_train, x_val)
        print(x_train, x_val)

        model = LGBMClassifier(n_estimators=args.n_estimators, 
                               max_depth=args.max_depth, 
                               num_leaves=args.num_leaves, 
                               n_jobs=args.n_jobs,
                               learning_rate=args.learning_rate, 
                               boost_from_average=args.boost_from_average)
        
        model.fit(x_train, y_train)
        f1, recall = valid(args.threshold, model, x_val, y_val)

        recall_scores.append(recall)
        f1_scores.append(f1)

        print(f"Fold {i+1}: Done!")
        print('---------------------------------------------------------------------------------------------------')

    print(f'F1_score 평균 : {sum(f1_scores) / (i+1)}')
    print(f'Recall 평균 : {sum(recall_scores) / (i+1)}')
    print(f'F1, Recall 평균 : {((sum(f1_scores) / (i+1)) + (sum(recall_scores) / (i+1)))/2}')
    return f1_scores, recall_scores


def train_full_dataset(args, train_set, test_set):
    X, Y = train_set.drop(columns=['is_converted']), train_set['is_converted']
    X_test, Y_test = test_set.drop(columns=['is_converted']), test_set['is_converted']

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

    print(f"---------------------------------------Validation Start-----------------------------------------")

    submission = valid(args.threshold, model, X_test, Y_test, args.is_inference)
    submission.to_csv('./result/{args.test_set}_result.csv', index=None)

    print(f"--------------------------------------Validation Complete----------------------------------------")
    print(f"Result File Made : {args.test_set}_result.csv")

    return model


def valid(threshold, model, x_test, y_test, is_inference=False):
    if not is_inference:
        pred_proba = model.predict_proba(x_test)
        pred = proba_to_target(pred_proba, threshold)

        f1, recall = get_clf_eval(y_test, pred)
        return f1, recall
    
    else:
        pred_proba = model.predict_proba(x_test)
        pred = proba_to_target(pred_proba, threshold)

        x_test['is_converted'] = pred
        return x_test

