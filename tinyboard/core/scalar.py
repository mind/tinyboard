from __future__ import absolute_import, division, print_function

from tinyboard.core.compat import clean_tag
from tinyboard.proto.summary_pb2 import Summary


def scalar(name, scalar, collections=None):
    """Prepare a summary proto containing a scalar value.

    :param string name: The name of the scalar series.
    :param Tensor scalar: The scalar value. Should contain a single value.
    :param list<string> collections: Optional collections keys. The new summary
        will be added to these collections.
    :returns Summary: The summary proto containing the scalar value.
    :raises ValueError: If the incoming tensor has the wrong shape/type.
    """
    name = clean_tag(name)
    return Summary(value=[Summary.Value(tag=name, simple_value=float(scalar))])
