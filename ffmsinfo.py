#!/usr/bin/env python3
"""Extract information from media files.
"""

import sys
import argparse

import ffms.console_mode #@UnusedImport


KEEP_INDEX_FILES = True

AUDIO_FORMATS = {
    ffms.FFMS_FMT_U8: "8-bit",
    ffms.FFMS_FMT_S16: "16-bit",
    ffms.FFMS_FMT_S32: "32-bit",
    ffms.FFMS_FMT_FLT: "float",
    ffms.FFMS_FMT_DBL: "double",
}


def parse_args():
    parser = argparse.ArgumentParser("ffmsinfo")
    parser.add_argument("source_files", type=str, nargs="+")
    parser.add_argument("-v", "--version", action="version",
                        version="FFMS version = {}".format(ffms.get_version()))
    parser.add_argument("-p", "--disable-progress", dest="progress",
                        action="store_false",
                        help="disable indexing progress reporting")
    return parser.parse_args()


def create_index(indexer, progress=True):
    ic = ffms.init_progress_callback() if progress else None
    index = indexer.do_indexing(-1, ic=ic)
    if ic:
        ic.done()
    if KEEP_INDEX_FILES:
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
            print()
            continue

        format_name = indexer.format_name
        source_type = indexer.source_type
        track_info_list = indexer.track_info_list

        print("format = {} ({})".format(format_name, source_type))

        try:
            index = ffms.Index.read(source_file=source_file)
        except ffms.Error as e:
            index = create_index(indexer, args.progress)
        else:
            # Recreate the index if there are any unindexed audio tracks.
            for track in index.tracks:
                if (track.type == ffms.FFMS_TYPE_AUDIO and
                        not track.frame_info_list):
                    index = create_index(indexer, args.progress)
                    break

        for n, (type_, codec_name) in enumerate(track_info_list):
            if type_ == ffms.FFMS_TYPE_VIDEO:
                vsource = ffms.VideoSource(source_file, n, index)
                vprops = vsource.properties
                frame = vsource.get_frame(0)
                sar_num, sar_den = ((vprops.SARNum, vprops.SARDen)
                                    if vprops.SARNum and vprops.SARDen
                                    else (1, 1))
                aspect_ratio = (frame.EncodedWidth * sar_num /
                                sar_den / frame.EncodedHeight)
                print("{}: video track:".format(n))
                print("\tcodec =", codec_name)
                print("\tresolution =", "{}×{}".format(
                    frame.EncodedWidth, frame.EncodedHeight))
                print("\taspect ratio =", aspect_ratio)
                print("\tfps =", vprops.FPSNumerator / vprops.FPSDenominator)
                print("\tnum frames =", vprops.NumFrames)
                print("\tduration (s) =", vprops.LastTime - vprops.FirstTime)
            elif type_ == ffms.FFMS_TYPE_AUDIO:
                asource = ffms.AudioSource(source_file, n, index)
                aprops = asource.properties
                sample_format_name = AUDIO_FORMATS.get(
                    aprops.SampleFormat, "unknown")
                print("{}: audio track: ".format(n))
                print("\tcodec =", codec_name)
                print("\tsample rate =", aprops.SampleRate),
                #print("\tbits per sample =", aprops.BitsPerSample)
                print("\tsample format =", sample_format_name)
                print("\tnum channels =", aprops.Channels)
                print("\tnum samples =", aprops.NumSamples)
                print("\tduration (s) =", aprops.LastTime - aprops.FirstTime)
            else:
                if type_ == ffms.FFMS_TYPE_DATA:
                    print("{}: data track: ".format(n))
                elif type_ == ffms.FFMS_TYPE_SUBTITLE:
                    print("{}: subtitle track: ".format(n))
                elif type_ == ffms.FFMS_TYPE_ATTACHMENT:
                    print("{}: attachment track: ".format(n))
                else:
                    print("{}: unknown track: ".format(n))
                print("\tcodec =", codec_name)

        print()


if __name__ == "__main__":
    sys.exit(main())
