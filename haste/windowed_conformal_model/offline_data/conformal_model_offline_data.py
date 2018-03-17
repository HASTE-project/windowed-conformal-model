import numpy as np
import pkg_resources


def _load_offline_resource(resource_path):
    # Load the file correctly if we've been imported (and even if we are an egg!)
    file_path = pkg_resources.resource_filename(__name__, resource_path)
    print(file_path)
    return np.load(file_path)


TRAIN_FEATURES_STANDARDIZED = _load_offline_resource('train_features_standardized.npy')
STANDARDIZING_VALUES = _load_offline_resource('standardizing_values.npy')

TRAIN_Y = _load_offline_resource('train_y.npy')
TEST_Y = _load_offline_resource('test_y.npy')
