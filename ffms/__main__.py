"""Create FFMS index file
"""

import argparse
import os
import sys

import ffms


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__.strip(),
        prog="{} -m {}".format(os.path.basename(sys.executable), "ffms")
    )
    parser.add_argument("input_file", type=get_filename,
                        help="input media filename")
    parser.add_argument("output_file", nargs="?", type=get_filename,
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


# For Python 2
def get_filename(filename):
    if not isinstance(filename, str):
        filename = filename.decode(sys.stdin.encoding)
    return filename


def iter_video_tracks(index):
    return (track for track in index.tracks
            if track.type == ffms.FFMS_TYPE_VIDEO)


def get_progress_callback():
    def ic(current=0, total=1, private=None):
        pct = current * 100 // total
        if pct > ic.pct:
            sys.stdout.write("\rIndexing... {:d}%".format(pct))
            sys.stdout.flush()
            ic.pct = pct
        return 0

    ic.pct = -1
    return ic


def main():
    args = parse_args()
    output_file = args.output_file or args.input_file + ffms.FFINDEX_EXT
    ffms.set_log_level(ffms.AV_LOGS[args.verbose])

    if args.progress:
        stdout_write = sys.stdout.write
        ic = get_progress_callback()
    else:
        stdout_write = lambda s: None
        ic = None

    try:
        if os.path.isfile(output_file) and not args.force:
            print("Index file already exists:", output_file)
            index = ffms.Index.read(output_file)
        else:
            indexer = ffms.Indexer(args.input_file,
                                   ffms.DEMUXERS[args.demuxer])
            anc_private = args.audio_filename
            index = indexer.do_indexing(
                args.indexing_mask, args.decoding_mask,
                anc_private=anc_private,
                error_handling=args.error_handling,
                ic=ic
            )
            if ic and ic.pct < 100:
                ic(1)
            stdout_write("\nWriting index...\n")
            index.write(output_file)

        if args.timecodes:
            stdout_write("Writing timecodes...\n")
            for track in iter_video_tracks(index):
                track.write_timecodes()

        if args.keyframes:
            stdout_write("Writing keyframes...\n")
            for track in iter_video_tracks(index):
                track.write_keyframes()

    except ffms.Error as e:
        print("Error:", e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
