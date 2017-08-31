from __future__ import absolute_import, division, print_function

import numpy as np

from tinyboard.core.compat import clean_tag
from tinyboard.proto.summary_pb2 import HistogramProto
from tinyboard.proto.summary_pb2 import Summary


def histogram(name, values, bins, collections=None):
    # pylint: disable=line-too-long
    """Outputs a `Summary` protocol buffer with a histogram.
    The generated
    [`Summary`](https://www.tensorflow.org/code/tensorflow/core/framework/summary.proto)
    has one summary value containing a histogram for `values`.
    This op reports an `InvalidArgument` error if any value is not finite.
    Args:
      name: A name for the generated node. Will also serve as a series name in
        TensorBoard.
      values: A real numeric `Tensor`. Any shape. Values to use to
        build the histogram.
      collections: Optional list of graph collections keys. The new summary op is
        added to these collections. Defaults to `[GraphKeys.SUMMARIES]`.
    Returns:
      A scalar `Tensor` of type `string`. The serialized `Summary` protocol
      buffer.
    """
    name = clean_tag(name)
    hist = make_histogram(values.astype(float), bins)
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
