#ifndef _RF_SD_Anim_H_
#define _RF_SD_Anim_H_

enum
{
	// groups
	SD_ANIM_SETUP				= 6000,

	SD_ANIM_FILE,
	SD_ANIM_START,
	SD_ANIM_END,
	SD_ANIM_OFFSET,
	SD_ANIM_SCALE,
	SD_ANIM_LOCK_LAST,
	SD_ANIM_LOCK_CURRENT,
	SD_ANIM_INVERT_SEQUENCE,
	SD_ANIM_CREATEKEYS,
	SD_ANIM_REMOVEKEYS,

	// v2.1.4 Maxwell - RF integration
	SD_ANIM_CURRENT_FRAME,

   // v2.4.3
   SD_ANIM_SHARE_ASSETS,
};

#endif
