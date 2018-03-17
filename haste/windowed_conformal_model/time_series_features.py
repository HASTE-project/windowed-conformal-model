# tsfeatures: computes features from time-series data
# ---------------------------------------------------

# the features I compute below are the same as those I used in my R demo
# later I will explore other potential features to extract
# such as those possible with the python package tsfresh (as used by Fredrik in his work)

import numpy as np


# TODO: reorder params, timestamps first
def time_series_features(feature_time_series, timestamps, end_time):
    """
    Computes summary features (mean,SD,etc.) for a time-window of a particular document (image) feature.

    :param feature_time_series: 1d ndarray feature timeseries (e.g. GFP sum at each of time_steps).
    :param timestamps: 1d ndarray e.g. 0:7, 0:15, but can deal with missing data.
    :param end_time: either 8, 16, 24, ..., 88.
    :return: 4 time-series features (mean; standard deviation; mean(trend); mean(trend change))
    """

    feat = np.zeros(4)

    feat[0] = np.mean(feature_time_series)  # mean of raw data
    feat[1] = np.std(feature_time_series)  # standard deviation of raw data

    z = np.polyfit(timestamps, feature_time_series, min(8, round(len(timestamps)/3)))
    zfit = np.poly1d(z)
    y_pred = zfit(np.arange(end_time))

    D1 = np.zeros(end_time)
    D2 = np.zeros(end_time)

    for i in range(1, end_time - 1):
        D1[i] = 0.5 * (y_pred[i + 1] - y_pred[i - 1])  # 1st derivative from smooth
        D2[i] = y_pred[i + 1] - 2 * y_pred[i] + y_pred[i - 1]  # 2nd derivative

    feat[2] = np.mean(D1[1:(end_time - 1)])
    feat[3] = np.mean(D2[1:(end_time - 1)])

    return feat

