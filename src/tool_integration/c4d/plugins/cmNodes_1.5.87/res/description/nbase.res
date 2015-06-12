CONTAINER Nbase                         {
    NAME Nbase;
    SCALE_V;

    INCLUDE Obaselist;

    GROUP Obaselist                     {
        HIDE ID_LAYER_LINK;
        STRING NB_STRING_LABEL          {ANIM OFF;}
        STRING NB_STRING_NOTE           {ANIM OFF; CUSTOMGUI MULTISTRING; SCALE_V;}
        BOOL NB_BOOL_DISABLE            {}
        BOOL NB_BOOL_POSTAGESTAMP       {}
    }

    GROUP NB_GROUP_NODEPROPERTIES       {
        DEFAULT 1;
        GROUP NB_GROUP_CHANNELS         {
            COLUMNS 3;
            HIDDEN;

            BOOL NB_BOOL_CHN_RED        {}
            BOOL NB_BOOL_CHN_GREEN      {}
            BOOL NB_BOOL_CHN_BLUE       {}
        }
    }
    GROUP NB_GROUP_MASKPROPERTIES       {
        DEFAULT 1;
        COLUMNS 3;
        HIDDEN;

        BOOL NB_BOOL_MASK               {}
        LONG NB_LONG_MASK_CHANNEL       {
            CYCLE                       {
                NB_CHN_RED;
                NB_CHN_GREEN;
                NB_CHN_BLUE;
                NB_CHN_SEP;
                NB_CHN_AVERAGE;
            }
        }
        BOOL NB_BOOL_INVERT             {}
    }
}
