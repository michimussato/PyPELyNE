CONTAINER Nreflection                           {
    NAME Nreflection;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        LONG NRFL_LONG_FALLOFF                  {
            CYCLE                               {
                NRFL_FALLOFF_NONE;
                NRFL_FALLOFF_LINEAR;
                NRFL_FALLOFF_SPLINE;
            }
        }
        REAL NRFL_REAL_MINDISTANCE              {UNIT METER; MIN 0.0; STEP 0.1;}
        REAL NRFL_REAL_MAXDISTANCE              {UNIT METER; MIN 0.0; STEP 0.1;}
        SPLINE NRFL_SPLINE_FALLOFF              {
            SHOWGRID_H;
            GRIDSIZE_V 10; GRIDSIZE_H 10;
            X_MIN 0;
            X_MAX 1;
            Y_MIN 0;
            Y_MAX 1;
            X_STEPS 0.01;
            Y_STEPS 0.01;
        }
        LONG NRFL_LONG_RAYLIMIT                 {MIN 1; MAX 500;}
        BOOL NRFL_BOOL_USEBUMP                  {}
    }
}
