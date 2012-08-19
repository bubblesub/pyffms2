#!/usr/bin/env python3
"""Extract information from media files.
"""

import os
import sys
import argparse

import ffms.console_mode #@UnusedImport


AUDIO_FORMATS = [
    "8-bit",
    "16-bit",
    "32-bit",
    "float",
    "double",
]

TYPES = [
    "video",
    "audio",
    "data",
    "subtitles",
    "attachment",
]


def parse_args():
    parser = argparse.ArgumentParser("ffmsinfo")
    parser.add_argument("source_files", type=str, nargs="+")
    parser.add_argument("-w", "--disable-write-index", dest="write_index",
                        action="store_false",
                        help="disable writing index to disk")
    parser.add_argument("-p", "--disable-progress", dest="progress",
                        action="store_false",
                        help="disable indexing progress reporting")
    parser.add_argument("--version", action="version",
                        version="FFMS {}".format(ffms.get_version()),
                        help="show FFMS version number")
    return parser.parse_args()


def create_index(indexer, write_index=True, progress=True, msg="Indexing…"):
    ic = ffms.init_progress_callback(msg) if progress else None
    index = indexer.do_indexing(-1, ic=ic)
    if ic:
        ic.done()
    if write_index:
        try:
            index.write()
        except ffms.Error as e:
            print(e, file=sys.stderr)
    return index


def main():
    args = parse_args()
    source_files = args.source_files

    for source_file in source_files:
        print(source_file)

        try:
            indexer = ffms.Indexer(source_file)
        except ffms.Error as e:
            print(e)
        else:
            format_name = indexer.format_name
            #source_type = indexer.source_type
            track_info_list = indexer.track_info_list
            index_file = source_file + ffms.FFINDEX_EXT

            if os.path.isfile(index_file):
                recreate_index = False
                try:
                    index = ffms.Index.read(index_file, source_file)
                except ffms.Error as e:
                    recreate_index = True
                    print(e, file=sys.stderr)
                else:
                    for track in index.tracks:
                        if (track.type == ffms.FFMS_TYPE_AUDIO and
                                not track.frame_info_list):
                            recreate_index = True
                            break
                if recreate_index:
                    index = create_index(indexer, args.write_index,
                                         args.progress, "Reindexing…")
            else:
                index = create_index(indexer, args.write_index, args.progress)

            print("format =", format_name)

            for n, (type_, codec_name) in enumerate(track_info_list):
                type_name = (TYPES[type_] if 0 <= type_ < len(TYPES)
                             else "unknown")
                #track = index.tracks[n]
                #time_base = track.time_base
                print("{}:".format(n))
                print("\ttype =", type_name)
                print("\tcodec =", codec_name)
                if type_ == ffms.FFMS_TYPE_VIDEO:
                    vsource = ffms.VideoSource(source_file, n, index)
                    vprops = vsource.properties
                    frame = vsource.get_frame(0)
                    sar_num, sar_den = ((vprops.SARNum, vprops.SARDen)
                                        if vprops.SARNum and vprops.SARDen
                                        else (1, 1))
                    aspect_ratio = (frame.EncodedWidth * sar_num /
                                    sar_den / frame.EncodedHeight)
                    print("\tresolution =", "{}×{}".format(
                        frame.EncodedWidth, frame.EncodedHeight))
                    print("\taspect ratio =", aspect_ratio)
                    print("\tfps =",
                          vprops.FPSNumerator / vprops.FPSDenominator)
                    print("\tduration =", vprops.LastTime - vprops.FirstTime)
                    print("\tnum frames =", vprops.NumFrames)
                elif type_ == ffms.FFMS_TYPE_AUDIO:
                    asource = ffms.AudioSource(source_file, n, index)
                    aprops = asource.properties
                    sample_format_name = (
                        AUDIO_FORMATS[aprops.SampleFormat]
                        if 0 <= aprops.SampleFormat < len(AUDIO_FORMATS)
                        else "unknown"
                    )
                    print("\tsample rate =", aprops.SampleRate),
                    #print("\tbits per sample =", aprops.BitsPerSample)
                    print("\tsample format =", sample_format_name)
                    print("\tnum channels =", aprops.Channels)
                    print("\tduration =", aprops.LastTime - aprops.FirstTime)
                    print("\tnum samples =", aprops.NumSamples)
        print()


if __name__ == "__main__":
    sys.exit(main())
