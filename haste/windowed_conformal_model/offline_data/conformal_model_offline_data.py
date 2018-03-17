import numpy as np

TRAIN_FEATURES_STANDARDIZED = np.load('offline_data/train_features_standardized.npy')
STANDARDIZING_VALUES = np.load('offline_data/standardizing_values.npy')

TRAIN_Y = np.load('offline_data/train_y.npy')
TEST_Y = np.load('offline_data/test_y.npy')
