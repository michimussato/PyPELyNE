#ifndef _Ninfo_H_
#define _Ninfo_H_

enum                                            {
    NINF_LONG_INFO                              = 1000,

    NINF_BOOL_NORMALIZE,
    NINF_REAL_MINVAL,
    NINF_REAL_MAXVAL,
    NINF_BOOL_USEBUMP,

    NINF_INFO_FACING                            = 0,
    NINF_INFO_UVW                               = 1,
    NINF_INFO_CAMDIST                           = 2,
    NINF_INFO_ONORMAL                           = 3,
    NINF_INFO_WNORMAL                           = 4,
    NINF_INFO_CNORMAL                           = 5,
    NINF_INFO_OBJCOLOR                          = 6,
    NINF_INFO_NORMALDIR                         = 7,

    NINF_DUMMY
};

#endif
