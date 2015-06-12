CONTAINER Ncondition                        {
    NAME Ncondition;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES           {
        DEFAULT 1;

        LONG NCND_LONG_CHANNEL              {
            CYCLE                           {
                NCND_CHN_LUM;
                NCND_CHN_SEP;
                NCND_CHN_HUE;
                NCND_CHN_SAT;
                NCND_CHN_LGT;
                NCND_CHN_SEP;
                NCND_CHN_RED;
                NCND_CHN_GRN;
                NCND_CHN_BLU;
            }
        }
        SPLINE NCND_SPLINE_DISTRIBUTION     {
            SHOWGRID_H;
            GRIDSIZE_V 10; GRIDSIZE_H 10;
            X_MIN 0;
            X_MAX 1;
            Y_MIN 0;
            Y_MAX 1;
            X_STEPS 0.01;
            Y_STEPS 0.01;
        }
        REAL NCND_REAL_FALLOFF              {MIN 0.0; MAX 1.0; STEP 0.01; CUSTOMGUI REALSLIDER;}
        BOOL NCND_BOOL_WRAP                 {}
    }
}
