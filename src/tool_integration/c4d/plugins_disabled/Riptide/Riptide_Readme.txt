 
                                  Red-i Productions Presents
                                       Riptide v1.9
                              Wavefront .Obj Import/Export Plugin
                                    for Maxon's Cinema 4D

                                Copyright 2008 by Keith Young
                                      (a.k.a. Spanki)
                                  http://www.skinprops.com
                                  


May 2, 2008
---------------

 

End User License:
==========================================================

While this package and contents are being distributed free of charge, it remains Copyright by Keith Young.
You are free to use this package on one or many installations, but you may not decompile or otherwise
reverse-engineer this product or use any parts of it in your own products.  You are free to distribute the
package provided no fee is charged over and above the cost of the delivery medium (ie. the nominal price of
a CD and postage) and that the package and all contents including copyright notices remain intact, as published.
Any questions regarding this license can be directed to:  spanki@skinprops.com



Disclaimer:
==========================================================

While every effort has been made to insure the intended and safe operation of this utility and there are no known
disastrous error conditions, we can not anticipate every situation and therefore can not guarantee 100% error-free
operation.  By using this software, the user agrees not hold Red-i Productions, it's employees or agents or
Keith Young responsible for any loss of work, loss of time, mental stress, or any other actual or perceived damages
caused by the use of this software.  In short, this utility comes with NO WARRANTEE, EITHER EXPRESSED OR IMPLIED -
USE AT YOUR OWN RISK.



Introduction:
==========================================================

I got frustrated by the inflexible way that C4D handles .obj files and decided that I could do a better job of it -
this plugin package is the result.

Included in this package is a "Wavefront .obj File Format Import/Export Filter Plugin".  The current plugin consists
of 2 new tags - a "Group Tag" and a "Region Tag" used to (optionally) specify 'Groups' and 'UVMapper Regions', along
with the Import and Export filters with extensive output/formatting options.

See the "Usage Information, Notes and Tips" section below for operational details and background information.



Revision History:
==========================================================

v1.9
--------
This is primarily a bug-fix release, with some maintenance changes.

- Fixed facet-parsing order bug

  Some of the re-organizational changes in the v1.8 release caused a problem where if the facet records (polygons)
  had all 3 index types (vertex/tex vertex/normal vertex indices), the parsor would trigger too early and ignore the
  uv/texture indices.  There may also have been similar problems with some of the other various facet formats. This
  should now be fixed. [My thanks to "rsquires" for pointing out this issue and sending me sample problem files]
  
- Fixed some cases where UVMapper Regions would be lost (spaces in names)

- Fixed another long-standing potential bug and/or memory-leak in export code.

- Additional internal structural changes (preparation of code as basis for the Pro version)

- Some non-standard material cleanup on export (my notes are sparse on this, so that's all I can say about it :) )



v1.8
--------
This release primarily focuses on a major Ngon-handling update/re-write...

- Bug/Feature-Fix:  Much improved Ngon handling

  When I first implemented Ngon support in Riptide, it was a bit of a struggle finding the necessary information that
  Riptide needed - Ngons are implemented as a layer on top of existing triangles and quads in C4D and some of the
  developer documentation on the subject (and access routines for utilizing Ngons) was confusing, and/or not really
  suited to the task at hand.  Anyway, I managed to glue enough code together to get Ngon support implemented a while
  back, but there were a few problems with that implementation...
  
  1. When importing, I was using very simplistic triangulation (a fan of triangles) to form the underlying polygons
     (triangles/quads are still there - Ngons are layered on top of them). This approach meant that only 'Convex'
     Ngons would load correctly - 'Concave' Ngons (quite popular from apps like SketchUp) would end up with bad
     polygons. [ And, it was just plain ugly ;) ]
     
  2. Either my import or my export (or both) would not maintain vertex ordering of the Ngon indices. The vertices
     themselves are never re-ordered, so this did not affect Poser morphs, but ZBrush (for example) also relies on
     the indices used by triangles and quads remaining the same and it's possible that those were changing in the
     triangulation process - of course ZBrush also doesn't handle Ngons anyway, so you already had to deal with
     those before-hand, but it may have been an issue with some other app(s).
  
  3. Because of all the crazy (non-compliant) .obj file formatting Riptide supports, there was tons of "similar, but
     mostly duplicated" paths through the code, which left a lot of room for cut/paste errors on my part.
  
  4. Related to the above, there were some other somewhat obscure problems found and fixed during the re-write.

  ...basically, I gutted the Import and Export Ngon handling code and started over from scratch.  The new Import code
  uses Cinema4D's internal triangulation routines, resulting in quads/triangles and support for 'Concave' Ngons.  This
  also included a fairly substantial re-structuring of my general polygon parsing code.  With some additional effort,
  It now also maintains vertex-ordering for Ngons (yay).

  There may or may not be (new) bugs in the code (none that I've found yet), but a side-benifit of the re-structuring
  is that it's now more consolidated (less room for typos) and easier to maintain.
  
  [NOTE: Ngons with 'holes' in them are still not supported (no way that I know of to represent those in a .obj file)]
  
  Finally, I also added support for "f v/ v/ v/" and fixed support for "f v// v// v//" formatted facet records (neither
  of which are compliant with the file format spec, but you'd be amazed at some of the stuff I've seen in .obj files).
  Riptide can currently parse the following facet record formats:
  
  fo <plus any of the below>   (really old format used 'fo' instead of 'f' for faces)
  f v v v                      (<--- compliant, vertex-only)
  f v/ v/ v/
  f v// v// v//
  f v/t v/t v/t                (<--- compliant, vertex + texture vertex)
  f v/t/ v/t/ v/t/
  f v//n v//n v//n             (<--- compliant, vertex + normal)
  f v/t/n v/t/n v/t/n          (<--- compliant, vertex + texture + normal)
  
  ...the v/t/n in the above examples are stand-ins for some 'vertex index' (an index into one of the tables), which can
  also be specified as negative offsets, which Riptide also supports, along with any embedded '\' line-continuation.
  
  Anyway, "better Ngon support" was one of the few (only?) remaining reasons to force use of the C4D built-in .obj
  import/export - despite it's other issues, it handled Concave Ngons just fine.  But enough geek-speak.. as usual, for
  more information or any questions, please visit the Riptide Support Forums -
  ( http://skinprops.com/ext/forum/forum_viewforum.php?9 ).


- Functionality: Holy Ngons

  Speaking of Ngons with 'holes' in them (like a window cut out of a wall), since these can not be saved to a .obj file,
  a check is now run on the document before prompting for a filename.  If any Ngons are found with holes in them on any
  mesh that is subject to export (visible and not restricted by an export mask tag), a new Yes/No dialog will pop up...
  
  "At least one mesh object contains Ngons with 'holes'...
  
  Click Yes to disable exporting Ngons and Continue.
  Click No to Cancel."
  
  ...if you click Yes, the export process will continue, but the "Export Ngons" option will be disabled (it/they will be
  written out as individual triangles and/or quads instead of a 4+ sided Ngon).  If you click No, the export is aborted.
  
  To fix these Ngons for export, you can try knifing at least one new edge from an interior hole edge/vertex out to an
  exterior edge or vertex of the Ngon.
  

- Enhancement: Material Handling change

  There was a recent inquiry about how materials are loaded/set when there's an existing material with the same name as
  one being loaded (when you merge an import into an existing scene).  The short answer is that IF it's a 'standard' C4D
  material (ie. not a 'Shader' or Plugin material of some sort) and it has the same name, it would be updated with data
  read from the .mtl file.  If it did not exist, or a non-standard material with that name existed, a new material
  would be created with the .mtl file data.

  If you already had a bunch of materials in the scene converted to Vray materials (whatever format that is), or some
  other plugin material, this could leave you with a lot of work to clean up all the material references.
  
  With this release, the functionality has changed as follows:
  
  * if no material exists in the scene with the desired name, a new one is created.
  * if a 'standard' C4D material exists in the scene with the desired name, it will be updated.
  * if any non-standard (or plugin) material exists in the scene with the desired name, it will be used, but not
    altered.
  
  ...this change means that shaders (like Nukei, Banji, Danel, Fog, Cheen, etc) as well as any plugin materials (like
  Vray) would be used if they were already set up in the scene.  I don't have Vray and hadn't done a lot of testing
  with this change, so let me know if there's any problems.

  [ NOTE: As always, only standard materials can be 'exported' ].


- Bug/Functionality: Bump Map record change in .mtl files

  As noted in the previous release, the Wavefront .mtl file-spec indicates that the record for a Bump Map file is 'bump'.
  Some applications use 'map_bump' and some (including all previous versions of Riptide) use 'map_Bump'.
  
  One design goal I've tried to follow with Riptide is:
  
  * on import, parse/support as much odd-ball formatting as possible for any supported features/records
  * on export, don't create any odd-ball formatting or non-compliant records
  
  ...with this in mind, I have decided to take the high-road and change Riptide to use the proper 'bump' record on
  export, to be compliant with the file-spec. Of course Riptide will still accept any of the 3 when importing, so this
  only affects files exported by Riptide.



v1.7
--------
This is a bug-fix release, with a few other changes...

- Bug-Fix:  Export crash when too many unused verts

  I'm really quite baffled how this particular bug has never been reported, since it's potentially been in the code for
  _years_ now... thanks to "tantarus" for reporting it!

  Basically, if you delete a bunch of polygons from your mesh, but don't go back and 'Optimize' the mesh to get rid of
  all the extra (now unused) vertices, this can (could) result in a crash when you went to export the mesh.  There was
  somewhat of a buffer that could save the day in some cases (depending on the number of unused vertices and _which_
  vertices were still being used by the remaining polygons), but that relied on luck more than anything.

  Anyway, this bug has now been fixed.


- Enhancement:  Better duplicate UV/Normal removal

  While fixing the above problem, I noticed that my code that consolidated duplicate UV and Normal indices was not
  really working as originally planned.  Both of these tables (UVs and Normals) in exported files are now optimized to
  remove any/all duplicate entries.  This can result in smaller output .obj files.

  [NOTE: the mesh vertices are NOT optimized to remove duplicates, since that would change the vertex-ordering,
         breaking morph creation with some apps, as well as some issues with the C4D<->ZBrush pipeline.  This also
         means that unused vertices are still being written/read from the .obj files to keep the ordering the same]


- Enhancement:  .mtl file changes

  I have been reviewing the official .mtl file spec and have made a few tweaks here and there to values being saved/read
  based on that (though many options are still not handled or even parsed).  There may have been other changes, but the
  few that come to mind are:
  
  * an Index of Refraction value ('Ni' record) is now being set/parsed if the material has transparency. As with various
    other values, the range defined by the wavefront .mtl spec (0.001 <-> 10.0) and the range used by C4D (0.25 <-> 4.0)
    differ.  Since this is a precise value, I do not try to do any conversion/scaling... it is simply clamped to the
    range used by C4D.

  * some apps write out a "map_bump" record, some apps (including Riptide) use "map_Bump" and it turns out that neither
    of those are part of the .mtl file spec - the proper record is simply "bump" :).  Riptide will now accept any of
    those and (for the time-being) is still using "map_Bump" when it creates a file (I need to do more research to
    determine the impact on other modern apps before a decision is made).

  * Displacement ("disp") map records are now read and written.

  * some apps were/are incorrectly adding file-path info to various texture filenames... these are now stripped off.



v1.6
--------
This is a general nit-pick / bug fix / enhancement release...

- Version consolidation...

  Starting a few versions ago, I decided to stop updating the plugin for earlier versions of Cinema4D.  This and future
  updates are limited to C4D R9.1 or later.  In the previous update, there were some changes needed in the code to
  move from R9.1 to R9.6 and/or R10 and later versions.  I have back-fitted those changes into the R9.1 code-base so the
  archive now includes:
  
  Riptide.cdl - compatible with PC R9.1 - R10.5 (and presumably later versions, but time will tell)
  Riptide.xdl - compatible with Mac PowerPC R9.1 - R9.6
  Riptide.dylib - compatible with Mac Universal Binary R9.6 - R10.5 (and presumably later versions, but time will tell)
  
  ...in other words, there's now only one distribution that supports both Mac and PC, R9.1 or later.  There are two notes
  related to this...
  
  1. My demo version of R9.6 on the Mac doesn't seem to want to load any plugins, so it hasn't been tested there - please
     let me know if you have any problems.
     
  2. Currently, I do not yet have a 64-bit PC version.  I will try to work out something on this as time and resources
     permit.
     

- Bug Fix: Repeating Dialog...

  If you ever tried exporting a mesh that used 'Shader' materials (like Banji, Banzi, Cheen, Danel, etc) then you've
  probably seen this dialog pop up...
  
              "Riptide does not support "Shader" materials - using default."
              
  ...over and over and over and over again.  Well, Riptide still does not support Shader materials, but because of
  where that check was placed in the code, it was displaying that dialog for every polygon assigned to that material,
  which was quite annoying, to say the least :) (most people probably assumed that the plugin had entered an endless
  loop, but it would actually end, if you clicked away enough dialogs).
  
  This update changes this to a simple debug print message (which can only be seen in the Console window) and is also
  now just printed once per mesh in the scene that has one of these materials on it.


- Improved Material (.mtl file) import/export...

  As mentioned in original documentation (below), there's not really a great 1-to-1 correspondence between Wavefront
  .mtl file materials and Cinema4D materials.  The file format only supports a subset of the C4D material parameters,
  so I have to convert those (and/or fill in some defaults) as best as possible.
  
  In previous versions of the plugin, the exporter always wrote out values for things like Specular Color, even if
  that channel was not enabled.  The importer also always set those values (to some defaults), even if the .mtl file
  didn't have data for them.  This often resulted in having (for example) Specular Color enabled, but set to Black.
  In this update, the plugin tries to be a bit smarter about what gets written on export and what gets enabled after
  importing.
  
  Within the limits of the file format, the new plugin does a much better job at re-creating materials (though there
  are still some limits, as well as some old .mtl files floating around with bad colors in them - if you fix the
  settings and re-save your .obj files, it should fix the materials).
  

- Better Phong Tag handling...

  When Riptide imports a .obj file, it creates a Phong Tag on the mesh within C4D in order to enable smooth shading.
  Previous versions of the plugin just left it like that... this update also takes the time to enable the "Angle Limit"
  option (angle set to 80deg).  This fixes a huge source of difference between the appearance of meshes loaded by
  Riptide vs. meshes loaded by C4D's built-in .obj loader.  Sharp edges should now look sharp, while rounder parts of
  the mesh get smoothed.  You may still want to adjust the angle value on the Phong Tag to suit your mesh.


- Better Export control...

  The plugin will NOW ONLY EXPORT OBJECTS THAT ARE CURRENTLY VISIBLE IN THE EDITOR WINDOW. This gives you another level
  of control over what gets exported from your scene.  Visibility (and therefore exportability) is based on the little
  grey/red/green tick-mark for the editor window (NOT the one for Rendering visibility).  Basically, if you can see
  the mesh in edit mode, it gets exported (but read the paragraph below).  Likewise, if you can't see it, it won't be
  exported.
  
  A few versions ago, I introduced a new "Export Mask Tag" to give you some level of control over what gets exported
  out of a scene and what doesn't.  That tag is still active and can still be used to mask entire branches of the
  Object Manager hierarchy from being exported - regardless of the visibility tick-mark settings of that branch.
  
  This means that you can have additional scenery, back-up meshes or other meshes in the scene for reference purposes
  as you do your model ling and either temporarily hide them before exporting or use an Export Mask Tag to keep them
  from being exported along with the model you're working on.
  
  
- Enhanced UV-map handling...

  This may take a little explaining, but the short version of the story is that the plugin now does a better job of
  determining proper uv-mapping when your Texture Tags are set to something besides UVW Mapping, or you've adjusted
  the Offset/Length/Tiles values.  For those interested, below is the longer explanation...
  
  Background:
  
  * The Wavefront .obj file format supports one type of mapping - UVW Mapping (or uv-mapping).
  * Cinema4D stores the UV values in it's UVWTag that is attached to polygonal mesh objects.
  * When you set a Texture Tag's Projection to UVW Mapping, C4D uses the uv values stored in that UVWTag.
  * C4D also lets you set Texture Tags to use other types of mapping, like Spherical, Cylindrical, Cubic, Frontal, etc.
  * If the Texture Tag's projection is set to anything other than UVW Mapping, the UVWTag on the mesh is ignored by C4D
    and the projection is 'computed', based on the projection type.
  * In addition to the Projection type, you can also change the X/Y Offset and Length/Tiling of each Texture Tag.
  * These Offset/Length/Tiles values affect all types of Projections (including UVW Mapping), but the affects that they
    have on the resulting mapping are not stored in the UVWTag's uv-values (think of them as a post-process).
  * For all Projection types EXCEPT for UVW Mapping, you can also use the Texture Tool and Texture Axis Tool to modify
    the axis (rotation, scaling and position) used to control how the Projection is applied (these tools have no affect
    on UVW Mapping).

  [ In the discussion above, note that I'm referring specifically to how the _Texture Tag(s)_ on your mesh are set up...
   BodyPaint also has tools to let you perform various types of projections (Cylindrical, Spherical, etc), but those all
   result in creating hard uv-values which are only used if your Texture Tag's Projection type is set to UVW Mapping ] 

  ...ok, with the above in mind, all previous versions of Riptide determined the uv-mapping as follows:
  
  + retrieve UVWTag from mesh
  + retrieve uv-values from UVWTag
  + do some fancy filtering to remove duplicate values (to create smaller files)
  + do any horizontal/vertical flipping adjustments (based on user selected options)
  + write out adjusted uv-values to file.
  
  ...so again, with the bullet-points above in mind, note that if you had Texture Tags on your mesh that used Spherical
  mapping (for example), Riptide would still just grab the UVWTag (which was being ignored by C4D) and write out
  whatever was in there. Even if your Texture Tag was set to UVW Mapping, if you had changed any of the Offset, Length
  or Tiles values, those were also being ignored by Riptide.
  
  In this version of the plugin, I've tried to address all of the above.  It's possible that I'm still not creating
  _exactly_ the same output that the built-in exporter does (I haven't done extensive testing yet), but you should find
  it MUCH closer to being correct than it was, in those cases.

  
- Bug Fix: Ngon UV-map handling...

  Speaking of UV-map enhancements, I finally tracked down an elusive bug that would sometimes assign a bad UV value to
  one (possibly more than one) vertex of an Ngon. This would typically show up as the vertex inadvertently being mapped
  to the bottom-left corner of the 0-1 UV space.  This bug only happened under some specific circumstances, which made
  it difficult to reproduce and therefore fix.



v1.5
--------
This release provides R10 support, as well as fixing some R9.6 issues...

- Will now export Ngons in R9.6+ (Maxon changed the way Ngons were accessed in R9.6, requiring changes and a recompile). 

- Bug Fix: v1.4 (for C4D R9.1 - R9.5) had support for exporting Ngons, but there was a bug when using the "C4D Ordering"
  option for Face Sorting (sorting by Material Group or Region worked fine).  The bug caused it to only save out the
  first Ngon found in the mesh.  This is now fixed (I still have to go back and fix this in the R9.1 version of the plugin,
  so keep an eye out for that).
  
- Apparently, Riptide stopped exporting groups and regions altogether in R10 - but no one bothered mentioning that to me,
  so I just now noticed it... fixed. (I'm currently still using C4D R9.1, so if you find problems with later versions,
  please report them so I can look into them - thanks).

- Added some additional error-reporting for start-up issues.  If the plugin fails to load for some reason, open the
  console window and look for any error messages.

- Support: I have spent a fair amount of time overhauling my web-site ( http://skinprops.com ), adding support forums in
  the process.  Please direct any support questions/issues/bug reports to the forums there - thanks.



v1.4
--------
Along with a new 'Export Mask' feature (see below), my objective with this release (and the previous release) was to
continue refining my IO routines to make this plugin more robust on reading various .obj and .mtl files, as well as
exporting .obj and .mtl files that are compatible with more 3D applications (without relying on the user knowing a
bunch of work-arounds). So the first few items listed below fall into this category...

- Riptide can now Import .mtl files that have spaces in their filenames, but other apps can't, so...

- On Export, Riptide will replace those spaces with underscores ('_').  Some apps (Poser, Hexagon, to name a few) do
not support spaces in the .mtl filename.  So if you export your mesh as "My New Mesh.obj", the .mtl file will now be
named "My_New_Mesh.mtl"

- Riptide now supports line-continuation ('\') and end-of-line comments ('!') in .obj (and .mtl) files on Import.
Since some apps don't support these features, Riptide doesn't create any when Exporting files.

- ** New Feature **

Previously, Riptide always exported any mesh it found in the scene... which can be a pain in the butt in some cases
(like when using PoseMixer, or if you just have some hidden backup copies of your mesh lying around in the scene).
To address this, there is now a new "Export Mask" tag that can be added to any Object Manager object that blocks it
from being Exported.  The tag can be found in the same place as the Group and Region tags ("Riptide Tags").

If you click on the Export Mask tag, you'll see 2 options in the attribute manager...

Enable - determines whether or not this tag is active or not.
Apply to Children - determines whether or not any children of this node are also hidden or not.

...these can be toggled on/off for the desired result.

By default, it will also block any children of that node from being exported, so if, for example, you have a bunch
of meshes in a scene that you don't want exported, you could put them all under a NULL object and add one of these
new "Export Mask" tags to that NULL and everything under that branch would be hidden from the Export code.

(NOTE: This new tag (and it's options) required some new string files and/or entries, but I have not yet had the new
text translated into other languages... if you'd like to translate them for me, zip up just that language folder (for
example just the "strings_de" folder and all of it's contents) and e-mail that to me (typhoon[AT]jetbroadband.com)...
I'll make the updated language files available for download on my site - thanks).



v1.3
--------

- For Export, Riptide now handles spaces in selection tag names by changing them to an underscore ('_'), for all cases
(Material, Group and Region selection tag names).

- On Import, Riptide now replaces spaces in Material names with an underscore ('_')... note that Region names can not
contain spaces and Group names are still treated as earlier versions (currently, polygons can only belong to one group...
group names are created based on the LAST string after a space on the 'g ' group record in the .obj file).

- On Import, the names for default (unassigned) Materials, Groups and Regions used to all be "default", which caused some
confusion with the related Selection Tag names... the new names are: "default_Mat", "default_Grp", "default_Rgn".


v1.2c
--------

- Fixed a crash bug if 'Export Normals' was disabled.  Oddly, only one person (out of about 200) noticed, or at least
mentioned, this bug - I can't fix bugs when I don't know they exist - Thanks Ed! :).


v1.2b
--------

- Fixed an issue where a comment line meant for the .mtl file was inadvertently written to the .obj file (not fatal,
just messy).


v1.2a
--------
It looks like I got too excited about finally getting the Ngon code to work (it was a battle :) and didn't go back and
verify all the various paths through the code so...

- Fixed crash bug when exporting with 'Export Ngons' NOT checked.

- Fixed crash bug when importing if there were more than 1000 Ngons in the file - new code is only limited by memory.


v1.2
--------
- Riptide will now Import/Export Ngons* (polygons with >4 sides). There are new import/export options to create Ngons**.

* NOTE: Ngons are only supported in R9+. This plugin requires R9.102 or later (the R9.102 update is available as a free
update from R9.0 at Maxon's web site).

** NOTE: The .obj file format does not support Ngons with 'holes' in them (like a window cut out of a wall panel),
so if you end up with strangely formed or overlapping polygons, go back to your original document and look for and fix
any holes before exporting (this plugin does not fix these for you like the built-in exporter does).

- Fixed an export bug related to not having uv-mapped a mesh before exporting.

- Fixed an export crash bug related to using BhodiNut Shaders.

- Added support for MakeHuman.exe's goofy facet record formatting.  Riptide now supports the following formats of that
record on import (v=vertex, t=texture, n=normal indices):

v v v
v// v// v//      (<-- MakeHuman uses this one)
v/t v/t v/t
v/t/ v/t/ v/t/   (<-- another odd one that some apps use)
v//n v//n v//n
v/t/n v/t/n v/t/n

...Riptide exports using one of the 4 un-commented formats above.


v1.0b
--------
- Mac port.


v1.0a
--------
- Bug-fix for triangulating Ngons on import.


v1.0
--------
- First release version.



Files Needed:
==========================================================

To fully utilize this package you will need the following:

- Cinema 4D R9.102 or later (plugins for R7.3 and R8.5 are also available on my web site).
- A desire for more flexibility in your .obj file output ;).



Installation:
==========================================================

This plugin is currently written for two main versions of Cinema 4D...

1. Copy the zip file into the "Plugins" folder of your C4D installation and unzip it there.
2. A new "Riptide" folder will be created, with everything needed to run the plugin.
3. Restart the C4D application to load the new plugin(s).
4. See the "Usage Information, Notes and Tips:" section below for usage details.



Detailed File List:
==========================================================
\Riptide\
Riptide.cdl
Riptide_Readme.txt

\Riptide\res\
redilogo.tif
RegionTag.tif
GroupTag.tif
c4d_symbols.h
riptide.tif

\Riptide\res\dialogs\
dlg_grouptag.res
dlg_regiontag.res
dlg_impfile.res
dlg_expfile.res

\Riptide\res\strings_us\
c4d_strings.str

\Riptide\res\strings_us\dialogs\
dlg_grouptag.str
dlg_regiontag.str
dlg_expfile.str
dlg_impfile.str

\Riptide\res\strings_de\
c4d_strings.str

\Riptide\res\strings_de\dialogs\
dlg_grouptag.str
dlg_regiontag.str
dlg_expfile.str
dlg_impfile.str

\Riptide\res\strings_fr\
c4d_strings.str

\Riptide\res\strings_fr\dialogs\
dlg_grouptag.str
dlg_regiontag.str
dlg_expfile.str
dlg_impfile.str

\Riptide\res\strings_jp\
c4d_strings.str

\Riptide\res\strings_jp\dialogs\
dlg_grouptag.str
dlg_regiontag.str
dlg_expfile.str
dlg_impfile.str

\Riptide\res\strings_sp\
c4d_strings.str

\Riptide\res\strings_sp\dialogs\
dlg_grouptag.str
dlg_regiontag.str
dlg_expfile.str
dlg_impfile.str



Usage Information, Notes and Tips:
==========================================================


Background:
=============================

I guess I should start by describing some of the reasoning/issues behind writing this plugin...  I primarily use C4D
to produce clothing/props/models to be used in Poser.  Poser supports several 3D formats, but I'm very familiar with
the Wavefront .obj format, it's very flexible, it's ASCII (easily accessible) and it's become the somewhat de facto
standard among Poser artists.  However, C4D's implementation of the format leaves some things to be desired...


C4D .obj Export Issues:
=============================

- all 'materials' from a particular mesh are condensed and combined into the first material listed on the mesh.  This
is probably the biggest problem I continually ran into.  I might have a dozen or more material selections defined on
a single mesh (skinhead, lips, nostrils, eyesockets, innermouth, gums, skinbody, fingernails, toenails, nipples, etc),
but when I export the model, I was LOSING all of those material selections and had to recreate them using some external
application (UVMapper, for example).  It's very easy to define these selections within C4D and can be quite a pain to
do in other applications... so losing them all on export sucks.

- no real 'group' support and/or inflexible group support, where it exists.  Basically, C4D creates ONE group record
for each 'mesh' (a separate group of polygons) contained in the document and the group name is basically made up from
all of the grouping hierarchy used within the C4D tree, so you might end up with something like:

Hyper_NURBS:Symmetry:Eye_Base:Left_Eye

...as a group name in the .obj file (note that the ':'s are added by C4D on import - they are spaces in the .obj file).

This is perfectly valid and probably a reasonable approach (C4D is a general-purpose 3D editor and not designed around
the .obj file format), but the file format allows for MULTIPLE groups per mesh, which can all share the same set of
vertices (see the import section below for additional issues related to this).

Anyway, a typical Poser humanoid character might have dozens of groups within the same 'mesh' (head, neck, chest, abdomen,
hip, left collar, right collar, left shoulder, right shoulder, left forearm, right forearm, lots-o-finger-segments, you
get the idea...). Short of creating separate 'meshes' for each of these 'groups', there's no way of defining them within
C4D currently.

- normals are 'reversed'. This one is no big deal really... they had to pick a direction, but the one they picked doesn't
happen to coincide with Poser's idea of which way they should face (or even C4D's, for that matter, so I guess they get
a 'bonk' for this one as well ;).  Anyway, the normals can be flipped around on import to Poser, export from UVMapper or
prior to export in C4D, but the new plugin makes it easy to get it right to start with.

- no support for UVMapper 'regions'.  As far as I know, 'regions' are something Steve Cox (author of UVMapper) came up
with and implemented as an extension to the .obj format (using comment fields), so this issue is clearly not an omission
with the C4D code, but I thought it would be handy to be able to define these while modelling, to help with UV Mapping
and layout later on (these 'regions' are just another way of grouping polygons together, but they are separate from and
can 'span' across group boundaries, which makes them very useful).


C4D .obj Import Issues:
=============================

- Material import... while C4D drops the ball on exporting materials, it actually does retain/recreate the proper polygon
selections on import.  I guess my only real issues/complaints here is the choice of naming of those selections ("Selection 1"
.. "Selection 2" .. "Selection 3", etc.).  Why not just use the material name(s)?  And the fact that it makes no attempt to
actually read the .mtl file and reproduce any of the desired material settings.

- Groups.  This is a tough one and I can't really cast to much blame for this one.  Programmatically, it's very difficult
(very time-comsuming, at the least) to determine the 'intent' of how a .obj file should be broken up upon import into
separate meshes.  There are a couple of obvious choices...

a) create one big mesh, and create polygon selection tags for each 'group' record.
b) create a separate mesh for each group record.

...C4D chose option 'b'.  Unfortunately, neither of those options is optimal in all situations, though option 'a' would
have been less 'destructive'.  By that, I'm referring to the fact that implementing option 'b' means creating new
vertices at the seams between what used to be group selections of the same mesh.  This can screw up vertex ordering, for
things like morph files.

- Loss of UVMapper regions.  Again, I'm not casting blame on this one, but an import filter could preserve (recreate)
these as polygon selections.

- Lack of additional import options.  There are no options to flip normals or textures or.. well, any options, aside from
the scaling factor.



Implementation:
==========================================================

Ok, so now you know some of the issues I was trying to address and while I was at it, I came up with some additional
features to add flexibility.  The plugin itself is made up of two new Tags, as well as an Import and Export plugins.  Below
I will describe the role and function of each.


Group Tag
=============================

This is a new tag that can be attached to your polygonal mesh objects (Editable Meshes).  To add one, right-click
on the mesh name in the Objects Tab, then select "New Tag->Plugin Tags->Group Tag" (or just "New Tag->Group Tag" in v8.x)
from the menu.  A dialog will open, displaying all available/current (and named, btw) 'Polygon Selection Tags'.  You can
move these from the 'Available' to the 'Selected' list (and back) by highlighting them with the mouse and clicking on the
appropriate arrow gadgets.

By moving a selection to the 'Selected' list, you are basically defining that polygon selection as a 'Group'.  The
export filter will scan this list of selections and create the appropriate group records within the .obj file.  The
tag itself will be saved/loaded with your .c4d file.


Region Tag
=============================

This new tag functions identically to the Group Tag outlined above.  To add one, right-click on the mesh name in the
Objects Tab, then select "New Tag->Plugin Tags->UVM Region Tag" (or just "New Tag->UVM Region Tag" in v8.x) from the menu.

By moving a selection to the 'Selected' list, you are basically defining that polygon selection as a 'UVMapper Region'.
The export filter will scan this list of selections and create the appropriate region records within the .obj file.


Tag implementation/background
=============================

The polygon selection tags in C4D are a pretty good match for material/group/region selections in a .obj file, but there
are some differences you should be aware of.  The primary difference is that while individual polygons may exist in more
than one C4D selection (overlap), they may only exist in ONE .obj file material/group/region selection.  The same polygon
can be in one material AND one group AND one region, but it can't be in more than one of each type.  This is accounted for
in the code by assigning each polygon to the first selection it exists in (for each selection type - material/group/region).

For example, let's say that you have a humanoid model, with a 'Body' C4D selection tag, that encompasses every polygon of
the mesh.  You also have a 'hip' C4D selection tag that only contains polygons that make up the hip area.  Suppose you
want to create 'Group' records for each of these selections... obviously, there is overlap between the selections, so if
the 'Body' selection is listed before (to the left of) the 'hip' selection, ALL of the polygons will go into the 'Body'
group and the 'hip' group will be lost.  To get around this problem, you could either move the 'hip' C4D selection tag
ahead (to the left) of the 'Body' tag, or remove the hip polygons from the Body selection.

I hope that makes sense... you only need to worry about overlap within the same type of group (a UVMapper Region could
encompass/span several 'groups', for example, which is why they are useful to begin with ;).

Other considerations:

- selections must be NAMED to show up as 'Available' in the assignment dialogs.
- selections that are deleted or renamed after being added to the group/region lists are not removed/updated in those
  lists, which won't hurt anything, but you'll have to update them manually to get the expected results.


.obj Export Plugin
=============================

Once the plugin is installed, a new option shows up in the Plugins menu, named "Riptide".  One of it's sub-menus is named
".Obj Exporter".  After selecting a filename, an export options dialog will appear.  Below is a description of each option...

o Scale Factor:
  This is used for scaling the output mesh and should be set to the same value as the C4D .obj import/export value.

o Export Ngons (only available in the v9.102 plugin)
  IF your model has N-gons in it (polygons with more than 4 sides), they will be exported as such in the .obj file.

* NOTE: N-gons are only supported in R9+.  This plugin requires R9.102 or later (the R9.102 update is available as a free
update from R9.0 at Maxon's website).

** NOTE: The .obj file format does not support N-gons with 'holes' in them (like a window cut out of a wall panel),
so if you end up with strangly formed or overlapping polygons, go back to your original document and look for and fix
any holes before exporting (this plugin does not fix these for you like the built-in exporter does).

o Export Normals (only available in the v8.5 and later plugins)
  IF your model has C4D Normal Tags, enabling this option will save those Normals to the output .obj file.  If no Normal Tags
  are found, no Normals are saved.

o Export Faces
  You can choose to export the polygon faces or not (morph files don't need faces, just vertices, for example).  Also enables
  the additional Face Sorting options...

    o C4D Ordering
    Writes out the facet (polygon) records in the order encountered in the C4D in-memory image.
    
    o Sort By Material
    Sorts facets (within each mesh) based on the material groups.
    
    o Sort By Group
    Sorts facets (within each mesh) based on the Group Tag selections.

    o Sort By Region
    Sorts facets (within each mesh) based on the Region Tag selections.
    
...just as background, it doesn't adversely affect anything to change the 'order' facets are listed in the .obj file (unlike
vertex ordering, which can redefine things to the extent that may break things like morph files).  There are a couple of
reasons that you might want to sort them differently, and most of them have to do with aesthetics (.obj files are
human-readable ASCII text files) or file-size, but may also be relevant for application implementers who prefer a particular
ordering.

When you start adding group and material information to a .obj file, anytime a facet (polygon) belongs to a different group,
material or region, you have to write out a new record before the facet record.  So you can imagine that if you have a humanoid
model with 50+ groups and a dozen or so materials, if you just start writing out facets based on the order they may have been
created in C4D, you might constantly be writing out a new group or material record every few lines as the list meanders around
through the mesh.  Generally, you can produce a smaller (and more human-readable) file by sorting them by Group (if there's
more groups than materials) or by Material (if there's more materials than groups).  Just as an aside, you can still sort by
Group, Material or Region, even if you're not exporting that particular record type (though it may or may not ultimately be
non-meaningful to do so ;).

o Reverse Faces
  This reverses the winding order of the polygons (in effect, changing the direction that the 'Normals' point), which changes
  the direction that the polygons face.  Since C4D itself uses the opposite face direction for determining backface culling,
  you should pretty much always leave this option selected.

o Export UV Coords
  UV (sometimes called UVW) Coordinates are basically the texture coordinates... you can choose to export these or not.

o Flip UV Horizontally/Vertically
  If your textures show up upside-down or flipped left->right in whatever external application you use, you can use these
  options to flip them around.

o Export Materials
  Enable/Disable saving material groups.  Note that these groups are saved based on the materials/selections you have set up
  in C4D.  To get the expected results, you really should use the 'Restrict to Selection' feature of the material dialog and
  re-read the text above about overlapping selections if you run into problems.    As implemented, a "default" material record
  will be written to hold any polygons that don't belong to any other material group.

o Export Groups
  This option determines whether any group records are written to the exported file and also enables the additional group
  options on the dialog...

   o Mesh Names
   determines whether the mesh names are written to the file (default C4D behavior is to write out the mesh names as groups).
   
       o As groups
       mimic C4D .obj export functionality
       
       o As UVMapper Regions
       write the mesh names out as UVMapper Regions instead of Groups (without using any Region tags, you can still create
       'region wrappers' around the separate meshes being saved).

   o Group Tag Names
   determines whether the list of selections in the Group Tag(s) are saved as group records.  As implemented, a "default"
   group record will be written to hold any polygons that don't belong to any other group.
   
   o Preserve Hierarchy
   using the example given earlier, would produce "Hyper_NURBS:Symmetry:Eye_Base:Left_Eye" when enabled or just "Left_Eye"
   as a group name if disabled.

o Export Regions
  determines whether the list of selections in the Region Tag(s) are saved in the output file.  As implemented, a "default"
  region record will be written to hold any polygons that don't belong to any other region.


.obj Import Plugin
=============================

The other sub-menu of the new "Plugins->Riptide" menu is ".Obj Importer".  This feature will allow you to import either a
Wavefront format ".obj" mesh file or a Wavefront format ".mtl" material file (importing a .obj file can also import the
specified .mtl file... see below for details).

If a .mtl file is selected, that file is read any existing materials in the active document that are named the same are
updated with the new information.  New materials are created for any uniquely named materials found in the file.  If a .obj
file is selected, an Import Options dialog will open, with the following options...

o Scale Factor:
  This is used for scaling the input mesh and should normally be set to the same value as the C4D .obj import/export value.

o Import Ngons (only available in the v9.102 plugin)
  IF your N-gons (polygons with more than 4 sides) exist in the .obj file, they will be impoorted as such into C4D.

* NOTE: N-gons are only supported in R9+.  This plugin requires R9.102 or later (the R9.102 update is available as a free
update from R9.0 at Maxon's website).

** NOTE: The .obj file format does not support N-gons with 'holes' in them (like a window cut out of a wall panel),
so if you end up with strangly formed or overlapping polygons, go back to your original document and look for and fix
any holes before exporting (this plugin does not fix these for you like the built-in exporter does).

o Import Normals (only available in the v8.5 plugin)
  If Normals exist in the .obj file, C4D Normal Tags will be created using that information. If no Normals exist in the file,
  no Normal Tags are created.

o Import Groups
  - Selection tags are created for any Groups within the mesh and a 'Group Tag' is created and set up to track them.
  - If disabled, no Group Selections or Group Tags will be created (note that even if this option is disabled, you can still
    "Split by Group" and get separate meshes, who's names are the group names).

o Import Regions
  - Selection tags are created for any UVMapper regions found and a 'Region Tag' is created and set up to track them.
  - If disabled, no UVMapper Region Selections or Region Tags will be created (note that even if this option is disabled,
    you can still "Split by Region" and get separate meshes, who's names are the region names).

o Import Materials
  - If the .obj file lists a mtllib and it can be found and read, Materials are created (or updated) using that information,
    otherwise they are created using some default settings (see information below about some re-mapping that takes place).
  - Selection tags are created for any Material groupings and the selections use the material names (no more "Selection 1",
    "Selection 2" ... "Selection 34", etc. (yay!)).
  - Texture Tags are created for every material grouping.
  - If disabled, no Material Selections, Texture Tags or Materials will be created (note that even if this option is disabled,
    you can still "Split by Material" and get separate meshes, who's names are the material names).

o Import UV Coords
  - If the mesh has UV (texture) coordinates, a UVW Coordinates tag(s) is created and added.
  - If disabled, no UV Coordinate Tags will be created.

o Flip UV Horizontally/Vertically
  These can be used to flip textures left->right or top->bottom.

o Reverse Faces
  This option can be used to reverse the facets of the imported mesh.

o Don't Split
  The mesh is set up as one big Polygon Object (editable mesh).

o Split by Group
  The mesh being loaded is split up into one Polygon Object per group record found in the file (ala C4D's importer).

o Split by Region
  The mesh being loaded is split up into one Polygon Object per UVMapper Region record found in the file.

o Split by Material
  The mesh being loaded is split up into one Polygon Object per Material selection found in the file.

o Create New Document
  When selected, the mesh being loaded is loaded into a fresh/new document.

o Merge Into Current Document
  When selected, the mesh being loaded is merged into the current/active document.



Wavefront .mtl file notes:
==========================================================

Note that besides being largely undocumented (I spent a week scouring the net to get what information I have on it),
a Wavefront .mtl file supports (at best) a small subset of the settings you have available within C4D and as such, there
is no 1-to-1 mapping of material properties (bump maps are supported, but there's no way to specify bumpmap strength,
for example).

With that in mind, I had to make some decisions about how to best map C4D's idea of material properties into something
that makes sense in a .mtl file.  As another example, the .mtl file supports a 'Diffuse' color and texture map, but
these are a closer match to C4D's 'Color' channel than the 'Diffuse' channel, so I translate them between the two.

Other design-decisions/implementation details:

o 'Ambient' settings are mapped to the 'Luminance' property/channel
o Specular Color (and any related texture) are set up, but Specular Scale is not.
o Texture sampling is set to "Alias1" (instead of MIP)
o Blend Mode is set to "Multiply" (instead of Normal)
o C4D has a 'brightness' value for various channel colors, but there's not a separate parameter for that in the .mtl file,
  so the RGB values are scaled by it.  In other words, if you had a channel set to White (RGB all = 100%) with a Brightness
  of 50%, you'd get a mid-Grey color.  If you export that mesh, then re-import it and go check that material/channel, you'll
  find that now the RGB values are all set to 50% and the Brightness is set to 100% - which is opposite - but the resulting
  mid-Grey color is the same ;).

...On a related note, some applications (Poser, for example) don't always save out all of the values you are expecting (like
transparency/alpha maps), so you will likely need to still manually load or adjust some settings for best results. In the end,
it's still a step up from C4D's built-in .obj import, which ignores the .mtl file all together

Also note that for the textures to be loaded correctly, you'll need to set up your "Texture Paths" within C4D for it to find
them ("Edit->General Settings" menu in C4D v7.303).



Limitations:
==========================================================

I guess the biggest issue of note here is speed... a lot of the pre-processing done internally to allow all of this amount
of flexibility is very brute-force/intensive/repetitive - much of it requiring recursive walks through every polygon in the
list multiple times.  I've tried to optimize the code wherever possible to account for this, but it may still take a few
seconds longer than C4D's built-in .obj import/export feature does to input/output the same file.

One additional word of caution... various features of the various plugins make attempts to enforce unique group/region/material
naming, but not all do.  So to get the best (expected) results, you should try to make sure each of your selections (for
example) have unique names before exporting.  It's also best to make sure that everything is accounted for... polygons that
don't belong to any particular group/region/material will get consolidated into some 'default' group/region/material... this
might create unexpected results.  So... "If in doubt, spell it out".

And on that happy note...



Acknowledgements:
==========================================================

I'd like to give a special thanks to the following people who helped make this happen:

o Testing and Feedback
  'ramhernan'
  'Viomar'
  'Specs2'
  'Beanzvision'
  'Chris'
  'umblefugly'
  'Irish'
  'jelisa'
  'Damsel'

o French string (and documentation) translations
  'Viomar'

o German string translations  
  'Specs2'

o Sample imagery used in Riptide Logo
  'Beanzvision'

o Developer Support
  Maxon Computers


Final Comments:
==========================================================

Thanks again for your patronage.  I am always interested in comments and product feedback. I am always happy to try to
help with questions whenever possible, but please do me the courtesy of reading through the documentation above first.

If you like this product, please visit my store for your future shopping needs:

Spanki - http://market.renderosity.com/softgood.ez?Who=Spanki

If you'd like to keep up to date on the latest products, freebies and updates, please stop by the forums at Spanki's
Prop Shop ( http://www.skinprops.com ).


Enjoy,

Keith Young a.k.a. Spanki
http://www.skinprops.com
