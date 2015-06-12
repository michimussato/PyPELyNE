#ifndef _Nspecular_H_
#define _Nspecular_H_

enum {
    NSPC_FIRST                  = 1000,

    NSPC_REAL_INTENSITY,
    NSPC_REAL_FALLOFF,
    NSPC_REAL_OFFSET,
    NSPC_BOOL_USEBUMP,
    NSPC_LONG_EXCLUSION_MODE,
    NSPC_INEX_LIGHTS,
    NSPC_BOOL_USESHADOWS,

    NSPC_MODE_INCLUDE           = 0,
    NSPC_MODE_EXCLUDE           = 1,

    NSPC_DUMMY
};

#endif
