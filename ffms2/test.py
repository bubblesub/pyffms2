#!/usr/bin/env python3
"""Test suite for ffms2."""

import unittest
from pathlib import Path

import ffms2

ROOT_DIR = Path(__file__).parent


class TestFFMS2(unittest.TestCase):
    def test_sample_video(self):
        source_path = Path(ROOT_DIR / "data/CINT_Nik_H264_720_512kb.mp4")

        indexer = ffms2.Indexer(source_path)
        self.assertEqual(indexer.format_name, "mov,mp4,m4a,3gp,3g2,mj2")

        track_info_list = list(indexer.track_info_list)
        for track_info in track_info_list:
            indexer.track_index_settings(track_info.num, 1, 0)

        self.assertEqual(track_info_list[0].codec_name, "h264")
        self.assertEqual(track_info_list[1].codec_name, "aac")

        index = indexer.do_indexing2()

        tracks = list(index.tracks)
        self.assertEqual(tracks[0].type, ffms2.FFMS_TYPE_VIDEO)
        self.assertEqual(tracks[1].type, ffms2.FFMS_TYPE_AUDIO)

        video_source = ffms2.VideoSource(source_path, 0, index)
        self.assertEqual(video_source.properties.ColorRange, 0)
        self.assertEqual(video_source.properties.ColorSpace, 2)
        self.assertEqual(video_source.properties.CropBottom, 0)
        self.assertEqual(video_source.properties.CropLeft, 0)
        self.assertEqual(video_source.properties.CropRight, 0)
        self.assertEqual(video_source.properties.CropTop, 0)
        self.assertEqual(video_source.properties.FPSNumerator, 24)
        self.assertEqual(video_source.properties.FPSDenominator, 1)
        self.assertEqual(video_source.properties.FirstTime, 0)
        self.assertEqual(video_source.properties.LastTime, 1429 / 24)
        self.assertEqual(video_source.properties.NumFrames, 1430)
        self.assertEqual(video_source.properties.RFFNumerator, 24)
        self.assertEqual(video_source.properties.RFFDenominator, 1)
        self.assertEqual(video_source.properties.SARNum, 0)
        self.assertEqual(video_source.properties.SARDen, 1)
        self.assertEqual(video_source.properties.TopFieldFirst, 0)

        audio_source = ffms2.AudioSource(source_path, 1, index)
        self.assertEqual(audio_source.properties.BitsPerSample, 32)
        self.assertEqual(audio_source.properties.ChannelLayout, 3)
        self.assertEqual(audio_source.properties.Channels, 2)
        self.assertEqual(audio_source.properties.FirstTime, 8 / 375)
        self.assertEqual(audio_source.properties.LastTime, 22336 / 375)
        self.assertEqual(audio_source.properties.NumSamples, 2860032)
        self.assertEqual(audio_source.properties.SampleFormat, 3)
        self.assertEqual(audio_source.properties.SampleRate, 48000)


if __name__ == "__main__":
    unittest.main()
