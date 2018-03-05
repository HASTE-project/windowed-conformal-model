# This is the entry point for the containers

# This one is a wrapper for Phils 'core' model, and handles mongodb, windowing, related biz logic for interestingness.

# Derive from:
# https://github.com/HASTE-project/HasteStorageClient/blob/master/haste_storage_client/interestingness_model.py


# TODO: no state here! except a mongo client!


# TODO: these can go in the ctor - pull the "demo-ness" into the top level repo where we can see it
ALPHA = 0.8
WINDOW_SIZE = 8

# This model 'wraps' the other one, handles buisness logic for windowing, fetching of features from MongoDB, etc.

# It also adapts the conformal result from Phils model into a binary interestingness decision to match the rest of the
# API.

# It is this API which we use from the rest of the system- it allows us to keep the 'core maths' clean from anything
# messy with MongoDB for example. We put all that "mess" in here.


class ConformalInterestingnessModel:

    def __init(self):
        # TODO: create mongo client? (or pass is collection passed in?)
        pass

    def interestingness(self,
                        stream_id=None,
                        timestamp=None,
                        location=None,
                        substream_id=None,
                        metadata=None,
                        mongo_collection=None):
        """
        :param stream_id (str): ID for the stream session - used to group all the data for that streaming session.
        :param timestamp (numeric): should come from the cloud edge (eg. microscope). integer or floating point.
            *Uniquely identifies the document within the streaming session*.
        :param location (tuple): spatial information (eg. (x,y)).
        :param substream_id (string): ID for grouping of documents in stream (eg. microscopy well ID), or 'None'.
        :param metadata (dict): extracted metadata (eg. image features).
        :param mongo_collection: collection in mongoDB allowing custom queries (this is a hack - best avoided!)
        """

        # TODO: check to see if we at end of window

        # TODO: if not, return the interestingness of the last image in this substream (query mongoDB)
        # TODO: Return it.

        # TODO: if so, query mongoDB for all historic features for this substream

        # TODO: query the core model (pass in whatever it needs, also window size)

        # TODO: interpret the conformal prediction - make a binary decision 1 or 0 on interestingness.

        # TODO: return that value

        # Log like this
        print('windowed_conformal_model: log something here', flush=True)  # Flush for Docker.

        return {'interestingness': 1}
