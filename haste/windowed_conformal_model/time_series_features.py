# tsfeatures: computes features from time-series data
# ---------------------------------------------------

# pygam was the closest thing I could find in python to R's mgcv (a great package for GAMs)
#       pip install pygam
# pygam says to do the following installation to install scikit-sparse and nose
# I have nose but installed scikit-sparse on my mac with:
#       conda install -c conda-forge scikit-sparse
# the features I compute below are the same as those I used in my R demo
# later I will explore other potential features to extract
# such as those possible with the python package tsfresh (as used by Fredrik in his work)

import numpy as np
import pandas as pd
from pygam import LinearGAM


def time_series_features(feature_time_series, timestamps, end_time):
    """
    Computes summary features (mean,SD,etc.) for a time-window of a particular document (image) feature.

    :param feature_time_series: 1d ndarray feature timeseries (e.g. GFP sum at each of time_steps).
    :param timestamps: 1d ndarray e.g. 0:7, 0:15, but can deal with missing data.
    :param end_time: either 8, 16, 24, ..., 88.
    :return: 4 time-series features (mean; standard deviation; mean(trend); mean(trend change))
    """

    if len(feature_time_series) != len(timestamps):
        raise Exception('feature_time_series and timestamps must have equal length')

    feat = np.zeros(4)

    X = pd.DataFrame(timestamps)
    Y = pd.Series(feature_time_series)

    gam = LinearGAM(n_splines=min(25, len(Y))).gridsearch(X, Y)

    feat[0] = np.mean(Y)  # mean of raw data
    feat[1] = np.std(Y)  # standard deviation of raw data

    endt = end_time  # TODO: unneeded?
    y_pred = gam.predict(pd.DataFrame(np.arange(endt)))

    D1 = np.zeros(endt)
    D2 = np.zeros(endt)

    for i in range(1, endt - 1):
        D1[i] = 0.5 * (y_pred[i + 1] - y_pred[i - 1])  # 1st derivative from smooth
        D2[i] = y_pred[i + 1] - 2 * y_pred[i] + y_pred[i - 1]  # 2nd derivative

    feat[2] = np.mean(D1[1:(endt - 1)])
    feat[3] = np.mean(D2[1:(endt - 1)])

    return feat


if __name__ == '__main__':
    # strangely when running this "poor man's unit test" from the terminal I get an ImportWarning
    # but not when I run it in a jupyter notebook!?
    # in both cases things appear to work though...
    features = np.sort(np.random.random(8))
    timestamps = np.arange(8)
    end_time = 8
    ts_features = time_series_features(feature_time_series=features, timestamps=timestamps, end_time=end_time)
    # if just using GFP will run the above function twice appending the results as we go
    # so run for GFP sum and get 4 features
    # then run with GFP correlation and append four more features to the 1d ndarray
    # if we use the LNP data then similarly just append four new features 
    # for each granulometry disc size we decide to use
    # in my R demo I used disk sizes 2:4
    # so for the "full" model I had 32 features to fit the models to
    print(ts_features)

# Phil's TODO list (with help as needed from Ben & Håkan)
# ------------------------------------------------------

# necessary for streaming demo to work
# ------------------------------------
# create 1d ndarray with response variables for "training" data (sum(GFP correlation) through time >= 20)
# exclude B10 from all analyses (i.e. not part of "training" or "test" data) [had a fibre across image field]
# use tsfeatures above on "training" data to make a 3d ndarray (train_data)
# dimensions = number of training wells X number of features X number of time windows
# number of features = 8 if just using GFP sum and GFP correlation
# number of time windows = 11 [= 8/88]: first = 0:7, second = 0:15, etc
# standardise train_data and store the mean and sd of the standardisations for use on the "test" data
# standardisation happens after using "tsfeatures" function but before running "interestingness" TCP function

# for my own explorations and additional bits and pieces for AZ demo
# ------------------------------------------------------------------
# test on my mac (non-streaming)
# are results comparable to those gotten with R?
# plot results also with python (as from end of R demo)
# tables of results from python run (again as from end of my R demo)
