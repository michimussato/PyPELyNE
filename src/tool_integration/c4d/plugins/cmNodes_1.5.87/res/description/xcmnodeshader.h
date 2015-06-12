#ifndef _Xcmnodeshader_H_
#define _Xcmnodeshader_H_

enum                                    {
    Xcmnodeshader                       = 1000,

    XCMNS_LINK_OUTPUT,
    XCMNS_LONG_CHANNEL,
    XCMNS_LONG_DATA1,
    XCMNS_LONG_VRAYADV_SHADER,

    XCMNS_CHANNEL_COLOR                 = 0,
    XCMNS_CHANNEL_DIFFUSION             = 1,
    XCMNS_CHANNEL_LUMINANCE             = 2,
    XCMNS_CHANNEL_TRANSPARENCY          = 3,
    XCMNS_CHANNEL_REFLECTION            = 4,
    XCMNS_CHANNEL_ENVIRONMENT           = 5,
    XCMNS_CHANNEL_FOG                   = 6,
    XCMNS_CHANNEL_BUMP                  = 7,
    XCMNS_CHANNEL_ALPHA                 = 8,
    XCMNS_CHANNEL_SPECULAR              = 9,
    XCMNS_CHANNEL_SPECULARCOLOR         = 10,
    XCMNS_CHANNEL_GLOW                  = 11,
    XCMNS_CHANNEL_DISPLACEMENT          = 12,
    XCMNS_CHANNEL_NORMAL                = 13,

    // Vray Advanced Material Shaders
    XCMNS_VA_COLOR1_SHADER = 4100,
    XCMNS_VA_COLOR1_TRANSPSHADER,
    XCMNS_VA_LUMINANCE_SHADER,
    XCMNS_VA_LUMINANCE_TRANSPSHADER,
    XCMNS_VA_TRANSPARENCY_SHADER,
    XCMNS_VA_TRANSPARENCY_TRANSPSHADER,
    XCMNS_VA_TRANSPARENCY_GLOSSINESSSHADER,
    XCMNS_VA_REFLECTION_SHADER,
    XCMNS_VA_REFLECTION_TRANSPSHADER,
    XCMNS_VA_BUMP_SHADER,
    XCMNS_VA_SPECULAR1_SHADER,
    XCMNS_VA_SPECULAR1_TRANSPSHADER,
    XCMNS_VA_SPECULAR1_HIGHLIGHTGLOSSSHADER,
    XCMNS_VA_SPECULAR1_REFLECTIONGLOSSSHADER,
    XCMNS_VA_SPECULAR2_SHADER,
    XCMNS_VA_SPECULAR2_TRANSPSHADER,
    XCMNS_VA_SPECULAR2_HIGHLIGHTGLOSSSHADER,
    XCMNS_VA_SPECULAR2_REFLECTIONGLOSSSHADER,
    XCMNS_VA_SPECULAR3_SHADER,
    XCMNS_VA_SPECULAR3_TRANSPSHADER,
    XCMNS_VA_SPECULAR3_HIGHLIGHTGLOSSSHADER,
    XCMNS_VA_SPECULAR3_REFLECTIONGLOSSSHADER,
    XCMNS_VA_TRANSP_SHADER,
    XCMNS_VA_SPECULAR4_SHADER,
    XCMNS_VA_SPECULAR4_TRANSPSHADER,
    XCMNS_VA_SPECULAR4_HIGHLIGHTGLOSSSHADER,
    XCMNS_VA_SPECULAR4_REFLECTIONGLOSSSHADER,
    XCMNS_VA_SPECULAR5_SHADER,
    XCMNS_VA_SPECULAR5_TRANSPSHADER,
    XCMNS_VA_SPECULAR5_HIGHLIGHTGLOSSSHADER,
    XCMNS_VA_SPECULAR5_REFLECTIONGLOSSSHADER,
    XCMNS_VA_COLOR2_SHADER,
    XCMNS_VA_COLOR2_TRANSPSHADER,
    XCMNS_VA_SPECULAR1_ANISOTROPYSHADER,
    XCMNS_VA_SPECULAR1_ANISOTROPYROTSHADER,
    XCMNS_VA_SPECULAR2_ANISOTROPYSHADER,
    XCMNS_VA_SPECULAR2_ANISOTROPYROTSHADER,
    XCMNS_VA_SPECULAR3_ANISOTROPYSHADER,
    XCMNS_VA_SPECULAR3_ANISOTROPYROTSHADER,
    XCMNS_VA_SPECULAR4_ANISOTROPYSHADER,
    XCMNS_VA_SPECULAR4_ANISOTROPYROTSHADER,
    XCMNS_VA_SPECULAR5_ANISOTROPYSHADER,
    XCMNS_VA_SPECULAR5_ANISOTROPYROTSHADER,
    XCMNS_VA_MATTE_OPSHADER,
    XCMNS_VA_MATTE_ALPHASHADER,
    XCMNS_VA_COLOR1_ROUGHNESSTEX,
    XCMNS_VA_COLOR2_ROUGHNESSTEX,
    XCMNS_VA_SPECULAR1_FRESNELREFLSHADER,
    XCMNS_VA_SPECULAR1_FRESNELREFRSHADER,
    XCMNS_VA_SPECULAR2_FRESNELREFLSHADER,
    XCMNS_VA_SPECULAR2_FRESNELREFRSHADER,
    XCMNS_VA_SPECULAR3_FRESNELREFLSHADER,
    XCMNS_VA_SPECULAR3_FRESNELREFRSHADER,
    XCMNS_VA_SPECULAR4_FRESNELREFLSHADER,
    XCMNS_VA_SPECULAR4_FRESNELREFRSHADER,
    XCMNS_VA_SPECULAR5_FRESNELREFLSHADER,
    XCMNS_VA_SPECULAR5_FRESNELREFRSHADER,
    XCMNS_VA_SSS_OVERALLCOLORSHADER,
    XCMNS_VA_SSS_SSSCOLORSHADER,
    XCMNS_VA_SSS_SCATTERSHADER,
    XCMNS_VA_SSS_SCATTERMULTSHADER,
    XCMNS_VA_COLOR1_DIRTRADIUSTEX,
    XCMNS_VA_COLOR1_DIRTOCCLUDED,
    XCMNS_VA_COLOR1_DIRTUNOCCLUDED,
    XCMNS_VA_COLOR2_DIRTRADIUSTEX,
    XCMNS_VA_COLOR2_DIRTOCCLUDED,
    XCMNS_VA_COLOR2_DIRTUNOCCLUDED,
    XCMNS_VA_LUMINANCE_DIRTRADIUSTEX,
    XCMNS_VA_LUMINANCE_DIRTOCCLUDED,
    XCMNS_VA_LUMINANCE_DIRTUNOCCLUDED,
    XCMNS_VA_COLOR1_SSSBACKSHADER,
    XCMNS_VA_FLAKES_COLORSHADER,
    XCMNS_VA_FLAKES_GLOSSINESSSHADER,
    XCMNS_VA_FLAKES_ORIENTATIONSHADER,

    XCMNS_DUMMY
};

#endif
