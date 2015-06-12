CONTAINER Nmatrix                               {
    NAME Nmatrix;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        SHOW NB_GROUP_CHANNELS;

        GROUP NMTX_GROUP_MATRIX_5X5             {
            DEFAULT 1;
            COLUMNS 5;

            LONG NMTX_LONG_MATRIX_01            {}
            LONG NMTX_LONG_MATRIX_02            {}
            LONG NMTX_LONG_MATRIX_03            {}
            LONG NMTX_LONG_MATRIX_04            {}
            LONG NMTX_LONG_MATRIX_05            {}

            LONG NMTX_LONG_MATRIX_06            {}
            LONG NMTX_LONG_MATRIX_07            {}
            LONG NMTX_LONG_MATRIX_08            {}
            LONG NMTX_LONG_MATRIX_09            {}
            LONG NMTX_LONG_MATRIX_10            {}

            LONG NMTX_LONG_MATRIX_11            {}
            LONG NMTX_LONG_MATRIX_12            {}
            LONG NMTX_LONG_MATRIX_13            {}
            LONG NMTX_LONG_MATRIX_14            {}
            LONG NMTX_LONG_MATRIX_15            {}

            LONG NMTX_LONG_MATRIX_16            {}
            LONG NMTX_LONG_MATRIX_17            {}
            LONG NMTX_LONG_MATRIX_18            {}
            LONG NMTX_LONG_MATRIX_19            {}
            LONG NMTX_LONG_MATRIX_20            {}

            LONG NMTX_LONG_MATRIX_21            {}
            LONG NMTX_LONG_MATRIX_22            {}
            LONG NMTX_LONG_MATRIX_23            {}
            LONG NMTX_LONG_MATRIX_24            {}
            LONG NMTX_LONG_MATRIX_25            {}
        }
        GROUP                                   {
            COLUMNS 1;

            REAL NMTX_REAL_DISTANCE             {MIN 0.000001; STEP 0.001; CUSTOMGUI CM_REAL_GUI;}
            REAL NMTX_REAL_ADD                  {MIN 0.0; STEP 0.01;}
            BOOL NMTX_BOOL_NORMALIZE            {}
        }
    }
    SHOW NB_GROUP_MASKPROPERTIES;
}
