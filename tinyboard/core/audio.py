from __future__ import absolute_import, division, print_function

import io
import struct
import wave

from tinyboard.proto.summary_pb2 import Summary


def audio(tag, tensor, sample_rate=44100):
    tensor_list = [int(32767.0 * x) for x in tensor]
    fio = io.BytesIO()
    Wave_write = wave.open(fio, 'wb')
    Wave_write.setnchannels(1)
    Wave_write.setsampwidth(2)
    Wave_write.setframerate(sample_rate)
    tensor_enc = b''
    for v in tensor_list:
        tensor_enc += struct.pack('<h', v)

    Wave_write.writeframes(tensor_enc)
    Wave_write.close()
    audio_string = fio.getvalue()
    fio.close()
    audio = Summary.Audio(sample_rate=sample_rate, num_channels=1, length_frames=len(
        tensor_list), encoded_audio_string=audio_string, content_type='audio/wav')

    return Summary(value=[Summary.Value(tag=tag, audio=audio)])
