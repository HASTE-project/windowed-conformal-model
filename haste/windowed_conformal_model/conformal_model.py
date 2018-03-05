# This is the 'core' model - a simple function computing interestingness of a new image, given external features:

# TODO: no state here! just a function!

# This is the 'core' model - it just does the math for the conformal prediction

# it knows nothing about MongoDB

# The intention being that this class could be re-used for other contexts to do conformal prediction in the future


def interestingness(all_features, features_for_new_image, all_y):
    """
    :param all_features: array of dicts of features for all images seen so far (this comes from MongoDB) 
    :param features_for_new_image: dict of features for new image
    :return: representation of conformal prediction
    """
    
    # TODO: import the 'training' data from another file.

    # Phil's transductive conformal prediction (TCP) model.
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np
    
    X = all_features # ndarray: rows = "training" objects; cols = features
    xnew = features_for_new_image # feature for new object (ndarray)
    y = all_y # object labels/classes for "training" objects
 
    nlabs = len(np.unique(y)) # number of classes
    pval = np.zeros(nlabs) # for storing p-values
    
    # Mondrian TCP
    for i in range(0, nlabs):
        model = RandomForestClassifier(n_estimators=100)
        X_fit = np.append(X, [xnew], axis=0) 
        y_fit = np.append(y, i)
        model.fit(X_fit, y_fit)
        samp = np.where(y_fit==i)[0]
        # non-conformity scores for objects with label i
        alpha = 1 - model.predict_proba(X_fit[samp, :])[:, i] 
        # score for "test" object assuming label = i
        alpha_new = alpha[-1]
        # p-value for label i
        pval[i] = len(np.where(alpha > alpha_new)[0])
        # more careful treatment of cases where alpha == alpha_new
        pval[i] += np.random.uniform() * len(np.where(alpha == alpha_new)[0])
        pval[i] /= len(alpha)

    return(pval)
