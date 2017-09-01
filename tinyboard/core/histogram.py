from __future__ import absolute_import, division, print_function

import numpy as np

from tinyboard.core.compat import clean_tag
from tinyboard.proto.summary_pb2 import HistogramProto
from tinyboard.proto.summary_pb2 import Summary


def histogram(name, tensor, bins, collections=None):
    """Prepare a summary proto containing a histogram.

    :param string name: The name of the histogram.
    :param Tensor tensor: The tensor of the histogram. Can be of any shape.
    :param list<string> collections: Optional collections keys. The new summary
        will be added to these collections.
    :returns Summary: The summary proto containing the histogram.
    """
    name = clean_tag(name)
    hist = make_histogram(tensor.astype(float), bins)
    return Summary(value=[Summary.Value(tag=name, histo=hist)])


def make_histogram(values, bins):
    """Convert values into a histogram proto using logic from histogram.cc."""
    values = values.reshape(-1)
    counts, limits = np.histogram(values, bins=bins)
    return HistogramProto(
        min=values.min(), max=values.max(),
        num=len(values),
        sum=values.sum(), sum_squares=values.dot(values),
        bucket_limit=limits[1:], bucket=counts,
    )
