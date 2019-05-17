"""av_log API
"""

AV_LOG_QUIET = -8

# Something went really wrong and we will crash now.
AV_LOG_PANIC = 0

# Something went wrong and recovery is not possible.
# For example, no header was found for a format which depends
# on headers or an illegal combination of parameters is used.
AV_LOG_FATAL = 8

# Something went wrong and cannot losslessly be recovered.
# However, not all future data is affected.
AV_LOG_ERROR = 16

# Something somehow does not look correct. This may or may not
# lead to problems. An example would be the use of '-vstrict -2'.
AV_LOG_WARNING = 24

AV_LOG_INFO = 32
AV_LOG_VERBOSE = 40

# Stuff which is only useful for libav* developers.
AV_LOG_DEBUG = 48
