import time
import argparse
import pandas as pd


def main(args):
    return

if __name__ == "__main__":


    ######################## BASIC ENVIRONMENT SETUP
    parser = argparse.ArgumentParser(description='parser')
    arg = parser.add_argument


    ############### BASIC OPTION
    arg('--data_path', type=str, default='data/', help='Data path를 설정할 수 있습니다.')
    arg('--saved_model_path', type=str, default='./saved_models', help='Saved Model path를 설정할 수 있습니다.')
    arg('--model', type=str, choices=['FM', 'FFM', 'NCF', 'WDN', 'DCN', 'CNN_FM', 'DeepCoNN'],
                                help='학습 및 예측할 모델을 선택할 수 있습니다.')
    arg('--test_size', type=float, default=0.2, help='Train/Valid split 비율을 조정할 수 있습니다.')
    arg('--seed', type=int, default=42, help='seed 값을 조정할 수 있습니다.')
    arg('--use_best_model', type=bool, default=True, help='검증 성능이 가장 좋은 모델 사용여부를 설정할 수 있습니다.')

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
    arg('--threshold', type=float, default=0.3)
    arg('--cnt', type=int, default=5)
    arg('--is_inference', type=bool, default=False)
    arg('--train_set', type=str, default=False)
    arg('--test_set', type=str, default=False)

    args = parser.parse_args()
    main(args)
