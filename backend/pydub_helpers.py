from pydub import AudioSegment
from io import BytesIO

def read_arbitrary(data, format):
    return AudioSegment.from_file(
            BytesIO(data),
            format = format
    )

def read_opus(data):
    return AudioSegment.from_file(
            BytesIO(data),
            codec = 'opus'
    )

def read_mp3(data):
    return AudioSegment.from_file(
            BytesIO(data),
            format = 'mp3'
    )

def as_mp3(audio_segment):
    buf = BytesIO()
    audio_segment.export(buf, format='mp3')
    return buf.getvalue()
