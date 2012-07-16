#!/usr/bin/env python3
"""Test suite for ffms
"""

import os
import unittest
from collections import namedtuple

import ffms


class TestFFMS(unittest.TestCase):
    SourceInfo = namedtuple("SourceInfo", ("file", "format_name"))
    TrackInfo = namedtuple("TrackInfo", ("type", "codec_name"))

    test_dir = "test"

    tests = [
        (SourceInfo("x264.mkv", "matroska"), [
            TrackInfo(ffms.FFMS_TYPE_VIDEO, "h264"),
        ]),
    ]

    def test_samples(self):
        for source_info, track_info_list in self.tests:
            source_path = os.path.join(self.test_dir, source_info.file)
            indexer = ffms.Indexer(source_path)
            self.assertEqual(indexer.format_name, source_info.format_name)
            index = ffms.Index.make(source_path)

            for n, (type_, codec_name) in enumerate(indexer.track_info_list):
                expected = track_info_list[n]
                self.assertEqual(type_, expected.type)
                self.assertEqual(codec_name, expected.codec_name)
                if type_ == ffms.FFMS_TYPE_VIDEO:
                    source = ffms.VideoSource(source_path, n, index)
                    source.properties
                elif type_ == ffms.FFMS_TYPE_AUDIO:
                    source = ffms.AudioSource(source_path, n, index)
                    source.properties


if __name__ == "__main__":
    unittest.main()
