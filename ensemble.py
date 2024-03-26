import pandas as pd
from utils import ensemble, get_clf_eval
import argparse

def main(args):
    
    dataset1, dataset2, eval_dataset = pd.read_csv(args.dataset1), pd.read_csv(args.dataset2), pd.read_csv(args.eval_dataset)

    ensembled_datset = ensemble(dataset1, dataset2)
    eval_dataset.sort_values(by=['idx'], inplace=True)
    
    f1, recall = get_clf_eval(eval_dataset['is_converted'], ensembled_datset['is_converted'])
    print(f'F1_score, Recall After Ensemble : {f1:.3f}, {recall:.3f}')

    ensembled_datset.to_csv(f'./result/ensemble/ensembled_{args.dataset1.split('.')[-2]}_{args.dataset2.split('.')[-2]}.csv',index=None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parser')
    arg = parser.add_argument

    arg("--dataset1", type=str, default = './result/csv/0.25_val_set.csv')
    arg("--dataset2", type=str, default = './result/csv/0.25_ct_val_set.csv')
    arg("--eval_dataset", type=str, default = './data/val_set.csv')

    args = parser.parse_args()
    main(args)