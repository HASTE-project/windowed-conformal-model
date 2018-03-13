from sklearn.ensemble import RandomForestClassifier
import numpy as np

# This is the 'core' model - a simple function computing interestingness of a new image, given external features:

# TODO: no state here! just a function!

# This is the 'core' model - it just does the math for the conformal prediction

# it knows nothing about MongoDB

# The intention being that this class could be re-used for other contexts to do conformal prediction in the future


def interestingness(all_features, features_for_new_image, all_y):
    """
    :param all_features: ndarray: rows = "training" objects; cols = time series features; 3rd: time window index
    :param features_for_new_image: dict of time-series features for new image for all previous images (not image features)
    :param all_y: 'training' data - ground truth interestingness per well
    :return: a list of p-values for each class [uninteresting, interesting]
    """

    # TODO: import the 'training' data from another file.

    # Phil's transductive conformal prediction (TCP) model.

    # TODO: create the ND-array here - see https://docs.scipy.org/doc/numpy/reference/arrays.ndarray.html
    n_labels = len(np.unique(all_y))  # number of classes
    p_values = np.zeros(n_labels)  # for storing p-values

    # Mondrian TCP
    for label in range(0, n_labels):
        model = RandomForestClassifier(n_estimators=100)
        X_fit = np.append(all_features, [features_for_new_image], axis=0)
        y_fit = np.append(all_y, label)
        model.fit(X_fit, y_fit)
        samp = np.where(y_fit == label)[0]
        # non-conformity scores for objects with label i
        alpha = 1 - model.predict_proba(X_fit[samp, :])[:, label]
        # score for "test" object assuming label = i
        alpha_new = alpha[-1]
        # p-value for label i
        p_values[label] = len(np.where(alpha > alpha_new)[0])
        # more careful treatment of cases where alpha == alpha_new
        p_values[label] += np.random.uniform() * len(np.where(alpha == alpha_new)[0])
        p_values[label] /= len(alpha)

    return p_values


if __name__ == '__main__':
    # TODO: add example here
    pass
