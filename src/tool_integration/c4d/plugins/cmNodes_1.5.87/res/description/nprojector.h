#ifndef _Nprojector_H_
#define _Nprojector_H_

enum {
    NPRJ_LONG_PROJECTION        = 1000,
    NPRJ_BOOL_TILE,
    NPRJ_BOOL_SEAMLESS,
    NPRJ_REAL_OFFSET_U,
    NPRJ_REAL_OFFSET_V,
    NPRJ_REAL_LENGTH_U,
    NPRJ_REAL_LENGTH_V,
    NPRJ_VECTOR_POSITION,
    NPRJ_VECTOR_SIZE,
    NPRJ_VECTOR_ROTATION,
    NPRJ_BOOL_FORCE2D,

    NPRJ_PROJ_SPHERICAL         = 0,
    NPRJ_PROJ_CYLINDRICAL       = 1,
    NPRJ_PROJ_FLAT              = 2,
    NPRJ_PROJ_CUBIC             = 3,
    NPRJ_PROJ_FRONTAL           = 4,
    NPRJ_PROJ_SPATIAL           = 5,
    NPRJ_PROJ_UVW               = 6,
    NPRJ_PROJ_SHRINKWRAP        = 7,

    NPRJ_DUMMY
};

#endif
