CONTAINER Nshadow                               {
    NAME Nshadow;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        REAL NSHD_REAL_INTENSITY                {MIN 0.0; STEP 0.001;}
        BOOL NSHD_BOOL_USEBUMP                  {}
        BOOL NSHD_BOOL_CLAMP                    {}
        SEPARATOR                               {LINE;}
        LONG NSHD_LONG_EXCLUSION_MODE           {
            CYCLE                               {
                NSHD_MODE_INCLUDE;
                NSHD_MODE_EXCLUDE;
            }
        }
        IN_EXCLUDE NSHD_INEX_LIGHTS             {SCALE_V; NUM_FLAGS 0; ACCEPT {Olight;}}
    }
}
