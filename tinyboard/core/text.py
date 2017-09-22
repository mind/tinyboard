from __future__ import absolute_import, division, print_function

from tinyboard.proto.summary_pb2 import Summary, SummaryMetadata
from tinyboard.proto.tensor_pb2 import TensorProto


def text(name, text):
    """Prepare a summary proto containing text.

    :param string name: The name of the text.
    :param string text: The text.
    :returns Summary: The summary proto containing the text.
    """
    plugin_data = [SummaryMetadata.PluginData(plugin_name='text')]
    meta = SummaryMetadata(plugin_data=plugin_data)
    tensor = TensorProto(
        dtype='DT_STRING', string_val=[text.encode(encoding='utf_8')],
    )
    return Summary(value=[
        Summary.Value(node_name=name, metadata=meta, tensor=tensor),
    ])
