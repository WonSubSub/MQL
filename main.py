import time
import argparse
import pandas as pd
from utils import seed_everything
from trainer import train_stratifiedkfold, train_full_dataset
import pickle


def main(args):
    seed_everything(args.seed)

    train_set, test_set = pd.read_csv(args.data_path + args.train_set), pd.read_csv(args.data_path + args.test_set)
    
    f1_scores, recall_scores, best_threshold = train_stratifiedkfold(args, train_set=train_set)

    with open(f'./result/f1_score/{args.train_set.split('.')[0]}_f1_scores.pkl', 'wb') as f:
        pickle.dump(f1_scores, f)
    with open(f'./result/recall/{args.train_set.split('.')[0]}_recall_scores.pkl', 'wb') as f:
        pickle.dump(recall_scores, f)

    val_f1_scores, val_recall_scores, pred = train_full_dataset(args, train_set=train_set, test_set=test_set, best_threshold=best_threshold)

    if not args.is_inference:
        with open(f'./result/f1_score/{args.test_set.split('.')[0]}_f1_scores.pkl', 'wb') as f:
            pickle.dump(val_f1_scores, f)
        with open(f'./result/recall/{args.test_set.split('.')[0]}_recall_scores.pkl', 'wb') as f:
            pickle.dump(val_recall_scores, f)

    test_set['is_converted'] = pred
    test_set.to_csv(f'./result/csv/{best_threshold}_{args.test_set}', index=None)
    print(f"Result File Made : result_{args.test_set}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='parser')
    arg = parser.add_argument


    ############### BASIC OPTION
    arg('--train_set', type=str, default='train_set.csv')
    arg('--test_set', type=str, default='val_set.csv')

    arg('--data_path', type=str, default='data/')
    # arg('--saved_model_path', type=str, default='./saved_models')
    arg('--seed', type=int, default=42)
    arg('--is_inference', type=bool, default=False)

    ############### TRAINING OPTION
    arg('--continuous_columns', type=list, default=['lead_desc_length', 'historical_existing_cnt'])
    arg('--n_splits', type=int, default=5)
    arg('--shuffle', type=bool, default=True)
    arg('--n_estimators', type=int, default=500)
    arg('--learning_rate', type=float, default=0.03)
    arg('--num_leaves', type=int, default=100)
    arg('--n_jobs', type=int, default=-1)
    arg('--max_depth', type=float, default=22)
    arg('--boost_from_average', type=bool, default=False)
    arg('--thresholds', type=float, default=[0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2 ,0.15, 0.1])
    arg('--cnt', type=int, default=2)

    args = parser.parse_args()
    main(args)
