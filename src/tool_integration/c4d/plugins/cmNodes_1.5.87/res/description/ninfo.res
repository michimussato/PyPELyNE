CONTAINER Ninfo                                 {
    NAME Ninfo;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;

        LONG NINF_LONG_INFO                     {
            CYCLE                               {
                NINF_INFO_FACING;
                NINF_INFO_OBJCOLOR;
                NINF_INFO_UVW;
                NINF_INFO_CAMDIST;
                NINF_INFO_ONORMAL;
                NINF_INFO_CNORMAL;
                NINF_INFO_WNORMAL;
                NINF_INFO_NORMALDIR;
            }
        }
        BOOL NINF_BOOL_NORMALIZE                {PARENTCOLLAPSE;}
        REAL NINF_REAL_MINVAL                   {UNIT METER; STEP 0.01; PARENTCOLLAPSE NINF_BOOL_NORMALIZE;}
        REAL NINF_REAL_MAXVAL                   {UNIT METER; STEP 0.01; PARENTCOLLAPSE NINF_BOOL_NORMALIZE;}
        BOOL NINF_BOOL_USEBUMP                  {}
    }
}
