CONTAINER Nshuffle {
    NAME Nshuffle;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        COLUMNS 1;

        LONG NSHF_LONG_SHUFFLE_RED              {
            CYCLE                               {
                NSHF_CHN_RED;
                NSHF_CHN_GREEN;
                NSHF_CHN_BLUE;
                NSHF_CHN_SEP;
                NSHF_CHN_WHITE;
                NSHF_CHN_BLACK;
            }
        }
        LONG NSHF_LONG_SHUFFLE_GREEN            {
            CYCLE                               {
                NSHF_CHN_RED;
                NSHF_CHN_GREEN;
                NSHF_CHN_BLUE;
                NSHF_CHN_SEP;
                NSHF_CHN_WHITE;
                NSHF_CHN_BLACK;
            }
        }
        LONG NSHF_LONG_SHUFFLE_BLUE             {
            CYCLE                               {
                NSHF_CHN_RED;
                NSHF_CHN_GREEN;
                NSHF_CHN_BLUE;
                NSHF_CHN_SEP;
                NSHF_CHN_WHITE;
                NSHF_CHN_BLACK;
            }
        }
    }
}
