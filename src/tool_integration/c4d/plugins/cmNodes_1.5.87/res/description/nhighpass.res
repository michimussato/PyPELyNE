CONTAINER Nhighpass                             {
    NAME Nhighpass;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        REAL NHPS_REAL_RADIUS                   {MIN 0.0; STEP 0.001; CUSTOMGUI CM_REAL_GUI;}

        SEPARATOR                               {}

        LONG NHPS_LONG_DENSITY                  {
            CYCLE                               {
                NHPS_DENSITY_LOW;
                NHPS_DENSITY_MED;
                NHPS_DENSITY_HIGH;
                NHPS_DENSITY_CUSTOM;
            }
        }
        LONG NHPS_LONG_CUSTOM_DENSITY           {MIN 3;}
    }
}
