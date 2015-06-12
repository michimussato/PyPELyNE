CONTAINER Nprojector                        {
    NAME Nprojector;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES           {
        DEFAULT 1;

        LONG NPRJ_LONG_PROJECTION           {
            CYCLE                           {
                NPRJ_PROJ_SPHERICAL;
                NPRJ_PROJ_CYLINDRICAL;
                NPRJ_PROJ_FLAT;
                NPRJ_PROJ_CUBIC;
                NPRJ_PROJ_FRONTAL;
                NPRJ_PROJ_SPATIAL;
                NPRJ_PROJ_UVW;
                NPRJ_PROJ_SHRINKWRAP;
            }
        }
        SEPARATOR                           {LINE;}
        BOOL NPRJ_BOOL_FORCE2D              {}
        BOOL NPRJ_BOOL_TILE                 {}
        BOOL NPRJ_BOOL_SEAMLESS             {}
        SEPARATOR                           {LINE;}
        GROUP                               {
            COLUMNS 2;
            REAL NPRJ_REAL_OFFSET_U         {STEP 0.01;}
            REAL NPRJ_REAL_OFFSET_V         {STEP 0.01;}
            REAL NPRJ_REAL_LENGTH_U         {STEP 0.01;}
            REAL NPRJ_REAL_LENGTH_V         {STEP 0.01;}
        }
        SEPARATOR                           {LINE;}
        VECTOR NPRJ_VECTOR_POSITION         {UNIT METER;}
        VECTOR NPRJ_VECTOR_SIZE             {UNIT METER;}
        VECTOR NPRJ_VECTOR_ROTATION         {UNIT DEGREE;}
    }
}
