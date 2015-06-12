CONTAINER Nspecular                             {
    NAME Nspecular;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        REAL NSPC_REAL_INTENSITY                {MIN 0.0; STEP 0.001;}
        REAL NSPC_REAL_FALLOFF                  {MIN 0.0; STEP 0.001;}
        REAL NSPC_REAL_OFFSET                   {STEP 0.1;}
        BOOL NSPC_BOOL_USEBUMP                  {}
        BOOL NSPC_BOOL_USESHADOWS               {}
        SEPARATOR                               {LINE;}
        LONG NSPC_LONG_EXCLUSION_MODE           {
            CYCLE                               {
                NSPC_MODE_INCLUDE;
                NSPC_MODE_EXCLUDE;
            }
        }
        IN_EXCLUDE NSPC_INEX_LIGHTS             {SCALE_V; NUM_FLAGS 0; ACCEPT {Olight;}}
    }
}
