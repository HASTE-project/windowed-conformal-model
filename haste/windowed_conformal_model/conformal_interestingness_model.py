import pymongo

# This is the entry point for the containers

# This one is a wrapper for Phils 'core' model, and handles mongodb, windowing, related biz logic for interestingness.

# Derive from:
# https://github.com/HASTE-project/HasteStorageClient/blob/master/haste_storage_client/interestingness_model.py


# TODO: no state here! except a mongo client!


# TODO: these can go in the ctor - pull the "demo-ness" into the top level repo where we can see it
EPSILON = 0.2
WINDOW_SIZE = 8

# This model 'wraps' the other one, handles buisness logic for windowing, fetching of features from MongoDB, etc.

# It also adapts the conformal result from Phils model into a binary interestingness decision to match the rest of the
# API.

# It is this API which we use from the rest of the system- it allows us to keep the 'core maths' clean from anything
# messy with MongoDB for example. We put all that "mess" in here.


# Some of the wells are processed offline for training, these wells we process online:
WELLS_FOR_ONLINE_ANALYSIS = ['B05', 'C02', 'C03', 'C04', 'C09', 'D04', 'D06', 'E10', 'F09', 'G02', 'G10', 'G11']
GREEN_COLOR_CHANNEL = 2


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

        # For the demo - skip wells which we trained on.
        if substream_id not in WELLS_FOR_ONLINE_ANALYSIS:
            print('interestingness=0 for training well %s' % metadata['well'], flush=True)
            return {'interestingness': 0}

        if metadata['color_channel'] != GREEN_COLOR_CHANNEL:
            # TODO: could perhaps use instead same interestingness as most recent green (+field 1) image for substream
            print('interestingness=0 for non-green image: %s' % metadata['original_filename'], flush=True)
            return {'interestingness': 0}

        if metadata['imaging_point_number'] != 1:
            # TODO: could perhaps use instead same interestingness as most recent green (+field 1) image for substream
            print('interestingness=0 for image from second field: %s' % metadata['original_filename'], flush=True)
            return {'interestingness': 0}

        # TODO: check to see if we at end of window

        if timestamp % WINDOW_SIZE == 0:
            # At the end of the window.

            # TODO: if so, query mongoDB for all historic features for this substream
            # mongo_collection.find({ 'substream_id': substream_id, 'order_by': 'timestamp'}).fetch()

            # TODO: query the core model (pass in whatever it needs, also window size)

            # TODO: interpret the conformal prediction - make a binary decision 1 or 0 on interestingness.
            # based on epsilon

            # TODO: return that value
            return {'interestingness': 1}

        else:
            # Not at the end of the window.
            # TODO: if not, return the interestingness of the last image in this substream (query mongoDB)
            lastest_image_for_substream = list(mongo_collection.find(filter={'substream_id': substream_id,
                                                                             'metadata.imaging_point_number': 1,
                                                                             'metadata.color_channel': GREEN_COLOR_CHANNEL},
                                                                     sort=[('timestamp', pymongo.DESCENDING)],
                                                                     projection=['interestingness'],
                                                                     limit=1))

            if len(lastest_image_for_substream) == 0:
                print('returning interestingness=1: not at end of window, and nothing processed yet', flush=True)
                return {'interestingness': 1}
            else:
                interestingness = lastest_image_for_substream[0]['interestingness']
                print('returning interestingness=%d: not at end of window, falling back to latest result'
                      % interestingness, flush=True)
                return {'interestingness': interestingness}


if __name__ == '__main__':
    STREAM_ID = 'strm_2018_03_05__14_35_26_from_al'
    mongo_client = pymongo.MongoClient('mongodb://metadata-db-prod')
    mongo_db = mongo_client.streams
    cim = ConformalInterestingnessModel()

    # Modify this to test the above
    # TODO: refactor into some proper test-cases
    result = cim.interestingness(stream_id=STREAM_ID,
                                 timestamp=88,
                                 location=None,
                                 substream_id='G11',
                                 metadata={
                                     "full_path": "/foo/bar/wibble/AssayPlate_NUNC_#165305-1_G11_T0088F002L01A02Z01C01",
                                     "imaging_point_number": 1,
                                     "time_point_number": 88,
                                     "unix_timestamp": 1520267258.6972,
                                     "assay_plate_name": "AssayPlate_NUNC_#165305-1",
                                     "original_filename": "AssayPlate_NUNC_#165305-1_G11_T0088F002L01A02Z01C01.tif",
                                     "color_channel": 2,
                                     "image_length_bytes": 2554170,
                                     "well": "G11",
                                     "z_index_3d": 1,
                                     "time_line_number": 1,
                                     "action_list_number": 2,
                                     "extracted_features": {
                                         "sum_of_intensities": 10000531,
                                         "correlation": 0.065282808685255,
                                         "laplaceVariance": 1.8528573200424e-7
                                     }},
                                 mongo_collection=mongo_db[STREAM_ID])

    print(result)
