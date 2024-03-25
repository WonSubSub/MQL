import time
import argparse
import pandas as pd
from utils import seed_everything
from trainer import train_stratifiedkfold, train_full_dataset


def main(args):
    seed_everything(args.seed)

    train_set, test_set = pd.read_csv(args.data_path + args.train_set), pd.read_csv(args.data_path + args.test_set)
    
    f1_scores, recall_scores = train_stratifiedkfold(args, train_set=train_set)

    model = train_full_dataset(args, train_set=train_set, test_set=test_set)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='parser')
    arg = parser.add_argument


    ############### BASIC OPTION
    arg('--train_set', type=str, default='new_train.csv')
    arg('--test_set', type=str, default='new_test.csv')

    arg('--data_path', type=str, default='data/')
    # arg('--saved_model_path', type=str, default='./saved_models')
    arg('--seed', type=int, default=42)
    arg('--is_inference', type=bool, default=True)

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
    arg('--threshold', type=float, default=0.2)
    arg('--cnt', type=int, default=5)

    args = parser.parse_args()
    main(args)
