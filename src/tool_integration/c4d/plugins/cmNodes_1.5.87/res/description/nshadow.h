#ifndef _Nshadow_H_
#define _Nshadow_H_

enum {
    NSHD_FIRST                  = 1000,

    NSHD_REAL_INTENSITY,
    NSHD_BOOL_USEBUMP,
    NSHD_BOOL_CLAMP,
    NSHD_LONG_EXCLUSION_MODE,
    NSHD_INEX_LIGHTS,

    NSHD_MODE_INCLUDE           = 0,
    NSHD_MODE_EXCLUDE           = 1,

    NSHD_DUMMY
};

#endif
