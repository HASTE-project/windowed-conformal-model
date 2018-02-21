# This is the entry point for the containers

# This one is a wrapper for Phils 'core' model, and handles mongodb, windowing, related biz logic for interestingness.

# Derive from:
# https://github.com/HASTE-project/HasteStorageClient/blob/master/haste_storage_client/interestingness_model.py


# TODO: no state here! except a mongo client!


# TODO: these can go in the ctor - pull the "demo-ness" into the top level repo where we can see it
ALPHA = 0.8
WINDOW_SIZE = 8


class ConformalInterestingnessModel:

    def __init(self):
        # TODO: create mongo client? (or pass is collection passed in?)
        pass

    def interestingness(self,
                        metadata):
        """
        :param metadata: dictionary containing extracted metadata (eg. image features) for a single image
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
