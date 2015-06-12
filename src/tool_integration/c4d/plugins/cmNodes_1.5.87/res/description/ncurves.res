CONTAINER Ncurves                       {
    NAME Ncurves;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES       {
        DEFAULT 1;
        SHOW NB_GROUP_CHANNELS;

        SPLINE NCRV_SPLINE_CURVE        {
            SHOWGRID_H;
            GRIDSIZE_V 10; GRIDSIZE_H 10;
            X_MIN 0;
            X_MAX 1;
            Y_MIN 0;
            Y_MAX 1;
            X_STEPS 0.01;
            Y_STEPS 0.01;
        }

        SEPARATOR                       {LINE;}

        REAL NCRV_REAL_MIX             {UNIT PERCENT; MIN 0.0; MAX 100.0; MINSLIDER 0.0; MAXSLIDER 100.0; STEP 0.01; CUSTOMGUI REALSLIDER;}
    }
    SHOW NB_GROUP_MASKPROPERTIES;
}
