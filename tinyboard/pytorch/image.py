from io import BytesIO

import numpy as np
import torch
from PIL import Image

from tinyboard.core.compat import clean_tag
from tinyboard.proto.summary_pb2 import Summary


def image(name, tensor):
    """Prepare a summary proto containing an image.

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
    name = clean_tag(name)
    if isinstance(tensor, np.ndarray):
        tensor = tensor.astype(np.float32)
    else:
        if not isinstance(tensor, (torch.FloatTensor, torch.cuda.FloatTensor)):
            raise ValueError('Image summary received invalid tensor value')
        dim = tensor.dim()
        if dim == 2:
            tensor = tensor.unsqueeze(0)
        elif dim != 3:
            raise ValueError('Image summary must have 3D tensor')
        tensor = tensor.cpu().permute(1, 2, 0).numpy()
    tensor = (tensor * 255).astype(np.uint8)
    return Summary(value=[Summary.Value(tag=name, image=_make_image(tensor))])


def _make_image(value):
    """Convert a numpy image into a image proto."""
    height, width, channel = value.shape
    image = Image.fromarray(value)
    output = BytesIO()
    image.save(output, format='PNG')
    image_string = output.getvalue()
    output.close()
    return Summary.Image(width=width, height=height,
                         colorspace=channel,
                         encoded_image_string=image_string)
