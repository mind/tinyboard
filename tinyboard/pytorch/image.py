from io import BytesIO

import numpy as np
import torch
from PIL import Image

from tinyboard.core.compat import clean_tag
from tinyboard.proto.summary_pb2 import Summary


def image(name, tensor):
    """Prepare a summary proto containing an image.

    :param string name: The name of the image summary.
    :param Tensor tensor: The image tensor. It should contain height, width,
        and channel, which can be grayscale (1) or rgb(a) (3, 4).
    :returns Summary: The summary proto containing the serialized image.
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
