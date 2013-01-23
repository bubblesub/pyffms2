ffms – Python bindings for FFmpegSource
=======================================


Example usage
-------------

If you don’t need to keep the index, create a video source right away:

>>> import ffms
>>> source_file = "test/CINT_Nik_H264_720_512kb.mp4"
>>> vsource = ffms.VideoSource(source_file)


Or you can create an indexer:

>>> indexer = ffms.Indexer(source_file)
>>> indexer.format_name
'mov,mp4,m4a,3gp,3g2,mj2'
>>> indexer.track_info_list
[TrackInfo(type=0, codec_name='h264'), TrackInfo(type=1, codec_name='aac')]


Then create the index for the video source:

>>> index = indexer.do_indexing(-1)
>>> track_number = index.get_first_indexed_track_of_type(ffms.FFMS_TYPE_VIDEO)
>>> vsource = ffms.VideoSource(source_file, track_number, index)


Extract information from the video source:

>>> vsource.properties.NumFrames
1430
>>> vsource.track.keyframes[:5]
[0, 12, 24, 36, 48]
>>> vsource.track.timecodes[:5]
[0.0, 41.666666666666664, 83.33333333333333, 125.0, 166.66666666666666]


Retrieve a video frame:

>>> frame = vsource.get_frame(0)
>>> frame.EncodedWidth, frame.EncodedHeight
(416, 240)
>>> frame.planes[0]
array([41, 41, 41, ..., 41, 41, 41], dtype=uint8)


Audio stuff:

>>> track_number = index.get_first_indexed_track_of_type(ffms.FFMS_TYPE_AUDIO)
>>> asource = ffms.AudioSource(source_file, track_number, index)
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


``ffmsinfo.py`` is a demo script showing how this package can be used.


Installation
------------

To install the package for Python 3, use::

  $ ./setup.py install

To install the package for Python 2, use::

  $ python2 setup.py install

On Windows, you may use one of the MSI binary packages provided on the
`download page <https://bitbucket.org/spirit/ffms/downloads>`_.


Requirements
------------

- `Python 3.2+ <http://www.python.org>`_ (or 2.7)
- `FFmpegSource <http://code.google.com/p/ffmpegsource>`_
- `numpy <http://www.numpy.org>`_
- `pywin32 <http://sourceforge.net/projects/pywin32>`_ (Windows only)
- `lib3to2 <https://bitbucket.org/amentajo/lib3to2>`_
  (if installing for Python 2)


The API was designed to be an object-oriented and Pythonic version
of `the original FFmpegSource API
<http://ffmpegsource.googlecode.com/svn/trunk/doc/ffms2-api.html>`_.
