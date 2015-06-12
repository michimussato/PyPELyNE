CONTAINER Nclamp                        {
    NAME Nclamp;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES       {
        DEFAULT 1;
        SHOW NB_GROUP_CHANNELS;

        SEPARATOR                       {LINE;}

        GROUP                           {
            COLUMNS 2;

            BOOL NCLMP_BOOL_MIN         {}
            COLOR NCLMP_COLOR_MIN       {OPEN;}

            BOOL NCLMP_BOOL_MAX         {}
            COLOR NCLMP_COLOR_MAX       {OPEN;}
        }

        SEPARATOR                       {LINE;}

        REAL NCLMP_REAL_MIX             {UNIT PERCENT; MIN 0.0; MAX 100.0; MINSLIDER 0.0; MAXSLIDER 100.0; STEP 0.01; CUSTOMGUI REALSLIDER;}
    }
    SHOW NB_GROUP_MASKPROPERTIES;
}
