from sklearn.ensemble import RandomForestClassifier
import numpy as np

# This is the 'core' model - a simple function computing interestingness of a new image, given external features:

# TODO: no state here! just a function!

# This is the 'core' model - it just does the math for the conformal prediction

# it knows nothing about MongoDB

# The intention being that this class could be re-used for other contexts to do conformal prediction in the future


def interestingness(all_features, features_for_new_image, all_y):
    """
    :param all_features: tuples of time-features for each *window* of images (not the image features themselves)
    :param features_for_new_image: dict of image time-features for new image window (not the image features themselves)
    :param all_y: 'training' data
    :return: a list of p-values for each class [not interesting, interesting]
    """

    # TODO: import the 'training' data from another file.

    # Phil's transductive conformal prediction (TCP) model.

    # TODO: create the ND-array here - see https://docs.scipy.org/doc/numpy/reference/arrays.ndarray.html
    X = all_features  # ndarray: rows = "training" objects; cols = features
    xnew = features_for_new_image  # feature for new object (ndarray)
    y = all_y  # object labels/classes for "training" objects

    nlabs = len(np.unique(y))  # number of classes
    p_values = np.zeros(nlabs)  # for storing p-values

    # Mondrian TCP
    for i in range(0, nlabs):
        model = RandomForestClassifier(n_estimators=100)
        X_fit = np.append(X, [xnew], axis=0)
        y_fit = np.append(y, i)
        model.fit(X_fit, y_fit)
        samp = np.where(y_fit == i)[0]
        # non-conformity scores for objects with label i
        alpha = 1 - model.predict_proba(X_fit[samp, :])[:, i]
        # score for "test" object assuming label = i
        alpha_new = alpha[-1]
        # p-value for label i
        p_values[i] = len(np.where(alpha > alpha_new)[0])
        # more careful treatment of cases where alpha == alpha_new
        p_values[i] += np.random.uniform() * len(np.where(alpha == alpha_new)[0])
        p_values[i] /= len(alpha)

    return p_values


if __name__ == '__main__':
    # TODO: add example here
    pass
