CONTAINER Ndiffuse                              {
    NAME Ndiffuse;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        REAL NDIF_REAL_INTENSITY                {MIN 0.0; STEP 0.001;}
        REAL NDIF_REAL_FALLOFF                  {MIN 0.0; STEP 0.001;}
        BOOL NDIF_BOOL_USEBUMP                  {}
        BOOL NDIF_BOOL_USESHADOWS               {}
        SEPARATOR                               {LINE;}
        LONG NDIF_LONG_EXCLUSION_MODE           {
            CYCLE                               {
                NDIF_MODE_INCLUDE;
                NDIF_MODE_EXCLUDE;
            }
        }
        IN_EXCLUDE NDIF_INEX_LIGHTS             {SCALE_V; NUM_FLAGS 0; ACCEPT {Olight;}}
    }
}
