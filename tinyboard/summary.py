from __future__ import absolute_import, division, print_function

import logging
import re as _re
import bisect
from six import StringIO
from six.moves import range
from PIL import Image
import numpy as np


def image(tag, tensor):
    """Outputs a `Summary` protocol buffer with images.
    The summary has up to `max_images` summary values containing images. The
    images are built from `tensor` which must be 3-D with shape `[height, width,
    channels]` and where `channels` can be:
    *  1: `tensor` is interpreted as Grayscale.
    *  3: `tensor` is interpreted as RGB.
    *  4: `tensor` is interpreted as RGBA.
    The `name` in the outputted Summary.Value protobufs is generated based on the
    name, with a suffix depending on the max_outputs setting:
    *  If `max_outputs` is 1, the summary value tag is '*name*/image'.
    *  If `max_outputs` is greater than 1, the summary value tags are
       generated sequentially as '*name*/image/0', '*name*/image/1', etc.
    Args:
      tag: A name for the generated node. Will also serve as a series name in
        TensorBoard.
      tensor: A 3-D `uint8` or `float32` `Tensor` of shape `[height, width,
        channels]` where `channels` is 1, 3, or 4.
    Returns:
      A scalar `Tensor` of type `string`. The serialized `Summary` protocol
      buffer.
    """
    import torch
    tag = _clean_tag(tag)
    assert isinstance(tensor, np.ndarray) or isinstance(tensor, torch.cuda.FloatTensor) or isinstance(
        tensor, torch.FloatTensor), 'input tensor should be one of numpy.ndarray, torch.cuda.FloatTensor, torch.FloatTensor'
    if not isinstance(tensor, np.ndarray):
        assert tensor.dim() < 4 and tensor.dim() > 1, 'input tensor should be 3 dimensional.'
        if tensor.dim() == 2:
            tensor = tensor.unsqueeze(0)
        tensor = tensor.cpu().permute(1, 2, 0).numpy()
    else:
        tensor = tensor.astype(np.float32)
    tensor = (tensor * 255).astype(np.uint8)
    image = make_image(tensor)
    return Summary(value=[Summary.Value(tag=tag, image=image)])


def make_image(tensor):
    """Convert an numpy representation image to Image protobuf"""
    height, width, channel = tensor.shape
    image = Image.fromarray(tensor)
    import io
    output = io.BytesIO()
    image.save(output, format='PNG')
    image_string = output.getvalue()
    output.close()
    return Summary.Image(height=height,
                         width=width,
                         colorspace=channel,
                         encoded_image_string=image_string)


def text(tag, text):
    import json
    PluginData = [SummaryMetadata.PluginData(plugin_name='text')]
    smd = SummaryMetadata(plugin_data=PluginData)
    tensor = TensorProto(dtype='DT_STRING', string_val=[
                         text.encode(encoding='utf_8')])
    return Summary(value=[Summary.Value(node_name=tag, metadata=smd, tensor=tensor)])
