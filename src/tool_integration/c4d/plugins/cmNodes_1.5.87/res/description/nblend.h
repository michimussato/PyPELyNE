#ifndef _Nblend_H_
#define _Nblend_H_

enum                                            {
    NBLN_LONG_BLENDMODE                         = 1000,
    NBLN_REAL_MIX,

    NBLN_MODE_SEP                               =  0,
    NBLN_MODE_NORMAL                            =  1,
    NBLN_MODE_DARKEN                            =  2,
    NBLN_MODE_MULTIPLY                          =  3,
    NBLN_MODE_COLORBURN                         =  4,
    NBLN_MODE_LINEARBURN                        =  5,
    NBLN_MODE_DARKERCOLOR                       =  6,
    NBLN_MODE_LIGHTEN                           =  7,
    NBLN_MODE_SCREEN                            =  8,
    NBLN_MODE_COLORDODGE                        =  9,
    NBLN_MODE_LINEARDODGE                       = 10,
    NBLN_MODE_LIGHTERCOLOR                      = 11,
    NBLN_MODE_OVERLAY                           = 12,
    NBLN_MODE_SOFTLIGHT                         = 13,
    NBLN_MODE_HARDLIGHT                         = 14,
    NBLN_MODE_VIVIDLIGHT                        = 15,
    NBLN_MODE_LINEARLIGHT                       = 16,
    NBLN_MODE_PINLIGHT                          = 17,
    NBLN_MODE_HARDMIX                           = 18,
    NBLN_MODE_DIFFERENCE                        = 19,
    NBLN_MODE_EXCLUSION                         = 20,
    NBLN_MODE_SUBTRACT                          = 21,
    NBLN_MODE_DIVIDE                            = 22,
    NBLN_MODE_HUE                               = 23,
    NBLN_MODE_SATURATION                        = 24,
    NBLN_MODE_COLOR                             = 25,
    NBLN_MODE_LUMINOSITY                        = 26,
    NBLN_MODE_LEVR                              = 27,
    NBLN_MODE_GRAINEXTRACT                      = 28,
    NBLN_MODE_GRAINMERGE                        = 29,

    NBLN_DUMMY
};

#endif
