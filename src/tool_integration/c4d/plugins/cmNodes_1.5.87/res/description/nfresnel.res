CONTAINER Nfresnel                              {
    NAME Nfresnel;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        REAL NFNL_REAL_IOR                      {MIN 1.0; STEP 0.001;}
        BOOL NFNL_BOOL_USEBUMP                  {}
    }
}
