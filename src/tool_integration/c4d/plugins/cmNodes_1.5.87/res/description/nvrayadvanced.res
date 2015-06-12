CONTAINER Nvrayadvanced {
    NAME Nvrayadvanced;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES {
        DEFAULT 1;

        LINK NVRAYADVANCED_LINK_MATERIAL {ACCEPT {ID_VRAYBRDF_MATERIAL;}}

        SEPARATOR {LINE;}

        BOOL VRAYMATERIAL_USE_MATTE {}
        BOOL VRAYMATERIAL_USE_TRANSP {}
        BOOL VRAYMATERIAL_USE_BUMP {}
        BOOL VRAYMATERIAL_USE_LUMINANCE {}
        BOOL VRAYMATERIAL_USE_FLAKES {}
        BOOL VRAYMATERIAL_USE_REFLECTION {}
        BOOL VRAYMATERIAL_USE_SPECULAR1 {}
        BOOL VRAYMATERIAL_USE_SPECULAR2 {}
        BOOL VRAYMATERIAL_USE_SPECULAR3 {}
        BOOL VRAYMATERIAL_USE_SPECULAR4 {}
        BOOL VRAYMATERIAL_USE_SPECULAR5 {}
        BOOL VRAYMATERIAL_USE_COLOR1 {}
        BOOL VRAYMATERIAL_USE_COLOR2 {}
        BOOL VRAYMATERIAL_USE_TRANSPARENCY {}
        BOOL VRAYMATERIAL_USE_SSS {}

        GROUP ID_VRAYMATERIALGROUP_MATTE {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_MATTE_OPSHADER {}
            BOOL VRAYMATERIAL_MATTE_ALPHASHADER {}
        }
        GROUP ID_VRAYMATERIALGROUP_TRANSP {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_TRANSP_SHADER {}
        }
        GROUP ID_VRAYMATERIALGROUP_BUMP {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_BUMP_SHADER {}
        }
        GROUP ID_VRAYMATERIALGROUP_LUMINANCE {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_LUMINANCE_SHADER {}
            BOOL VRAYMATERIAL_LUMINANCE_DIRTRADIUSTEX {}
            BOOL VRAYMATERIAL_LUMINANCE_DIRTOCCLUDED {}
            BOOL VRAYMATERIAL_LUMINANCE_DIRTUNOCCLUDED {}
            BOOL VRAYMATERIAL_LUMINANCE_TRANSPSHADER {}
        }
        GROUP ID_VRAYMATERIALGROUP_FLAKES {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_FLAKES_COLORSHADER {}
            BOOL VRAYMATERIAL_FLAKES_GLOSSINESSSHADER {}
            BOOL VRAYMATERIAL_FLAKES_ORIENTATIONSHADER {}
        }
        GROUP ID_VRAYMATERIALGROUP_REFLECTION {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_REFLECTION_SHADER {}
            BOOL VRAYMATERIAL_REFLECTION_TRANSPSHADER {}
        }
        GROUP ID_VRAYMATERIALGROUP_SPECULAR1 {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_SPECULAR1_SHADER {}
            BOOL VRAYMATERIAL_SPECULAR1_TRANSPSHADER {}
            BOOL VRAYMATERIAL_SPECULAR1_HIGHLIGHTGLOSSSHADER {}
            BOOL VRAYMATERIAL_SPECULAR1_REFLECTIONGLOSSSHADER {}
            BOOL VRAYMATERIAL_SPECULAR1_ANISOTROPYSHADER {}
            BOOL VRAYMATERIAL_SPECULAR1_ANISOTROPYROTSHADER {}
            BOOL VRAYMATERIAL_SPECULAR1_FRESNELREFLSHADER {}
            BOOL VRAYMATERIAL_SPECULAR1_FRESNELREFRSHADER {}
        }
        GROUP ID_VRAYMATERIALGROUP_SPECULAR2 {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_SPECULAR2_SHADER {}
            BOOL VRAYMATERIAL_SPECULAR2_TRANSPSHADER {}
            BOOL VRAYMATERIAL_SPECULAR2_HIGHLIGHTGLOSSSHADER {}
            BOOL VRAYMATERIAL_SPECULAR2_REFLECTIONGLOSSSHADER {}
            BOOL VRAYMATERIAL_SPECULAR2_ANISOTROPYSHADER {}
            BOOL VRAYMATERIAL_SPECULAR2_ANISOTROPYROTSHADER {}
            BOOL VRAYMATERIAL_SPECULAR2_FRESNELREFLSHADER {}
            BOOL VRAYMATERIAL_SPECULAR2_FRESNELREFRSHADER {}
        }
        GROUP ID_VRAYMATERIALGROUP_SPECULAR3 {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_SPECULAR3_SHADER {}
            BOOL VRAYMATERIAL_SPECULAR3_TRANSPSHADER {}
            BOOL VRAYMATERIAL_SPECULAR3_HIGHLIGHTGLOSSSHADER {}
            BOOL VRAYMATERIAL_SPECULAR3_REFLECTIONGLOSSSHADER {}
            BOOL VRAYMATERIAL_SPECULAR3_ANISOTROPYSHADER {}
            BOOL VRAYMATERIAL_SPECULAR3_ANISOTROPYROTSHADER {}
            BOOL VRAYMATERIAL_SPECULAR3_FRESNELREFLSHADER {}
            BOOL VRAYMATERIAL_SPECULAR3_FRESNELREFRSHADER {}
        }
        GROUP ID_VRAYMATERIALGROUP_SPECULAR4 {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_SPECULAR4_SHADER {}
            BOOL VRAYMATERIAL_SPECULAR4_TRANSPSHADER {}
            BOOL VRAYMATERIAL_SPECULAR4_HIGHLIGHTGLOSSSHADER {}
            BOOL VRAYMATERIAL_SPECULAR4_REFLECTIONGLOSSSHADER {}
            BOOL VRAYMATERIAL_SPECULAR4_ANISOTROPYSHADER {}
            BOOL VRAYMATERIAL_SPECULAR4_ANISOTROPYROTSHADER {}
            BOOL VRAYMATERIAL_SPECULAR4_FRESNELREFLSHADER {}
            BOOL VRAYMATERIAL_SPECULAR4_FRESNELREFRSHADER {}
        }
        GROUP ID_VRAYMATERIALGROUP_SPECULAR5 {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_SPECULAR5_SHADER {}
            BOOL VRAYMATERIAL_SPECULAR5_TRANSPSHADER {}
            BOOL VRAYMATERIAL_SPECULAR5_HIGHLIGHTGLOSSSHADER {}
            BOOL VRAYMATERIAL_SPECULAR5_REFLECTIONGLOSSSHADER {}
            BOOL VRAYMATERIAL_SPECULAR5_ANISOTROPYSHADER {}
            BOOL VRAYMATERIAL_SPECULAR5_ANISOTROPYROTSHADER {}
            BOOL VRAYMATERIAL_SPECULAR5_FRESNELREFLSHADER {}
            BOOL VRAYMATERIAL_SPECULAR5_FRESNELREFRSHADER {}
        }
        GROUP ID_VRAYMATERIALGROUP_COLOR {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_COLOR1_SHADER {}
            BOOL VRAYMATERIAL_COLOR1_DIRTRADIUSTEX {}
            BOOL VRAYMATERIAL_COLOR1_DIRTOCCLUDED {}
            BOOL VRAYMATERIAL_COLOR1_DIRTUNOCCLUDED {}
            BOOL VRAYMATERIAL_COLOR1_TRANSPSHADER {}
            BOOL VRAYMATERIAL_COLOR1_ROUGHNESSTEX {}
        }
        GROUP ID_VRAYMATERIALGROUP_COLOR2 {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_COLOR2_SHADER {}
            BOOL VRAYMATERIAL_COLOR2_DIRTRADIUSTEX {}
            BOOL VRAYMATERIAL_COLOR2_DIRTOCCLUDED {}
            BOOL VRAYMATERIAL_COLOR2_DIRTUNOCCLUDED {}
            BOOL VRAYMATERIAL_COLOR2_TRANSPSHADER {}
            BOOL VRAYMATERIAL_COLOR2_ROUGHNESSTEX {}
        }
        GROUP ID_VRAYMATERIALGROUP_TRANSPARENCY {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_TRANSPARENCY_SHADER {}
            BOOL VRAYMATERIAL_TRANSPARENCY_GLOSSINESSSHADER {}
            BOOL VRAYMATERIAL_COLOR1_SSSBACKSHADER {}
        }
        GROUP ID_VRAYMATERIALGROUP_SSS {
            HIDDEN;
            DEFAULT 1;
            BOOL VRAYMATERIAL_SSS_OVERALLCOLORSHADER {}
            BOOL VRAYMATERIAL_SSS_SSSCOLORSHADER {}
            BOOL VRAYMATERIAL_SSS_SCATTERSHADER {}
            BOOL VRAYMATERIAL_SSS_SCATTERMULTSHADER {}
        }
    }
}

