CONTAINER Ncolorize                             {
    NAME Ncolorize;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;

        LONG NCLZ_LONG_CHANNEL                  {
            CYCLE                               {
                NCLZ_CHN_LUM;
                NCLZ_CHN_SEP;
                NCLZ_CHN_HUE;
                NCLZ_CHN_SAT;
                NCLZ_CHN_LGT;
                NCLZ_CHN_SEP;
                NCLZ_CHN_RED;
                NCLZ_CHN_GRN;
                NCLZ_CHN_BLU;
            }
        }
        LONG NCLZ_LONG_REPEAT                   {
            CYCLE                               {
                NCLZ_RPT_NONE;
                NCLZ_RPT_CYCLE;
                NCLZ_RPT_MIRROR;
            }
        }
        GRADIENT NCLZ_GRAD_COLOR                {ICC_BASEDOCUMENT;}
    }
}
