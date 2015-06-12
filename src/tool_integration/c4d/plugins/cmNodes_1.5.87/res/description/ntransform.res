CONTAINER Ntransform                            {
    NAME Ntransform;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;

        GROUP                                   {
            COLUMNS 2;

            BOOL NTFM_BOOL_MIRROR               {}
            BOOL NTFM_BOOL_FLIP                 {}
        }

        GROUP                                   {
            COLUMNS 3;

            STATICTEXT NTFM_STATIC_TRANSLATE    {}
            REAL NTFM_REAL_TRANSLATE_X          {STEP 0.01;}
            REAL NTFM_REAL_TRANSLATE_Y          {STEP 0.01;}

            STATICTEXT NTFM_STATIC_ROTATE       {}
            REAL NTFM_REAL_ROTATE               {UNIT DEGREE;  STEP 0.1;}
            STATICTEXT NTFM_STATIC_1            {}

            STATICTEXT NTFM_STATIC_SCALE        {}
            REAL NTFM_REAL_SCALE_X              {UNIT PERCENT; STEP 1;}
            REAL NTFM_REAL_SCALE_Y              {UNIT PERCENT; STEP 1;}

            STATICTEXT NTFM_STATIC_CENTER       {}
            REAL NTFM_REAL_CENTER_X             {STEP 0.01;}
            REAL NTFM_REAL_CENTER_Y             {STEP 0.01;}
        }
    }
}
