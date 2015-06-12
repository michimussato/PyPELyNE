#ifndef _Ndiffuse_H_
#define _Ndiffuse_H_

enum {
    NDIF_FIRST                  = 1000,

    NDIF_REAL_INTENSITY,
    NDIF_REAL_FALLOFF,
    NDIF_BOOL_USEBUMP,
    NDIF_BOOL_USESHADOWS,
    NDIF_LONG_EXCLUSION_MODE,
    NDIF_INEX_LIGHTS,

    NDIF_MODE_INCLUDE           = 0,
    NDIF_MODE_EXCLUDE           = 1,

    NDIF_DUMMY
};

#endif
