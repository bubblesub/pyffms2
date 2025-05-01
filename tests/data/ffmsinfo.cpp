#include <inttypes.h>
#include <string>

#include <ffms.h>

#define NULL_CHECK(arg) \
    do { \
        if (arg == nullptr) { \
            printf("The %s pointer is not valid\n", #arg); \
            exit(1); \
        } \
    } while(0)

#define CHECK(arg, val) \
    do { \
        if (arg != val) { \
            printf("%s and %s have different values\n", #arg, #val); \
            exit(1); \
        } \
    } while(0)


int main(int argc, char **argv) {
    std::string fileName = "morning rescue.mkv";

    // Video Index
    FFMS_Indexer* indexer = nullptr;
    FFMS_Index* index = nullptr;

    // Video source
    int video_track_idx = -1;
    FFMS_VideoSource* video_source = nullptr;
    const FFMS_VideoProperties* VP = nullptr;

    // Audio source
    int audio_track_idx = -1;
    FFMS_AudioSource* audio_source = nullptr;
    const FFMS_AudioProperties* AP = nullptr;

    FFMS_ErrorInfo E;
    char ErrorMsg[1024];

    E.Buffer = ErrorMsg;
    E.BufferSize = sizeof(ErrorMsg);

    FFMS_Init(0, 0);

    indexer = FFMS_CreateIndexer(fileName.c_str(), &E);
    NULL_CHECK(indexer);

    for (int track = 0; track < FFMS_GetNumTracksI(indexer); track++) {
        FFMS_TrackIndexSettings(indexer, track, 1, 0);
    }

    index = FFMS_DoIndexing2(indexer, 0, &E);
    NULL_CHECK(index);

    // Get Video Track
    video_track_idx = FFMS_GetFirstTrackOfType(index, FFMS_TYPE_VIDEO, &E);
    CHECK(video_track_idx, 0);

    video_source = FFMS_CreateVideoSource(
        fileName.c_str(),
        video_track_idx,
        index,
        1,
        FFMS_SEEK_NORMAL,
        &E
    );

    NULL_CHECK(video_source);

    VP = FFMS_GetVideoProperties(video_source);

    printf("\n\nVideo properties\n\n");
    printf(
        "\tFPS = %f\n",
        (VP->FPSNumerator / static_cast<double>(VP->FPSDenominator))
    );
    printf("\tDuration = %f\n", VP->LastTime);
    printf("\tNum Frames = %d\n\n", VP->NumFrames);

    // Get Audio Track
    audio_track_idx = FFMS_GetFirstTrackOfType(index, FFMS_TYPE_AUDIO, &E);
    CHECK(audio_track_idx, 1);

    audio_source = FFMS_CreateAudioSource(
        fileName.c_str(),
        audio_track_idx,
        index,
        FFMS_DELAY_FIRST_VIDEO_TRACK,
        &E
    );

    NULL_CHECK(audio_source);

    AP = FFMS_GetAudioProperties(audio_source);

    printf("\n\nAudio properties\n\n");
    printf("\tSample Rate = %d\n", AP->SampleRate);
    printf("\tNum Channels = %d\n", AP->Channels);
    printf("\tDuration = %f\n", AP->LastTime);
    printf("\tNum Samples = %" PRId64 "\n\n", AP->NumSamples);

    FFMS_DestroyIndex(index);
    FFMS_DestroyVideoSource(video_source);
    FFMS_DestroyAudioSource(audio_source);
    FFMS_Deinit();

    return 0;
}
