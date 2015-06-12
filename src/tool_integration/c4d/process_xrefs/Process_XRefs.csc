var relative,the_folder,adjust,add_xref;

do_stuff(obj,doc)
{
	var reference_path,reference_file,relative_file;
	var new_path,prefix,the_name;

	if(!obj) return;	// if there is no object, return

	if(obj->GetType()!=200000118) return;	// if the object is not an XRef object, return

	prefix="";
	if(add_xref==TRUE) prefix="xref_";	// if the Add xref prefix option is on, set the prefix

	reference_path=obj#SCENEINSTANCE_FILENAME;
	if(reference_path!=nil) // if teh XRef object is not referencing anything, return
		{
		if(GeFileExist(reference_path,FALSE)==TRUE) // if the file exists
			{
			reference_file=stradd(prefix,reference_path->GetLastString());	// get the name of the referenced file and, optionally, add it the new prefix
			new_path=the_folder;
			new_path->AddLast(reference_file);	// set the new path for the referenced file

			if(relative==FALSE)	// if the file will not be saved in the document folder...
				{
				obj#SCENEINSTANCE_FILENAME=new_path;	// set the path
				}
			else
				{
				relative_file=new(Filename);	// create a new empty filename
				while(relative_file->IsEmpty()==FALSE) relative_file->RemoveLast();	// make sure it is really empty
				relative_file->AddLast(reference_file);	// it will only contain the name of the file
				obj#SCENEINSTANCE_FILENAME=relative_file;	// set the path
				}

			GeFileCopy(reference_path,new_path,TRUE);	// copy the file from its old location to the new location and with an optional new name
			new_path->RemoveLast();	// clear the file from the path
			if(adjust==TRUE)
				{
				obj->SetName(reference_file);	// if the names should be adjusted, set the new name
				obj->Message(MSG_UPDATE);
				}
			}
		}
}


check_document(obj,doc)	// go through the whole document, recursively.
{
	while(obj)
		{
		do_stuff(obj,doc);	// for each object of the scene, check it.
		check_document(obj->GetDown(),doc);
		obj=obj->GetNext();
		}
		return NULL;
}

class my_dialog:GeModalDialog	// create the initial dialog
{
	private:
		var doc;

	public:
		my_dialog();
		CreateLayout();
		Command(id, msg);
}

my_dialog::my_dialog()
{
	super();
}

my_dialog::CreateLayout()
{
	doc=GetActiveDocument();
	the_folder=doc->GetFilename();
	the_folder->RemoveLast();	// the default path is the path of the active document
	adjust=TRUE;	// the default is to adjust the names of the XRef objects
	add_xref=FALSE;	// the default is to NOT add any prefix to the copied files
	relative=TRUE;	// by default the paths are saved as relative
	SetTitle("Move XReferenced files to folder");
	AddGroupBeginV(200000, BFH_FIT, 3, "Folder", 0);
	{
		AddGroupBorder(BORDER_GROUP_IN);
		AddGroupBorderSpace(4, 4, 4, 4);
		AddGroupSpace(4, 4);
		AddStaticText(200001,BFH_LEFT,50,14,"Folder:",0);
		AddEditText(200002,BFH_SCALE,640,14);
		AddButton(200003,BFH_FIT,32,14,"...");
	}
	AddGroupEnd();
	AddCheckbox(200004,BFH_LEFT,0,0,"Adjust names");
	AddCheckbox(200005,BFH_LEFT,0,0,"Add xref to filename");
AddDlgGroup(3);
SetItem(200004,adjust);
SetItem(200005,add_xref);
SetString(200002,the_folder->GetFullString());
}

my_dialog::Command(id, msg)
{
var result,doc_path;

doc=GetActiveDocument();	// get the current document path
doc_path=doc->GetFilename();
doc_path->RemoveLast();

result=GetString(200002);
if(sizeof(result)>0)	// if the path field not is empty...
	{
	the_folder=new(Filename);
	the_folder->SetFullString(result);	// get the path
	relative=strcmp(result,doc_path->GetFullString())==0?TRUE:FALSE;
	}
else
	{
	doc=GetActiveDocument();	// otherwise, set it to the path of the active document
	the_folder=doc->GetFilename();
	the_folder->RemoveLast();
	relative=TRUE;	// the paths are relative
	}

switch(id)
	{
		case 200003:
			result=the_folder->PathSelect("Select the folder");	// allow the user to define a path to save the Xreferenced files
			relative=FALSE;	// the paths must be absolute
			if(result==FALSE)	// if the user hit Cancel...
				{
				doc=GetActiveDocument();	// set it to the path of the active document
				the_folder=doc->GetFilename();
				the_folder->RemoveLast();
				relative=TRUE;	// the paths are relative
				}
			SetString(200002,the_folder->GetFullString());
			break;
			
		case 200004:
			adjust=GetItem(200004);	// get the state of the "Adjust names" option
			break;

		case 200005:
			add_xref=GetItem(200005);	// get the state of the "Add Prefix" option
			break;

		case 200006:
			Close();
			return -1;
			break;

		case 200007:
			Close();
			return 1;
			break;
		
		default:
			break;
	}
}

//**************************

main(doc,op)
{
var obj,option;

var dialog = new(my_dialog);
dialog->Open(-1,-1);
option=dialog->GetResult();
if(option==0) return;

if(the_folder==nil)	// if no folder was defined...
	{
	the_folder=doc->GetFilename();	// set it to the path of the active document
	the_folder->RemoveLast();
	relative=TRUE;	// the paths are relative
	}


if(GeFileExist(the_folder,TRUE)==FALSE)	// if the folder does not exist
	{
	TextDialog("The folder you entered does not exist.");	// tell it to the user and leave
	return;
	}

obj=doc->GetFirstObject();	// get the first object of the scene

check_document(obj,doc);	// and go through all the document...
}