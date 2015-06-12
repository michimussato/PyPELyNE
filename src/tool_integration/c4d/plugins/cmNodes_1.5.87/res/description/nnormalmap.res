CONTAINER Nnormalmap                            {
    NAME Nnormalmap;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;

        REAL NNMP_REAL_RADIUS               {MIN 0.000001; STEP 0.001; CUSTOMGUI CM_REAL_GUI;}
        REAL NNMP_REAL_HEIGHT               {MIN 0.0; MAX 1.0; STEP 0.001; CUSTOMGUI CM_REAL_GUI;}
        LONG NNMP_LONG_METHOD               {
            CYCLE                           {
                NNMP_METHOD_SOBEL;
                NNMP_METHOD_PREWITT;
                NNMP_METHOD_KIRSH;
            }
        }
    }
}
