# This is the 'core' model - a simple function computing interestingness of a new image, given external features:

# TODO: no state here! just a function!

# This is the 'core' model - it just does the math for the conformal prediction

# it knows nothing about MongoDB

# The intention being that this class could be re-used for other contexts to do conformal prediction in the future


def interestingness(all_features, features_for_new_image):
    """
    :param all_features: array of dicts of features for all images seen so far (this comes from MongoDB) 
    :param features_for_new_image: dict of features for new image
    :return: representation of conformal prediction
    """

    # Phils ported R code goes here.

    # TODO: import the 'training' data from another file.

    pass
