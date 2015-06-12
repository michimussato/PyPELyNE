CONTAINER Nedgedetect                           {
    NAME Nedgedetect;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;

        REAL NEDT_REAL_RADIUS                   {MIN 0.000001; STEP 0.001; CUSTOMGUI CM_REAL_GUI;}
        LONG NEDT_LONG_METHOD                   {
            CYCLE                               {
                NEDT_METHOD_SOBEL;
                NEDT_METHOD_PREWITT;
                NEDT_METHOD_KIRSH;
            }
        }
    }
}
