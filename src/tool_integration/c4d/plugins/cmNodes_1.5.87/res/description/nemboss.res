CONTAINER Nemboss                               {
    NAME Nemboss;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        SHOW NB_GROUP_CHANNELS;

        GROUP                                   {
            REAL NEMB_REAL_INTENSITY            {STEP 0.01;}
            REAL NEMB_REAL_RADIUS               {MIN 0.000001; STEP 0.001; CUSTOMGUI CM_REAL_GUI;}
            REAL NEMB_REAL_ANGLE                {UNIT DEGREE;  STEP 0.1;}
            BOOL NEMB_BOOL_ADDITIVE             {}
        }
    }
    SHOW NB_GROUP_MASKPROPERTIES;
}
