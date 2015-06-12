#ifndef _Nbase_H_
#define _Nbase_H_

enum {
    //groups
    NB_GROUP_NODEPROPERTIES     = 801,
    NB_GROUP_MASKPROPERTIES,
    NB_GROUP_MISCPROPERTIES,
    NB_GROUP_CHANNELS,

    NB_PARAM_FIRST              = 820,

    //channel parameters
    NB_BOOL_CHN_RED,
    NB_BOOL_CHN_GREEN,
    NB_BOOL_CHN_BLUE,

    //mask properties
    NB_BOOL_MASK,
    NB_LONG_MASK_CHANNEL,
    NB_BOOL_INVERT,

    //misc properties
    NB_STRING_LABEL,
    NB_STRING_LABEL_AUTO,
    NB_BOOL_DISABLE,
    NB_BOOL_POSTAGESTAMP,
    NB_STRING_NOTE,

    //utility
    NB_BOOL_NODEINIT            = 900,
    NB_LONG_LASTPREVIEW         = 901,
    NB_BOOL_DIRTYPREVIEW        = 902,
    NB_BOOL_LFW                 = 903,
    NB_LONG_PROFILE             = 904,

    NB_CHN_SEP                  = 0,
    NB_CHN_RED                  = 1,
    NB_CHN_GREEN                = 2,
    NB_CHN_BLUE                 = 3,
    NB_CHN_AVERAGE              = 4,

    NB_DUMMY
};

#endif
