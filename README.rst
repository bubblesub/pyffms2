ffms – Python bindings for FFmpegSource
=======================================


Example usage
-------------

If you don’t need to keep the index, create a video source right away:

>>> import ffms
>>> source_file = "test/x264.mkv"
>>> vsource = ffms.VideoSource(source_file)


Or you can create an indexer:

>>> indexer = ffms.Indexer(source_file)
>>> indexer.format_name
'matroska'
>>> indexer.track_info_list
[TrackInfo(type=0, codec_name='h264')]


Then create the index for the video source:

>>> index = indexer.do_indexing(-1)
>>> track_number = index.get_first_indexed_track_of_type(ffms.FFMS_TYPE_VIDEO)
>>> vsource = ffms.VideoSource(source_file, track_number, index)


Extract information from the video source:

>>> vsource.properties.NumFrames
8
>>> vsource.track.keyframes
[0, 5]
>>> vsource.track.timecodes
[0.0, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0, 6000.0, 7000.0]


Retrieve a video frame:

>>> frame = vsource.get_frame(0)
>>> frame.EncodedWidth, frame.EncodedHeight
(128, 72)
>>> frame.planes[0]
array([16, 16, 16, ..., 16, 16, 16], dtype=uint8)


ffmsinfo.py is a demo script showing how this package can be used.


Requirements
------------

- `FFmpegSource <http://code.google.com/p/ffmpegsource/>`_
- `numpy <http://www.numpy.org/>`_


Additional requirements under Windows
-------------------------------------

- `pywin32 <http://sourceforge.net/projects/pywin32/>`_


The API was designed to be an object-oriented and Pythonic version
of the original FFmpegSource API. For more information, you can have a look
at the `original API documentation
<http://ffmpegsource.googlecode.com/svn/trunk/doc/ffms2-api.html>`_
