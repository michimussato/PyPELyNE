CONTAINER Ncopy                                 {
    NAME Ncopy;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;
        COLUMNS 2;

        BOOL NCPY_BOOL_RED                      {}
        LONG NCPY_LONG_RED                      {
            CYCLE                               {
                NCPY_CHN_RED;
                NCPY_CHN_GREEN;
                NCPY_CHN_BLUE;
            }
        }
        BOOL NCPY_BOOL_GREEN                    {}
        LONG NCPY_LONG_GREEN                    {
            CYCLE                               {
                NCPY_CHN_RED;
                NCPY_CHN_GREEN;
                NCPY_CHN_BLUE;
            }
        }
        BOOL NCPY_BOOL_BLUE                     {}
        LONG NCPY_LONG_BLUE                     {
            CYCLE                               {
                NCPY_CHN_RED;
                NCPY_CHN_GREEN;
                NCPY_CHN_BLUE;
            }
        }
    }
}
