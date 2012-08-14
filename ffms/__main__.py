"""Create FFMS index file
"""
from __future__ import print_function

import argparse
import ctypes
import os
import sys

import ffms


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__.strip(),
        prog="{} -m {}".format(os.path.basename(sys.executable), "ffms")
    )
    parser.add_argument("input_file",
                        help="input media filename")
    parser.add_argument("output_file", nargs="?",
                        help="output index filename")
    parser.add_argument("-f", "--force",
                        action="store_true",
                        help="overwrite existing index file")
    parser.add_argument("-v", "--verbose",
                        default=0, action="count",
                        help="FFmpeg verbosity level (can be repeated)")
    parser.add_argument("-p", "--disable-progress", dest="progress",
                        action="store_false",
                        help="disable progress reporting")
    parser.add_argument("-c", "--timecodes",
                        action="store_true",
                        help="write timecodes for video tracks")
    parser.add_argument("-k", "--keyframes",
                        action="store_true",
                        help="write keyframes for video tracks")
    parser.add_argument("-t", "--indexing-mask", metavar="N", type=int,
                        default=0,
                        help="audio indexing mask (-1 for all)")
    parser.add_argument("-d", "--decoding-mask", metavar="N", type=int,
                        default=0,
                        help="audio decoding mask (-1 for all)")
    parser.add_argument("-a", "--audio-filename", metavar="NAME",
                        default=ffms.DEFAULT_AUDIO_FILENAME_FORMAT,
                        help="audio filename format")
    parser.add_argument("-s", "--error-handling", metavar="N", type=int,
                        default=ffms.FFMS_IEH_STOP_TRACK,
                        help="audio decoding error handling")
    parser.add_argument("-m", "--demuxer", metavar="NAME",
                        default="default",
                        help="use the specified demuxer ({})"
                             .format(", ".join(ffms.DEMUXERS)))
    return parser.parse_args()


def iter_video_tracks(index):
    return (track for track in index.tracks
            if track.type == ffms.FFMS_TYPE_VIDEO)


def get_progress_callback():
    # Python 2 doesn’t support nonlocal.
    last_pct = ctypes.c_int(-1)

    def ic(current, total, private=None):
        pct = current * 100 // total
        if pct > last_pct.value:
            print("\rIndexing... {:d}%".format(pct), end="")
            last_pct.value = pct
        return 0

    return ic


def main():
    args = parse_args()
    print_if_progress = print if args.progress else lambda *args: None
    output_file = args.output_file or args.input_file + ffms.FFINDEX_EXT
    ffms.set_log_level(ffms.AV_LOGS[args.verbose])

    try:
        if os.path.isfile(output_file) and not args.force:
            print("Index file already exists:", output_file)
            index = ffms.Index.read(output_file)
        else:
            indexer = ffms.Indexer(args.input_file,
                                   ffms.DEMUXERS[args.demuxer])
            ic = get_progress_callback() if args.progress else None
            anc_private = args.audio_filename
            index = indexer.do_indexing(
                args.indexing_mask, args.decoding_mask,
                anc_private=anc_private,
                error_handling=args.error_handling,
                ic=ic
            )
            print_if_progress("\rIndexing... 100%")
            print_if_progress("Writing index...")
            index.write(output_file)

        if args.timecodes:
            print_if_progress("Writing timecodes...")
            for track in iter_video_tracks(index):
                track.write_timecodes()

        if args.keyframes:
            print_if_progress("Writing keyframes...")
            for track in iter_video_tracks(index):
                track.write_keyframes()

    except ffms.Error as e:
        print("Error:", e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
