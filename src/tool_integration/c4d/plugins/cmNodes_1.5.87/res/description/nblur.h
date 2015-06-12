#ifndef _Nblur_H_
#define _Nblur_H_

enum {
    NBLR_FIRST                  = 1000,

    NBLR_REAL_SIZEX,
    NBLR_REAL_SIZEY,
    NBLR_BOOL_LINKSIZE,
    NBLR_LONG_DENSITY,
    NBLR_REAL_MIX,
    NBLR_LONG_CUSTOM_DENSITY,
    NBLR_LONG_BLUR_TYPE,

    NBLR_DENSITY_LOW            = 0,
    NBLR_DENSITY_MED            = 1,
    NBLR_DENSITY_HIGH           = 2,
    NBLR_DENSITY_CUSTOM         = 3,

    NBLR_TYPE_BOX               = 0,
    NBLR_TYPE_SIMPLE            = 1,
    NBLR_TYPE_GAUSSIAN          = 2,

    NBLR_DUMMY
};

#endif
