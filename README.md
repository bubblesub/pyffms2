ffms2 – Python bindings for FFmpegSource
========================================

This project is a fork that supports more recent versions of FFMS.
The original repository can be found at https://bitbucket.org/spirit/ffms.

Example usage
-------------

If you don't need to keep the index, create a video source right away:

```python-console
>>> import ffms2
>>> source_file = "test/CINT_Nik_H264_720_512kb.mp4"
>>> vsource = ffms2.VideoSource(source_file)
```

Or you can create an indexer:

```python-console
>>> indexer = ffms2.Indexer(source_file)
>>> indexer.format_name
'mov,mp4,m4a,3gp,3g2,mj2'
>>> indexer.track_info_list
[TrackInfo(type=0, codec_name='h264'), TrackInfo(type=1, codec_name='aac')]
```

Then create the index for the video source:

```python-console
>>> for track in indexer.track_info_list:
>>>     indexer.track_index_settings(track.num, 1, 0)
>>> index = indexer.do_indexing2()
>>> track_number = index.get_first_indexed_track_of_type(ffms2.FFMS_TYPE_VIDEO)
>>> vsource = ffms2.VideoSource(source_file, track_number, index)
```

Extract information from the video source:

```python-console
>>> vsource.properties.NumFrames
1430
>>> vsource.track.keyframes[:5]
[0, 12, 24, 36, 48]
>>> vsource.track.timecodes[:5]
[0.0, 41.666666666666664, 83.33333333333333, 125.0, 166.66666666666666]
```

Retrieve a video frame:

```python-console
>>> frame = vsource.get_frame(0)
>>> frame.EncodedWidth, frame.EncodedHeight
(416, 240)
>>> frame.planes[0]
array([41, 41, 41, ..., 41, 41, 41], dtype=uint8)
```

Audio stuff:

```python-console
>>> track_number = index.get_first_indexed_track_of_type(ffms2.FFMS_TYPE_AUDIO)
>>> asource = ffms2.AudioSource(source_file, track_number, index)
>>> aprops = asource.properties
>>> aprops.SampleRate, aprops.BitsPerSample, aprops.Channels
(48000, 16, 2)
>>> min_audio, max_audio = float("inf"), float("-inf")
>>> for audio in asource.linear_access(rate=100):
...     if audio.min() < min_audio:
...         min_audio = audio.min()
...     if audio.max() > max_audio:
...         max_audio = audio.max()
>>> min_audio, max_audio
(-16191, 18824)
```

`ffmsinfo.py` is a demo script showing how this package can be used.

Installation
------------

To install the package for Python 3, use:

```console
$ ./setup.py install
```

Prerequisites
-------------

- [Python 3.2+](http://www.python.org)
- [FFmpegSource](https://github.com/FFMS/ffms2)
- [numpy](http://www.numpy.org)

The API was designed to be an object-oriented and Pythonic version of the
original [FFmpegSource
API](https://github.com/FFMS/ffms2/blob/master/doc/ffms2-api.md).
