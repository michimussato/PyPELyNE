# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------
 Source Python HELP
--------------------------------------------------------------------------------
This module has the objective to assist the development process between your 
favorite IDE and Maya. The reload of your Python script is now on a button.

Simply choose the working script, from the right list tree, choose the 
fonctions, the class to instanciate and there methods to run and just press the
button Run : <your script path>


Requirement : Pymel


Usage
    import source_python
    test = source_python.SourcePython()
    
    see the installation to put the menu in the main Maya window/General Editors
    and the auto-start.


Installation:
    In your usersetup.mel (not userSetup.py)
    (if you don't have one yet, create one on your mel folder) 
    put the lines below:
    
// put this line if you don't have it, it force the build of Maya menus
buildDeferredMenus();
// this add the menu Source Python below the Script Editor
python("import source_python;source_python.add_menu()");
// this load the interface on Maya start
evalDeferred "python(\"import source_python;test = source_python.SourcePython()\")";


Description:
    The Source Python and Script Editor windows (or dock) is divided in two zone.
    On bottom side: the standard Script Editor.
    
    On the up side: the new Source Python zone.
        This is divided in 2 panes:
            Right :
                the list of all the functions, classes and methodes of the loaded module
                
                Filter / Sort / Doc
                    Filter : enter the string you're looking for and define the test:
                    in, startswith or endswith
                    Sort Alphabetical : enable the sorting or keep the original order
                    Show doc : on each selection, the corresponding doc is printed
            
            Left :
                the text zone to define the execution request
    
    On top of all, the Run button to execute after reloading the script


Menus
    File:
        Open    : open a python script to work on it
        Refresh : read again the file to update the list of python object
        Recents : the list of last opened python scripts
                  (the length is settable on the options)
    Options:
        Insert ScriptEditor : to force the insertion of the scriptEditor
        Run Reset History   : the scriptEditor history is cleaned on each run
        In dock : to dock the window (by default on right side)
        
        Recents:
            Set length : define the max recent list length
            Reset      : clear the history
        
        Settings:
            Save  : Store the settings of the ui
            Reset : Restore the defaults ui settings
    
    Help : This help


Limitations:
    The scripts using some relatives informations using, for exemple __file__ or
    have some particular python object like singleton should not work.
    This because of the used method: execfile, where a new temporary file is used.
    
    This script use the utf-8 encoding.


Thanks to Mako developers to implement the string conversion of the ast objects 
arguments.

--------------------------------------------------------------------------------
 Author : Nicolas Pastrana
 Site   : http://n.pastrana.free.fr
 Mail   : n.pastrana@free.fr
 Version: 1.0.0
--------------------------------------------------------------------------------
"""

import os, sys
import codecs
import traceback
import compiler
from collections import namedtuple
from tempfile import gettempdir
from functools import partial

import pymel.core as pmc


class SimplePyParser(object):
    """ This object parse, store and sort by name the python file object's. """
    
    Def = namedtuple("def_", "name, argnames, defaults, doc, str_, repr_", verbose=False)
    Class = namedtuple("class_", "name, doc, methodes, str_, repr_", verbose=False)
    
    def __init__(self):
        self.objs = []
        self.order_obj = []

    def parse(self, path):
        self.__init__()
        try:
            mod = compiler.parseFile(path)
            
            for node in mod.node.nodes:
                if isinstance(node, compiler.ast.Function):
                    self.objs.append(self.Def(node.name,
                                              node.argnames,
                                              node.defaults,
                                              node.doc,
                                              self.__def_repr(node)[4:],
                                              self.__def_repr(node))
                                     )
                
                elif isinstance(node, compiler.ast.Class):
                    str_ = ""
                    repr_ = ""
                    children = node.getChildNodes()
                    for child in children:
                        if repr_:
                            break
                        if isinstance(child, compiler.ast.Stmt):
                            for c in child:
                                if isinstance(c, compiler.ast.Function) and c.name == "__init__":
                                    args = self.__arg_string(c)
                                    str_ = "test_%s = %s(%s)" % (node.name.lower(), node.name, args)
                                    repr_ = "class %s(%s)" % (node.name, args)
                                    break
                            else:
                                str_ = "test_%s = %s()" % (node.name.lower(), node.name)
                                repr_ = "class %s()" % node.name
                    
                    current = self.Class(node.name,
                                         node.doc, [],
                                         str_, repr_)
                    
                    self.objs.append(current)
                    for child in children:
                        if isinstance(child, compiler.ast.Stmt):
                            for c in child:
                                if isinstance(c, compiler.ast.Function):
                                    if not c.name.startswith("__"):
                                        args = self.__def_repr(c)
                                        current.methodes.append(self.Def(c.name,
                                                                         c.argnames,
                                                                         c.defaults,
                                                                         c.doc,
                                                                         "test_%s.%s(%s)" % (node.name.lower(), c.name, self.__arg_string(c)),
                                                                         "    " + self.__def_repr(c))
                                                                )
        except Exception, error:
            pmc.error(error)
    
    def __filter(self, obj_name, filter_str="", filter_test="in"):
        a = False
        if filter_str:
            if filter_test == "in":
                if filter_str not in obj_name.lower():
                    a = True
            elif filter_test == "startswith":
                if not obj_name.lower().startswith(filter_str):
                    a = True
            elif filter_test == "endswith":
                if not obj_name.lower().endswith(filter_str):
                    a = True
        return a
    
    def sort_objects(self, alphabetical=False, filter_str="", filter_test="in"):
        self.order_obj = []
        if self.objs:
            main_order = self.objs[:]
            if alphabetical:
                main_order.sort()
            
            for node in main_order:
                if isinstance(node, self.Class):
                    if not filter_str:
                        second_order = node.methodes[:]
                    else:
                        second_order = []
                        for m in node.methodes:
                            if self.__filter(m.name, filter_str, filter_test):
                                continue
                            
                            second_order.append(m)
                    
                    if second_order:
                        if alphabetical:
                            second_order.sort()
                        
                        self.order_obj.append(node)
                        self.order_obj.extend(second_order)
                else:
                    if self.__filter(node.name, filter_str, filter_test):
                        continue
                    
                    self.order_obj.append(node)

    def __arg_string(self, obj, keep_self=False):
        args = ""
        if obj.argnames and obj.defaults:
            start = len(obj.argnames) - len(obj.defaults)
            for i, argname in enumerate(obj.argnames):
                if i < start:
                    args += argname + ", "
                else:
                    t = ExpressionGenerator(obj.defaults[i - start])
                    v = t.value()
                    if v is not None:
                        args += "%s=%s, " % (argname, v)
                    
        elif obj.argnames and not obj.defaults:
            tmp = obj.argnames[:]
            args += ", ".join(tmp)
        
        if not keep_self:
            if args.startswith("self, "):
                args = args.replace("self, ", "", 1)
            elif args == "self":
                args = ""
        if args.endswith(", "):
            args = args[:-2]
        return args

    def __def_repr(self, obj):
        return "def %s(%s)" % (obj.name, self.__arg_string(obj, keep_self=True))


class SourcePython(object):
    """ This is the main script """
    
    spacetab = "    "
    ui_name = "Source Python and Script Editor"
    dock_name = "SourcePythonAndScriptEditor"
    exec_path = r"%s\source_py_execfile.py" % gettempdir()
    
    maya_version = pmc.mel.eval("getApplicationVersionAsFloat")
    script_panel = "scriptEditorPanel1"
    options = {
               "recents" : [u""], "cmds" : [u""],
               "sizes" : [
                          800, 600, # window size
                          50, 20, 50, 20, 100, 80, # source py pane sizes
                          100, 75, 100, 25 # script editor pane sizes
                          ],
               "dock": [0, 0, 2], # enable, floating, area
               "reset" : True, "order" : False, "show_doc" : False,
               "max_recents" : 10,
               "filter_test" : "in", # in, startswith, endswith
               }
    dock_areas = {1 : "left", 2 : "right", 3 : "top", 4 : "bottom"}
    old_options = ["sourcePytonRecents", "sourcePytonResetHis", "sourcePytonMainCmd",
                   "sourcePytonWindow", "sourcePytonDock"]
    to_delete = "commandReportercmdScrollFieldReporter"
    line = "-" * 79 + "\n"
    
    spp_ = SimplePyParser()
    
    def __init__(self):
        self.dock_ui = None
        self.init_instance()
        self.init_options()
        
        self.build_ui()
        self.read_py()

    def init_instance(self):
        self.py_path = ""
        self.old_path = ""
    
    #===========================================================================
    # Options
    #===========================================================================
    def get_option_name(self, name):
        return "%s%s" % (self.__class__.__name__, name.title())

    def init_options(self, force=False):
        for opt in self.options:
            opt_name = self.get_option_name(opt)
            if not pmc.optionVar.has_key(opt_name) or force:
                if force and opt in ["recents", "cmds"]:
                    continue
                pmc.optionVar[opt_name] = self.__class__.options[opt]
        
        for opt in self.old_options:
            if pmc.optionVar.has_key(opt):
                del pmc.optionVar[opt]
        
        self.get_options()

    def get_options(self):
        for opt in self.options:
            opt_value = pmc.optionVar.get(self.get_option_name(opt))
            if opt in ["recents", "cmds"]:
                if isinstance(opt_value, basestring):
                    opt_value = [opt_value]
            if opt in ["recents", "cmds", "dock"]:
                if not isinstance(opt_value, list):
                    opt_value = list(opt_value)
            elif opt in ["reset", "order", "show_doc"]:
                opt_value = bool(opt_value)
            
            setattr(self, opt, opt_value)
        
        self.update_pys()

    def set_options(self, *arg):
        for opt in self.options:
            if opt == "sizes":
                value = []
                if self.dock_ui:
                    value.append(pmc.dockControl(self.dock_ui, q=True, w=True))
                    value.append(pmc.dockControl(self.dock_ui, q=True, h=True))
                else:
                    value.append(pmc.window(self.win, q=True, w=True))
                    value.append(pmc.window(self.win, q=True, h=True))
                
                value.extend(pmc.paneLayout(self.main_layout, q=True, paneSize=True))
                value.extend(pmc.paneLayout(self.script_layout, q=True, paneSize=True))
            
            elif opt == "dock":
                if self.dock_ui:
                    value = [self.dock[0]]
                    value.append(int(pmc.dockControl(self.dock_ui, q=True, floating=True)))
                    tmp = pmc.dockControl(self.dock_ui, q=True, area=True)
                    for obj_id, a in self.dock_areas.iteritems():
                        if a == tmp:
                            break
                    else:
                        obj_id = self.dock[2]
                    value.append(obj_id)
                else:
                    value = getattr(self, opt)
            else:
                value = getattr(self, opt)
            
            opt_name = self.get_option_name(opt)
            pmc.optionVar[opt_name] = value
        
        self.update_pys()

    def save_options(self, *args):
        self.set_options()
        
        to_del = []
        for opt in pmc.optionVar.keys():
            if self.to_delete in opt and "Suppress" in opt:
                to_del.append(opt)
        for opt in to_del:
            del pmc.optionVar[opt]
        
        pmc.runtime.SavePreferences(g=True)

    def reset_options_ui(self, *args):
        self.init_options(force=True)
        self.ui()
        self.update_size_ui()
        self.update_ui()
    
    #===========================================================================
    # Current Python and commands
    #===========================================================================
    def update_pys(self):
        if self.recents:
            self.py_path = self.recents[0]
        else:
            self.py_path = u""
        
        if self.cmds:
            self.py_cmd = self.cmds[0]
        else:
            self.py_cmd = u""

    def select_py_ui(self, *args):
        mask = "*.py"
        if self.py_path:
            mask = os.path.join(os.path.dirname(self.py_path), mask)
        else:
            mask = os.path.join(sys.path[-1], mask)
        
        temp = pmc.fileDialog(directoryMask=mask)
        if temp:
            self.set_py(temp, force=True)

    def set_py(self, path, force=True, *args):
        self.old_path = self.py_path
        self.py_path = unicode(path)
        
        self.update_recents()
        self.update_recents_menu()
        self.read_py()
        self.set_options()

    def read_py(self, *arg):
        if self.py_path and os.path.isfile(self.py_path):
            self.spp_.parse(self.py_path)
            self.update_ui()
        else:
            pmc.textScrollList(self.infos_ui, e=True, ra=True)
            pmc.textScrollList(self.infos_ui, e=True, a="//error: select a python file or no more exist...")

    #===========================================================================
    # Recents
    #===========================================================================
    def update_recents(self):
        if self.recents and self.py_path:
            if self.recents == [u""] and self.cmds == [u""]:
                self.recents = [self.py_path]
                self.cmds = [self.py_cmd]
                self.update_pys()
                return
            
            for i, recent in enumerate(self.recents):
                if self.py_path == recent:
                    current = i
                    break
            else:
                if len(self.recents) > self.max_recents:
                    self.recents = self.recents[:self.max_recents]
                    self.cmds = self.cmds[:self.max_recents]
                
                self.recents.insert(0, self.py_path)
                self.cmds.insert(0, u"")
                self.update_pys()
                return
            
            self.recents.insert(0, self.recents.pop(current))
            if len(self.cmds) > current:
                self.cmds.insert(0, self.cmds.pop(current))
            else:
                self.cmds.insert(0, u"")
            self.update_pys()

    def update_recents_menu(self):
        pmc.menu(self.recents_menu_ui, e=True, deleteAllItems=True)
        if self.recents:
            for r in self.recents[1:]:
                pmc.menuItem(parent=self.recents_menu_ui, label=r, c=partial(self.set_py, r))

    def reset_recents_ui(self, *args):
        self.init_instance()
        self.recents = self.__class__.options["recents"]
        self.cmds = self.__class__.options["recents"]
        
        self.set_py("")

    def set_recents_ui(self, *args):
        tmp = pmc.promptBox("Recents max length", "Enter the max value", "Ok", "Cancel")
        if tmp:
            try:
                self.max_recents = int(tmp)
                self.update_recents()
                self.update_recents_menu()
                pmc.menuItem(self.max_recents_ui, e=True, label="Set length (%s)" % self.max_recents)
                self.save_options()
            except:
                pmc.warning("Please enter a integer value, i.e.: 5")

    #===========================================================================
    # UI methodes
    #===========================================================================
    def order_by_ui(self, *args):
        self.order = pmc.checkBoxGrp(self.order_ui, q=True, v1=True)
        
        self.spp_.sort_objects(alphabetical=self.order,
                               filter_str=pmc.textFieldGrp(self.filter_ui, q=True, text=True),
                               filter_test=self.filter_test)
        
        pmc.textScrollList(self.infos_ui, e=True, ra=True)
        pmc.textScrollList(self.infos_ui, e=True, a=[o.repr_ for o in self.spp_.order_obj])

    def update_size_ui(self):
        if self.dock_ui and self.dock[0]:
            kwargs = self.__dock_kwargs()
            kwargs["e"] = True
            pmc.dockControl(self.dock_ui, **kwargs)
        else:
            self.win.setWidthHeight(self.sizes[:2])
        
        paneSizes = []
        tmp = self.sizes[2:8]
        j = 1
        for i in range(0, len(tmp) - 1, 2):
            paneSizes.append([j, tmp[i], tmp[i + 1]])
            j += 1
        pmc.paneLayout(self.main_layout, e=True, paneSize=paneSizes)
        
        pmc.paneLayout(self.script_layout, e=True,
                       paneSize=[
                                 [1, self.sizes[8], self.sizes[10]],
                                 [2, self.sizes[9], self.sizes[11]],
                                 ]
                       )
        
        pmc.checkBoxGrp(self.order_ui, e=True, v1=self.order)
        pmc.checkBoxGrp(self.order_ui, e=True, v2=self.show_doc)
        
        pmc.optionMenuGrp(self.filter_test_ui, e=True, v=self.filter_test)
    
    def update_ui(self):
        self.clear_script_reporter()
        
        pmc.scrollField(self.cmd_ui, e=True, clear=True)
        self.user_cmd = self.py_cmd
        if self.py_path:
            pmc.button(self.run_but, e=True, l="Run : %s" % self.py_path)
            self.order_by_ui()
        else:
            pmc.button(self.run_but, e=True, l="please select")

    #===========================================================================
    # Command relative methods
    #===========================================================================
    @property
    def user_cmd(self):
        return unicode(pmc.scrollField(self.cmd_ui, q=True, text=1))
    
    @user_cmd.setter
    def user_cmd(self, text):
        pmc.scrollField(self.cmd_ui, e=True, text=text)
    
    def insert_cmd_ui(self, *arg):
        si = pmc.textScrollList(self.infos_ui, q=True, sii=1)
        if si:
            tmp = self.spp_.order_obj[si[0] - 1].str_ + "\n"
            if tmp != "\n":
                pmc.scrollField(self.cmd_ui, e=True, it=tmp)
                self.cmds[0] = self.user_cmd
                self.set_options()

    def doc_cmd_ui(self, *arg):
        if self.show_doc:
            si = pmc.textScrollList(self.infos_ui, q=True, sii=1)
            if si:
                obj = self.spp_.order_obj[si[0] - 1]
                if obj.doc is not None:
                    print "%sDoc of : %s\n%s%s\n%s\n" % (self.line, obj.name, self.line, obj.doc, self.line)
    
    def run_cmd_ui(self, *arg):
        if self.py_path:
            self.clear_script_reporter()
            self.cmds[0] = self.user_cmd
            
            cmd = ""
            with codecs.open(self.py_path, encoding="utf-8", mode="r") as f:
                cmd = f.read()
            
            if cmd:
                cmd += u"\n" + self.user_cmd
                with codecs.open(self.exec_path, encoding="utf-8", mode="w") as f:
                    f.write(cmd)
                
                try:
                    execfile(self.exec_path, globals())
                except Exception, error:
                    traceback.print_exc(file=sys.stdout)
                    if "encoding declaration in Unicode string" == error.args[0]:
                        try:
                            exec(cmd.encode("cp850"))
                        except Exception, error:
                            pmc.error(error)
                            traceback.print_exc(file=sys.stdout)
                    else:
                        pmc.error(error)
            
            self.set_options()
        else:
            self.select_py_ui()

    #===========================================================================
    # SLOTS
    #===========================================================================
    def help_ui(self, *args):
        print __doc__
    
    def set_show_doc_ui(self, *args):
        # don't use args because of 2011 qt compatibility
        self.show_doc = pmc.checkBoxGrp(self.order_ui, q=True, v2=True)
        self.save_options()

    def set_reset_his_ui(self, *args):
        self.reset = not self.reset
        self.save_options()
        self.update_ui()

    def set_filter_test_ui(self, *args):
        self.filter_test = pmc.optionMenuGrp(self.filter_test_ui, q=True, v=True)
        self.save_options()
        self.update_ui()

    def set_in_dock_ui(self, *args):
        self.dock[0] = int(not bool(self.dock[0]))
        self.save_options()
        self.build_ui()
    
    #===========================================================================
    # Script Editor methods
    #===========================================================================
    @property
    def script_layout(self):
        return pmc.melGlobals["$gCommandLayout"]
    
    def insert_script_editor_ui(self, *args):
        if pmc.window(self.script_panel + "Window", exists=True):
            pmc.deleteUI(self.script_panel + "Window", window=True)
        
        pmc.scriptedPanel(self.script_panel, e=True, unParent=True)
        pmc.scriptedPanel(self.script_panel, e=True, parent=self.form_scriptEditor)
        marge = 1
        pmc.formLayout(self.form_scriptEditor, edit=True,
                       attachForm=[
                                   (self.script_panel, "top", marge),
                                   (self.script_panel, "left", marge),
                                   (self.script_panel, "right", marge),
                                   (self.script_panel, "bottom", marge),
                                   ],
                       )
        
    
    def clear_script_reporter(self):
        if self.reset:
            pmc.cmdScrollFieldReporter(pmc.melGlobals["gCommandReporter"], e=True, clr=True)

    #===========================================================================
    # Main UI
    #===========================================================================
    def ui(self):
        marge = 2
        self.win = None
        if pmc.window(self.__class__.__name__, q=True, exists=True):
            pmc.deleteUI(self.__class__.__name__)
        
        with pmc.window(self.__class__.__name__, title=self.ui_name, menuBar=True) as self.win:
            #===================================================================
            # Menus
            #===================================================================
            pmc.menu(label="File", tearOff=False)
            pmc.menuItem(label="Open", c=self.select_py_ui)
            pmc.menuItem(label="Refresh", c=self.read_py)
            
            self.recents_menu_ui = pmc.menuItem(subMenu=True, label="Recents")
            pmc.setParent("..", menu=True)
            
            pmc.setParent("..", menu=True)
            
            pmc.menu(label="Options", tearOff=False)
            pmc.menuItem(label="Insert ScriptEditor", c=self.insert_script_editor_ui)
            self.reset_menu_ui = pmc.menuItem(label="Run Reset History",
                                              checkBox=self.reset,
                                              c=self.set_reset_his_ui)
            if self.maya_version >= 2011:
                self.dock_ui_item = pmc.menuItem(label="In Dock",
                                                 checkBox=self.dock[0],
                                                 c=self.set_in_dock_ui)
            pmc.menuItem(divider=True)
            pmc.menuItem(subMenu=True, label="Recents")
            self.max_recents_ui = pmc.menuItem(l="Set length (%s)" % self.max_recents, c=self.set_recents_ui)
            pmc.menuItem(l="Reset", c=self.reset_recents_ui)
            pmc.setParent("..", menu=True)
            
            pmc.menuItem(subMenu=True, label="Settings")
            pmc.menuItem(l="Reset", c=self.reset_options_ui)
            pmc.menuItem(l="Save", c=self.save_options)
            pmc.setParent("..", menu=True)
            
            pmc.menu(label='Help', helpMenu=True)
            pmc.menuItem(label='About', c=self.help_ui)
            
            #===================================================================
            # Layout and Contents
            #===================================================================
            main_form = pmc.formLayout(nd=100)
            self.run_but = pmc.button(l="Run", c=self.run_cmd_ui)
            
            self.main_layout = pmc.paneLayout(configuration="top3")
            
            form = pmc.formLayout(nd=100)
            self.cmd_ui = pmc.scrollField(ed=1, ww=0)
            pmc.setParent("..")
            
            form_infos = pmc.formLayout(nd=100)
            self.infos_ui = pmc.textScrollList(ams=0, fn="fixedWidthFont",
                                               sc=self.doc_cmd_ui,
                                               dcc=self.insert_cmd_ui)
            
            infos_layout = pmc.frameLayout(label="Filter / Sort / Doc", collapse=True, collapsable=True)
            pmc.columnLayout(adj=1)
            pmc.rowLayout(numberOfColumns=2, adj=1)
            self.filter_ui = pmc.textFieldGrp(label="Filter",
                                              text="",
                                              cw=[1, 40], adj=2,
                                              fcc=True,
                                              cc=self.order_by_ui)
            
            self.filter_test_ui = pmc.optionMenuGrp(cc=self.set_filter_test_ui)
            pmc.menuItem(label="in")
            pmc.menuItem(label="startswith")
            pmc.menuItem(label="endswith")
            
            pmc.setParent("..")
            
            self.order_ui = pmc.checkBoxGrp(numberOfCheckBoxes=2,
                                            label="Sort",
                                            label1="Alphabetical",
                                            label2="Show doc",
                                            cw=[1, 40],
                                            cc1=self.order_by_ui,
                                            cc2=self.set_show_doc_ui,
                                            )
            
            pmc.setParent("..")
            pmc.setParent("..")
            pmc.setParent("..")
            
            self.form_scriptEditor = pmc.formLayout(nd=100)
#            self.form_scriptEditor = pmc.paneLayout(configuration="single")
            pmc.setParent("..")
            
            pmc.setParent("..")
            
            #===================================================================
            # Layout settings
            #===================================================================
            pmc.formLayout(main_form, edit=True,
                             attachNone=[
                                         (self.run_but, "bottom")
                                         ],
                             attachForm=[
                                         (self.run_but, "top", marge),
                                         (self.run_but, "left", marge),
                                         (self.run_but, "right", marge),
                                         (self.main_layout, "top", marge),
                                         (self.main_layout, "left", marge),
                                         (self.main_layout, "right", marge),
                                         (self.main_layout, "bottom", marge),
                                         ],
                             attachControl=[
                                            (self.main_layout, "top", marge, self.run_but),
                                            ]
                            )
            pmc.formLayout(form, edit=True,
                             attachForm=[
                                         (self.cmd_ui, "top", marge),
                                         (self.cmd_ui, "left", marge),
                                         (self.cmd_ui, "right", marge),
                                         (self.cmd_ui, "bottom", marge),
                                         ],
                             )
            
            pmc.formLayout(form_infos, edit=True,
                             attachForm=[
                                         (self.infos_ui, "top", marge),
                                         (self.infos_ui, "left", marge),
                                         (self.infos_ui, "right", marge),
                                         (infos_layout, "left", marge),
                                         (infos_layout, "right", marge),
                                         (infos_layout, "bottom", marge),
                                         ],
                            attachControl=[
                                           (self.infos_ui, "bottom", marge, infos_layout)
                                           ]
                             )
        
        self.insert_script_editor_ui()
        
        self.dock_it()

    def show_window(self):
        pmc.showWindow(self.win)

    def build_ui(self):
        self.ui()
        self.update_ui()
        self.update_size_ui()
        self.update_recents_menu()

    #===========================================================================
    # DOCKS
    #===========================================================================
    def __dock_kwargs(self):
        kwargs = {
                  "floating" : self.dock[1],
                  "area" : self.dock_areas[self.dock[2]],
                  "w" : self.sizes[0],
                  "h" : self.sizes[1],
                  }
        return kwargs

    def dock_it(self):
        if self.maya_version >= 2011:
            if pmc.dockControl(self.dock_name, q=True, ex=True):
                pmc.deleteUI(self.dock_name)
            
            if self.dock[0]:
#                kw = self.__dock_kwargs()
                self.dock_ui = pmc.dockControl(self.dock_name, label=self.ui_name,
                                               content=self.win, r=True, **self.__dock_kwargs())
            else:
                self.dock_ui = None
                self.show_window()
        else:
            self.show_window()
        
        self.update_size_ui()


global NP_source_python_main
def NP_source_python_main(*arg):
    SourcePython()

def get_menus():
    return pmc.windows.menu(pmc.melGlobals["$gMainWindowMenu"], q=True, ia=True)

def add_menu():
    m1, m2 = None, None
    ok = False
    if not "$gMainWindowMenu" in pmc.melGlobals:
        reload(pmc)
    
    menus1 = get_menus()
    if not menus1:
        pmc.mel.eval("buildDeferredMenus();")
        menus1 = get_menus()
    
    for m1 in menus1:
        try:
            if pmc.windows.menu(m1, q=True, label=True) == "General Editors":
                menus2 = pmc.windows.menu(m1, q=True, ia=True)
                if not menus2:
                    pmc.mel.eval('buildObjectEdMenu("%s");' % m1)
                    menus2 = pmc.windows.menu(m1, q=True, ia=True)
                for m2 in menus2:
                    try:
                        if pmc.windows.menuItem(m2, q=True, label=True) == "Script Editor":
                            ok = True
                            break
                    except Exception, error:
                        print error
        except:
            continue
        if ok:
            break
    
    label = "Source Python"
    if m1 and m2:
        pmc.menuItem(label=label, parent=m1, ia=m2, c=NP_source_python_main)
    elif m1:
        pmc.menuItem(label=label, parent=m1, c=NP_source_python_main)




# ast.py
# Copyright (C) Mako developers
#
# This module is part of Mako and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""Handles parsing of Python code.

Parsing to AST is done via _ast on Python > 2.5, otherwise the compiler
module is used.
"""

from StringIO import StringIO

# words that cannot be assigned to (notably 
# smaller than the total keys in __builtins__)


class ExpressionGenerator(object):
    """given an AST node, generates an equivalent literal Python expression."""
    def __init__(self, astnode):
        self.buf = StringIO()
        compiler.visitor.walk(astnode, self) #, walker=walker())
    def value(self):
        return self.buf.getvalue()
    def operator(self, op, node, *args):
        self.buf.write("(")
        self.visit(node.left, *args)
        self.buf.write(" %s " % op)
        self.visit(node.right, *args)
        self.buf.write(")")
    def booleanop(self, op, node, *args):
        self.visit(node.nodes[0])
        for n in node.nodes[1:]:
            self.buf.write(" " + op + " ")
            self.visit(n, *args)
    def visitConst(self, node, *args):
        self.buf.write(repr(node.value))
    def visitAssName(self, node, *args):
        # TODO: figure out OP_ASSIGN, other OP_s
        self.buf.write(node.name)
    def visitName(self, node, *args):
        self.buf.write(node.name)
    def visitMul(self, node, *args):
        self.operator("*", node, *args)
    def visitAnd(self, node, *args):
        self.booleanop("and", node, *args)
    def visitOr(self, node, *args):
        self.booleanop("or", node, *args)
    def visitBitand(self, node, *args):
        self.booleanop("&", node, *args)
    def visitBitor(self, node, *args):
        self.booleanop("|", node, *args)
    def visitBitxor(self, node, *args):
        self.booleanop("^", node, *args)
    def visitAdd(self, node, *args):
        self.operator("+", node, *args)
    def visitGetattr(self, node, *args):
        self.visit(node.expr, *args)
        self.buf.write(".%s" % node.attrname)
    def visitSub(self, node, *args):
        self.operator("-", node, *args)
    def visitNot(self, node, *args):
        self.buf.write("not ")
        self.visit(node.expr)
    def visitDiv(self, node, *args):
        self.operator("/", node, *args)
    def visitFloorDiv(self, node, *args):
        self.operator("//", node, *args)
    def visitSubscript(self, node, *args):
        self.visit(node.expr)
        self.buf.write("[")
        [self.visit(x) for x in node.subs]
        self.buf.write("]")
    def visitUnarySub(self, node, *args):
        self.buf.write("-")
        self.visit(node.expr)
    def visitUnaryAdd(self, node, *args):
        self.buf.write("-")
        self.visit(node.expr)
    def visitSlice(self, node, *args):
        self.visit(node.expr)
        self.buf.write("[")
        if node.lower is not None:
            self.visit(node.lower)
        self.buf.write(":")
        if node.upper is not None:
            self.visit(node.upper)
        self.buf.write("]")
    def visitDict(self, node):
        self.buf.write("{")
        c = node.getChildren()
        for i in range(0, len(c), 2):
            self.visit(c[i])
            self.buf.write(": ")
            self.visit(c[i + 1])
            if i < len(c) - 2:
                self.buf.write(", ")
        self.buf.write("}")
    def visitTuple(self, node):
        self.buf.write("(")
        c = node.getChildren()
        for i in range(0, len(c)):
            self.visit(c[i])
            if i < len(c) - 1:
                self.buf.write(", ")
        self.buf.write(")")
    def visitList(self, node):
        self.buf.write("[")
        c = node.getChildren()
        for i in range(0, len(c)):
            self.visit(c[i])
            if i < len(c) - 1:
                self.buf.write(", ")
        self.buf.write("]")
    def visitListComp(self, node):
        self.buf.write("[")
        self.visit(node.expr)
        self.buf.write(" ")
        for n in node.quals:
            self.visit(n)
        self.buf.write("]")
    def visitListCompFor(self, node):
        self.buf.write(" for ")
        self.visit(node.assign)
        self.buf.write(" in ")
        self.visit(node.list)
        for n in node.ifs:
            self.visit(n)
    def visitListCompIf(self, node):
        self.buf.write(" if ")
        self.visit(node.test)
    def visitCompare(self, node):
        self.visit(node.expr)
        for tup in node.ops:
            self.buf.write(tup[0])
            self.visit(tup[1])
    def visitCallFunc(self, node, *args):
        self.visit(node.node)
        self.buf.write("(")
        if len(node.args):
            self.visit(node.args[0])
            for a in node.args[1:]:
                self.buf.write(", ")
                self.visit(a)
        self.buf.write(")")
