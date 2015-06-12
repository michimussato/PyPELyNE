CONTAINER Ndistort                              {
    NAME Ndistort;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        SHOW NB_GROUP_CHANNELS;

        GROUP                                   {
            COLUMNS 3;

            STATICTEXT NDST_STATIC_OFFSET       {}
            REAL NDST_REAL_OFFSET_X             {STEP 0.01;}
            REAL NDST_REAL_OFFSET_Y             {STEP 0.01;}

            STATICTEXT NDST_STATIC_SCALE        {}
            REAL NDST_REAL_SCALE_X              {UNIT PERCENT; STEP 1;}
            REAL NDST_REAL_SCALE_Y              {UNIT PERCENT; STEP 1;}
        }
        REAL NDST_REAL_STRENGTH                 {UNIT PERCENT; MINSLIDER 0.0; MAXSLIDER 100.0; STEP 0.1; CUSTOMGUI REALSLIDER;}

        SEPARATOR                               {LINE;}

        REAL NDST_REAL_MIX                      {UNIT PERCENT; MIN 0.0; MAX 100.0; MINSLIDER 0.0; MAXSLIDER 100.0; STEP 0.01; CUSTOMGUI REALSLIDER;}
    }
    SHOW NB_GROUP_MASKPROPERTIES;
}
