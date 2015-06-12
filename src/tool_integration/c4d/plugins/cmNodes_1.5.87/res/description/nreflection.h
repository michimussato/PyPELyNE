#ifndef _Nreflection_H_
#define _Nreflection_H_

enum {
    NRFL_FIRST                  = 1000,

    NRFL_LONG_FALLOFF,
    NRFL_REAL_MINDISTANCE,
    NRFL_REAL_MAXDISTANCE,
    NRFL_BOOL_USEBUMP,
    NRFL_LONG_RAYLIMIT,
    NRFL_SPLINE_FALLOFF,

    NRFL_FALLOFF_NONE           = 0,
    NRFL_FALLOFF_LINEAR         = 1,
    NRFL_FALLOFF_SPLINE         = 2,

    NRFL_DUMMY
};

#endif
