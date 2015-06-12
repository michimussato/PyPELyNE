CONTAINER Ndistance                             {
    NAME Ndistance;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        REAL NDNST_REAL_DISTANCE                {MIN 0.0; UNIT METER;}
        LONG NDNST_LONG_EXCLUSION_MODE          {
            CYCLE                               {
                NDNST_MODE_INCLUDE;
                NDNST_MODE_EXCLUDE;
            }
        }
        IN_EXCLUDE NDNST_INEX_OBJECTS           {SCALE_V; NUM_FLAGS 0; ACCEPT {Obase;}}
    }
}
