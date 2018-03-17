import pymongo
import numpy
from .time_series_features import time_series_features
from haste.windowed_conformal_model.offline_data.conformal_model_offline_data import TRAIN_FEATURES_STANDARDIZED, TRAIN_Y, STANDARDIZING_VALUES
from .conformal_model import interestingness as conformal_interestingness

EPSILON = 0.2
WINDOW_SIZE = 8

# It is this API which we use from the rest of the system- it allows us to keep the 'core maths' clean from anything
# messy with MongoDB for example. We put all that "mess" in here.


# Some of the wells are processed offline for training, these wells we process online:
WELLS_FOR_ONLINE_ANALYSIS = ['B05', 'C02', 'C03', 'C04', 'C09', 'D04', 'D06', 'E10', 'F09', 'G02', 'G10', 'G11']
GREEN_COLOR_CHANNEL = 2


def _standardize(features, standardizing_values):
    return (features - standardizing_values[0]) / standardizing_values[1]


def _all_course_features_for_substream(mongo_collection, substream_id):
    # TODO: exclude image features from the future (nice to know for now - is stuff being processed in the right order?)
    # Search for documents with specific substream_id having image_point_number = 1 and color_channel = 2 (Green)
    cursor = mongo_collection.find(filter={'substream_id': substream_id,
                                           'metadata.imaging_point_number': 1,
                                           'metadata.color_channel': GREEN_COLOR_CHANNEL},
                                   sort=[('timestamp', pymongo.ASCENDING)],
                                   projection=['timestamp', 'metadata.extracted_features'])

    correlations = []
    sums_of_intensities = []
    x_times = []

    for document in cursor:
        correlations.append(document['metadata']['extracted_features']['correlation'])
        sums_of_intensities.append(document['metadata']['extracted_features']['sum_of_intensities'])
        x_times.append(document['timestamp'])

    return correlations, sums_of_intensities, x_times


def _convert_p_values(p_interesting, p_uninteresting):
    # Interpret the conformal p-values, converting to the HASTE notion of interestingness.
    is_interesting = p_interesting > EPSILON
    is_uninteresting = p_uninteresting > EPSILON
    if is_interesting and not is_uninteresting:
        return {'interestingness': 1}
    elif not is_interesting and is_uninteresting:
        return {'interestingness': 0}
    elif is_interesting and is_uninteresting:
        # classified as both
        return {'interestingness': 0.5}
    else:
        # classified as neither
        return {'interestingness': 0.9}


class ConformalInterestingnessModel:
    """
    This model 'wraps' conformal_model, handles business logic for windowing, fetching of features from MongoDB, etc.
    It also adapts the conformal result from Phil's model into a HASTE-friendly interestingness measure.

    Derives from:
    https://github.com/HASTE-project/HasteStorageClient/blob/master/haste_storage_client/interestingness_model.py
    """

    def interestingness(self,
                        stream_id=None,
                        timestamp=None,
                        location=None,
                        substream_id=None,
                        metadata=None,
                        mongo_collection=None):
        """
        :param stream_id (str): ID for the stream session - used to group all the data for that streaming session.
        :param timestamp (must be integer for this model): should come from the cloud edge (eg. microscope). integer or floating point.
            *Uniquely identifies the document within the streaming session*.
        :param location (tuple): spatial information (eg. (x,y)).
        :param substream_id (string): ID for grouping of documents in stream (eg. microscopy well ID), or 'None'.
        :param metadata (dict): extracted metadata (eg. image features).
        :param mongo_collection: collection in mongoDB allowing custom queries (this is a hack - best avoided!)
        """

        if timestamp != int(timestamp):
            raise ValueError('this model only supports integer timestamps')

        # For the demo - skip wells which we trained on.
        if substream_id not in WELLS_FOR_ONLINE_ANALYSIS:
            print('interestingness=0 for training well {}'.format(metadata['well']), flush=True)
            return {'interestingness': 0}

        if metadata['color_channel'] != GREEN_COLOR_CHANNEL:
            # TODO: could perhaps use instead same interestingness as most recent green (+field 1) image for substream
            print('interestingness=0 for non-green image: {}'.format(metadata['original_filename']), flush=True)
            return {'interestingness': 0}

        if metadata['imaging_point_number'] != 1:
            # TODO: could perhaps use instead same interestingness as most recent green (+field 1) image for substream
            print('interestingness=0 for image from second field: {}'.format(metadata['original_filename']), flush=True)
            return {'interestingness': 0}

        if timestamp == 0:
            # AZN data starts at timestamp=1
            print('timestamp 0 is not supported by time_series_features', flush=True)
            return {'interestingness': 1}
        elif timestamp % WINDOW_SIZE == 0:
            # At the end of the window.

            course_features = _all_course_features_for_substream(mongo_collection=mongo_collection,
                                                                 substream_id=substream_id)
            # ([correlation], [sum_of_intensities], [x_time])

            # TODO: move ndarray conversion inside 'time_series_features' function.

            timestamps = course_features[2]
            timestamps_ndarray = numpy.ndarray(shape=(len(timestamps)),
                                               dtype=int,
                                               buffer=numpy.array(timestamps))

            # Correlation
            correlation = course_features[0]
            correlation_ndarray = numpy.ndarray(shape=(len(correlation)),
                                                dtype=float,
                                                buffer=numpy.array(correlation))

            # Compute features on the entire timeseries so far for that well:
            correlation_ts_features = time_series_features(correlation_ndarray,
                                                           timestamps_ndarray,
                                                           timestamp)

            # Sum of intensities
            sum_of_intensities = course_features[1]
            sum_of_intensities_ndarray = numpy.ndarray(shape=(len(sum_of_intensities)),
                                                       dtype=int,
                                                       buffer=numpy.array(sum_of_intensities))

            # Compute features on the entire timeseries so far for that well:
            sum_of_intensities_ts_features = time_series_features(sum_of_intensities_ndarray,
                                                                  timestamps_ndarray,
                                                                  timestamp)

            # .. = (mean,sd,d1,d2)

            ts_features = numpy.append(correlation_ts_features, sum_of_intensities_ts_features, axis=0)

            window_index = int(timestamp / WINDOW_SIZE) - 1
            ts_features_standardized = _standardize(ts_features, STANDARDIZING_VALUES[:, :, window_index])
            p_values = conformal_interestingness(TRAIN_FEATURES_STANDARDIZED[:, :, window_index],
                                                 ts_features_standardized, TRAIN_Y)

            print('p_values for timestamp {} = {}'.format(timestamp, p_values), flush=True)

            p_interesting = p_values[1]
            p_uninteresting = p_values[0]
            return _convert_p_values(p_interesting, p_uninteresting)
        else:
            # Not at the end of the window.
            # TODO: if not, return the interestingness of the last image in this substream (query mongoDB)
            lastest_image_for_substream = list(mongo_collection.find(filter={'substream_id': substream_id,
                                                                             'metadata.imaging_point_number': 1,
                                                                             'metadata.color_channel': GREEN_COLOR_CHANNEL},
                                                                     sort=[('timestamp', pymongo.DESCENDING)],
                                                                     projection=['interestingness',
                                                                                 'timestamp'],
                                                                     limit=1))

            if len(lastest_image_for_substream) == 0:
                print('returning interestingness=1: not at end of window, and nothing processed yet', flush=True)
                return {'interestingness': 1}
            else:
                interestingness = lastest_image_for_substream[0]['interestingness']
                print('returning interestingness= {} : not at end of window, falling back to latest result'
                      .format(interestingness), flush=True)

                latest_image_timestamp = lastest_image_for_substream[0]['timestamp']
                if latest_image_timestamp + 1 != timestamp:
                    print('unexpected most recent image - current timestamp: {} previous image has timestamp {} !'
                          .format(timestamp, latest_image_timestamp), flush=True)
                return {'interestingness': interestingness}


if __name__ == '__main__':
    STREAM_ID = 'strm_2018_03_05__14_35_26_from_al'
    mongo_client = pymongo.MongoClient('mongodb://metadata-db-prod')
    # mongo_client = pymongo.MongoClient('mongodb://localhost')
    mongo_db = mongo_client.streams
    cim = ConformalInterestingnessModel()

    MOCK_METADATA = {"full_path": "/foo/bar/wibble/AssayPlate_NUNC_#165305-1_G11_T0088F002L01A02Z01C01",
                     "imaging_point_number": 1,
                     "time_point_number": 88, "unix_timestamp": 1520267258.6972,
                     "assay_plate_name": "AssayPlate_NUNC_#165305-1",
                     "original_filename": "AssayPlate_NUNC_#165305-1_G11_T0088F002L01A02Z01C01.tif",
                     "color_channel": GREEN_COLOR_CHANNEL, "image_length_bytes": 2554170, "well": "G11",
                     "z_index_3d": 1,
                     "time_line_number": 1, "action_list_number": 2,
                     "extracted_features": {"sum_of_intensities": 10000531, "correlation": 0.065282808685255,
                                            "laplaceVariance": 1.8528573200424e-7}}

    # Modify this to test the above
    # TODO: refactor into some proper test-cases

    for timestamp in range(1, 17):
        print(timestamp)
        result = cim.interestingness(stream_id=STREAM_ID,
                                     timestamp=timestamp,
                                     location=None,
                                     substream_id='G11',
                                     metadata=MOCK_METADATA,
                                     mongo_collection=mongo_db[STREAM_ID])
        print(result)
