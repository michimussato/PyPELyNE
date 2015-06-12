CONTAINER Nmath                         {
    NAME Nmath;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES       {
        DEFAULT 1;
        SHOW NB_GROUP_CHANNELS;

        LONG NMTH_LONG_OPERATION        {
            CYCLE                       {
                NMTH_OP_ADD;
                NMTH_OP_SUB;
                NMTH_OP_MUL;
                NMTH_OP_DIV;
                NMTH_OP_MIN;
                NMTH_OP_MAX;
            }
        }
        REAL NMTH_REAL_MIX                      {UNIT PERCENT; MIN 0.0; MAX 100.0; MINSLIDER 0.0; MAXSLIDER 100.0; STEP 0.01; CUSTOMGUI REALSLIDER;}
    }
    SHOW NB_GROUP_MASKPROPERTIES;
}
