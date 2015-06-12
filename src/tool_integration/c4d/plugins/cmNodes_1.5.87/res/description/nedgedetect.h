#ifndef _Nedgedetect_H_
#define _Nedgedetect_H_

enum {
    NEDT_FIRST                  = 1000,

    NEDT_REAL_RADIUS,
    NEDT_LONG_METHOD,

    NEDT_METHOD_SOBEL           = 0,
    NEDT_METHOD_PREWITT         = 1,
    NEDT_METHOD_KIRSH           = 2,

    NEDT_DUMMY
};

#endif
