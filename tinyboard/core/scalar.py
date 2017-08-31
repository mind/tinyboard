from __future__ import absolute_import, division, print_function

from tinyboard.core.compat import clean_tag
from tinyboard.proto.summary_pb2 import Summary


def scalar(name, scalar, collections=None):
    """Outputs a `Summary` protocol buffer containing a single scalar value.
    The generated Summary has a Tensor.proto containing the input Tensor.
    Args:
      name: A name for the generated node. Will also serve as the series name in
        TensorBoard.
      tensor: A real numeric Tensor containing a single value.
      collections: Optional list of graph collections keys. The new summary op is
        added to these collections. Defaults to `[GraphKeys.SUMMARIES]`.
    Returns:
      A scalar `Tensor` of type `string`. Which contains a `Summary` protobuf.
    Raises:
      ValueError: If tensor has the wrong shape or type.
    """
    return Summary(value=[
        Summary.Value(tag=clean_tag(name), simple_value=float(scalar)),
    ])
