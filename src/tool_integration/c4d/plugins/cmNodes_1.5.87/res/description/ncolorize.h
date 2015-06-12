#ifndef _Ncolorize_H_
#define _Ncolorize_H_

enum                                            {
    NCLZ_LONG_CHANNEL                           = 1000,
    NCLZ_LONG_REPEAT,
    NCLZ_GRAD_COLOR,

    NCLZ_CHN_SEP                                = 0,
    NCLZ_CHN_LUM                                = 1,
    NCLZ_CHN_HUE                                = 2,
    NCLZ_CHN_SAT                                = 3,
    NCLZ_CHN_LGT                                = 4,
    NCLZ_CHN_RED                                = 5,
    NCLZ_CHN_GRN                                = 6,
    NCLZ_CHN_BLU                                = 7,

    NCLZ_RPT_NONE                               = 0,
    NCLZ_RPT_CYCLE                              = 1,
    NCLZ_RPT_MIRROR                             = 2,

    NCLZ_DUMMY
};

#endif
