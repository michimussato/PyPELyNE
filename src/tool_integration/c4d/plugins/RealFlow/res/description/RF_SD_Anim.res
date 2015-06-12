CONTAINER RF_SD_ANIM
{
	NAME RFSDAnim;
	INCLUDE Obase;

	GROUP SD_ANIM_SETUP
	{
		DEFAULT 1;
		
		FILENAME SD_ANIM_FILE {}
		LONG SD_ANIM_START {}
		LONG SD_ANIM_END {}
		LONG SD_ANIM_OFFSET {}
		REAL SD_ANIM_SCALE {STEP 0.1;}
		BOOL SD_ANIM_LOCK_LAST {}
		BOOL SD_ANIM_LOCK_CURRENT {}
		BOOL SD_ANIM_INVERT_SEQUENCE {}
		SEPARATOR {LINE;}
		BUTTON SD_ANIM_CREATEKEYS {}
		BUTTON SD_ANIM_REMOVEKEYS {}
      SEPARATOR {LINE;}
      BOOL SD_ANIM_SHARE_ASSETS {}
	}
}
