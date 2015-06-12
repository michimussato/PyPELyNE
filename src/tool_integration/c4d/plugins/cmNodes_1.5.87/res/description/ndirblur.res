CONTAINER Ndirblur                              {
    NAME Ndirblur;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        SHOW NB_GROUP_CHANNELS;

        REAL NDBL_REAL_RADIUS                   {MIN 0.0; STEP 0.001; CUSTOMGUI CM_REAL_GUI;}
        REAL NDBL_REAL_ANGLE                    {UNIT DEGREE; STEP 0.001;}

        SEPARATOR                               {}

        LONG NDBL_LONG_DENSITY                  {
            CYCLE                               {
                NDBL_DENSITY_LOW;
                NDBL_DENSITY_MED;
                NDBL_DENSITY_HIGH;
                NDBL_DENSITY_CUSTOM;
            }
        }
        LONG NDBL_LONG_CUSTOM_DENSITY           {MIN 3;}

        SEPARATOR                               {LINE;}

        REAL NDBL_REAL_MIX                      {UNIT PERCENT; MIN 0.0; MAX 100.0; MINSLIDER 0.0; MAXSLIDER 100.0; STEP 0.01; CUSTOMGUI REALSLIDER;}
    }
    SHOW NB_GROUP_MASKPROPERTIES;
}
