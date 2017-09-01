from __future__ import absolute_import, division, print_function

import logging
import re as _re
import bisect
from six import StringIO
from six.moves import range
import numpy as np


def text(tag, text):
    import json
    PluginData = [SummaryMetadata.PluginData(plugin_name='text')]
    smd = SummaryMetadata(plugin_data=PluginData)
    tensor = TensorProto(dtype='DT_STRING', string_val=[
                         text.encode(encoding='utf_8')])
    return Summary(value=[Summary.Value(node_name=tag, metadata=smd, tensor=tensor)])
