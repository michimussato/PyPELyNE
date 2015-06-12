CONTAINER Nblur                                 {
    NAME Nblur;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        SHOW NB_GROUP_CHANNELS;

        REAL NBLR_REAL_SIZEX                    {MIN 0.0; STEP 0.001; CUSTOMGUI CM_REAL_GUI;}
        REAL NBLR_REAL_SIZEY                    {MIN 0.0; STEP 0.001; CUSTOMGUI CM_REAL_GUI;}
        BOOL NBLR_BOOL_LINKSIZE                 {}

        SEPARATOR                               {}

        LONG NBLR_LONG_BLUR_TYPE                {
            CYCLE                               {
                NBLR_TYPE_BOX;
                NBLR_TYPE_SIMPLE;
                NBLR_TYPE_GAUSSIAN;
            }
        }

        SEPARATOR                               {}

        LONG NBLR_LONG_DENSITY                  {
            CYCLE                               {
                NBLR_DENSITY_LOW;
                NBLR_DENSITY_MED;
                NBLR_DENSITY_HIGH;
                NBLR_DENSITY_CUSTOM;
            }
        }
        LONG NBLR_LONG_CUSTOM_DENSITY           {MIN 3;}

        SEPARATOR                               {LINE;}

        REAL NBLR_REAL_MIX                      {UNIT PERCENT; MIN 0.0; MAX 100.0; MINSLIDER 0.0; MAXSLIDER 100.0; STEP 0.01; CUSTOMGUI REALSLIDER;}
    }
    SHOW NB_GROUP_MASKPROPERTIES;
}
