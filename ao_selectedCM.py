# -*- coding: utf-8 -*-
"""
========================================================================================================================
AO Selected Component Manager v1.0
========================================================================================================================
    Author: Anil Onlem <anilonlem@gmail.com>
    Date: 20-07-2014

    Description: This tool gives the user the ability to store component selections of the meshes outside of maya
        projects and reuse them into the same topology but not necessary to be the same mesh. This gives the selected
        component files to be used in every duplicate of the base mesh.
        The user can create/rename/delete a character folder to organize the character specific selections. The user can
        access to the character list from the characters menu and stored selection components is displayed on a text
        scroll list below the menu. Selection in the list can be activated by double click after the mesh selection from
        the maya.
        The user can also add a new set/ update the selected set or delete the selected set by using the New Set/ Update
        Set/Delete Set Buttons.
        There is also another function for the selection to give extra usability of the selections called add/sub
        selection buttons. These buttons adds or subtracts the sets from the selected components of the mesh.

    How to use:
        1. Create a path for the tool library.('C:/Users/~/Documents/maya/2017/scripts/selectedCM_lib/') (~ = user name)
        2. Create a new character folder by pressing the new character button and write the character's name
        3. Select the Base mesh and create any type of component selection(vtx,face and else.)
        4. Create a new set by pressing the new set button and write the set's name
        5. Select another mesh with the same topology.
        6. Double click the set in the text scroll list.
        7. More sets gives the user the ability to add or substract from the selections and update the current sets by
        pressing the update set buttons.

    Installation:
        1. Copy ao_selectedCM.py to '/Users/[USER]/Documents/maya/[MAYAVERSION]/prefs/scripts'
        2. Launch / Restart Maya
        3. Type into 'Script Editor' (Python tab) and execute
            import ao_selectedCM
            ao_selectedCM.UI()
========================================================================================================================
"""
import pymel.core as pm
import os
import cPickle
import sys
import time

""""this is a unique file extension specified only for this tool
all the created files is stored into a specified path"""
sComponentFileExtension = 'cse'


def UI():
    # A function to instantiate the Selected Component Manager window
    return SelectedCM.UI()


class SelectedCM(object):
    # A class for a basic selected component manager window
    @classmethod
    def UI(cls):
        # A function to instantiate the Selected Component Manager window
        win = cls()
        win.create()
        return win

    def __init__(self):
        """ Selected CM Class initializer
        """
        # Initialize data attributes
        # window tag
        self.window = 'SelectedCMWindow'
        self.mainForm = None
        self.textscroll_listFrame = None
        self.textscroll_listGrid = None
        self.optionMenuLbl = None
        self.txtScrlLs = None
        self.controlFrame = None
        self.controlGrid = None
        self.newCharacterBtn = None
        self.renameCharacterBtn = None
        self.deleteCharacterBtn = None
        self.updateSetBtn = None
        self.deleteSetBtn = None
        self.addToSelectionBtn = None
        self.subFromSelectionBtn = None
        self.doneBtn = None
        self.newSetBtn = None
        # window title
        self.title = 'Selected Component Manager'
        # window size
        self.size = (360, 480)
        # Directory path for the program to read and write the files.
        self.dirName = os.path.expandvars('M:/Personal_Backup/Anil/selectedCM_lib/')
        # selectedFile is a variable to keep the selected file from textscroll_list
        self.selectedFile = None
        self.selectedCharacter = None
        # checkList is a variable to keep the selected files path
        self.checkList = None
        self.characterList = None
        self.selectedObject = None

    def create(self):
        """Main UI function
        @usage: selectedCM.UI()
        :return: None
        """
        # delete the window if exists
        if pm.window(self.window, exists=True):
            pm.deleteUI(self.window, window=True)
        # initialize the window
        pm.window(self.window, title=self.title, wh=self.size, s=False)
        # main form layout
        self.mainForm = pm.formLayout()
        # frame for Stored files
        self.textscroll_listFrame = pm.frameLayout(label='Stored Component Files')
        # Stored files grid 2x1 and text_scroll_list which has double_click_cmd and select_cmd
        self.textscroll_listGrid = pm.columnLayout(w=self.size[0]/2-2, h=self.size[1]-2, cw=self.size[0]/2-2)
        pm.separator(h=5)
        self.optionMenuLbl = pm.optionMenuGrp("character_menu", label="Characters:", w=self.size[0]/2-10, h=30,
                                              ct2=['left', 'both'], co2=[5, 0], cw2=[65, 95], cc=self.get_files_cmd)
        pm.separator(h=10)
        # pm.setParent(self.textscroll_listForm)
        self.txtScrlLs = pm.textScrollList("txtScrlLs", w=self.size[0]/2-4, h=410, dcc=self.double_click_cmd,
                                            sc=self.select_cmd)
        # setting the parent to the main form and frame for control buttons
        pm.setParent(self.mainForm)
        self.controlFrame = pm.frameLayout(label='Control')
        # control buttons grid 10x1 and buttons to control the selections and files
        self.controlGrid = pm.columnLayout(w=self.size[0]/2-2, cw=self.size[0]/2-2)
        pm.separator(h=10)
        self.newCharacterBtn = pm.button(label='New Character', w=self.size[0]/2-4, h=30, c=self.new_character_btn_cmd)
        self.renameCharacterBtn = pm.button(label='Rename Character', w=self.size[0]/2-4, h=30,
                                            c=self.rename_character_btn_cmd)
        self.deleteCharacterBtn = pm.button(label='Delete Character', w=self.size[0]/2-4, h=30,
                                            c=self.delete_character_btn_cmd)
        pm.separator(h=40)
        self.newSetBtn = pm.button(label='New Set', w=self.size[0]/2-4, h=30, c=self.new_set_btn_cmd)
        self.updateSetBtn = pm.button(label='Update Set', w=self.size[0]/2-4, h=30, c=self.update_set_btn_cmd)
        self.deleteSetBtn = pm.button(label='Delete Set', w=self.size[0]/2-4, h=30, c=self.delete_set_btn_cmd)
        pm.separator(h=40)
        self.addToSelectionBtn = pm.button(label='Add To Selection', w=self.size[0]/2-4, h=30,
                                           c=self.add_to_selection_btn_cmd)
        self.subFromSelectionBtn = pm.button(label='Sub From Selection', w=self.size[0]/2-4, h=30,
                                             c=self.sub_from_selection_btn_cmd)
        pm.separator(h=40)
        self.doneBtn = pm.button(label='QUIT', w=self.size[0]/2-4, h=30, c=self.done_btn_cmd)
        # attach stored files frame and control buttons frame in main form
        ac = []
        af = []
        ac.append([self.controlFrame, 'left', 0, self.textscroll_listFrame])
        af.append([self.textscroll_listFrame, 'left', 0])
        af.append([self.textscroll_listFrame, 'top', 0])
        af.append([self.textscroll_listFrame, 'bottom', 0])
        af.append([self.controlFrame, 'right', 0])
        af.append([self.controlFrame, 'top', 0])
        af.append([self.controlFrame, 'bottom', 0])
        pm.formLayout(self.mainForm, e=True, attachControl=ac, attachForm=af)
        # show the window
        pm.showWindow(self.window)
        # force the window size
        pm.window(self.window, e=True, wh=self.size)
        self.characterList = init_folder(self.dirName)
        populate_characters(self.dirName, self.selectedCharacter, self.characterList, self.selectedFile)
        # calling the stored files from the path into the textscroll_list

    def get_files_cmd(self, *args):
        """ Get the files from the directory folder and put them into a menu for selection
        :return: None
        """
        self.selectedCharacter = pm.optionMenuGrp("character_menu", q=True, v=True)
        self.characterList = str(self.dirName + self.selectedCharacter + "/")
        populate_characters(self.dirName, self.selectedCharacter, self.characterList, self.selectedFile)

    def select_cmd(self):
        """This command activates when the user selects any file. it keeps the file name and find the path using the
        directory path
        :return: None
        """
        self.selectedFile = pm.textScrollList("txtScrlLs", q=True, si=True)[0]
        self.selectedFile, ID = self.selectedFile.split(" ")
        self.checkList = str(self.characterList + self.selectedFile + ".cse")
        pm.selectMode(component=True)

    def double_click_cmd(self):
        """This command activates when the user double-clicks the file from the scroll list. It looks that the mesh
        object selected to activate the selection.
        :return: None
        """
        pm.selectMode(object=True)
        if not self.get_s_object():
            self.selectedObject = None
            self.selectedObject = import_component(self.checkList, self.selectedObject)
            populate_characters(self.dirName, self.selectedCharacter, self.characterList, self.selectedFile)
        else:
            import_component(self.checkList, self.selectedObject)
            populate_characters(self.dirName, self.selectedCharacter, self.characterList, self.selectedFile)

    def get_selection(self):
        """This function selects the components from the mesh and split the component ID's store them into a list.
        :return: None
        """
        selected_list = pm.ls(sl=True, fl=True)
        selected_object = []
        selected_component_list = []
        for i in range(0, len(selected_list)):
            a, b = selected_list[i].split(".")
            selected_object.append(a)
            selected_component_list.append(b)
        if selected_list is None or len(selected_list) < 1:
            pm.confirmDialog(t='Error', b=['OK'], m='Please select one or more components.')
            return None
        else:
            return selected_component_list
        populate_characters(self.dirName, self.selectedCharacter, self.characterList, self.selectedFile)

    def new_character_btn_cmd(self, *args):
        """ This button command opens a new character naming window and creates a new character folder on the directory
        folder.
        :return: None
        """
        def store_character_name_cmd(*args):
            """ This command stores the written name for new character and populate it by using the populate characters
            module
            :return: None
            """
            src = pm.textField("NewCName", q=True, tx=True)
            if src is None or len(src) < 1:
                None
            else:
                new_character = self.dirName + src
                if not os.path.exists(new_character):
                    os.makedirs(new_character)
                    quit_character_win_cmd()
                    self.selectedCharacter = src
                    self.characterList = str(new_character+"/")
                    populate_characters(self.dirName, self.selectedCharacter, self.characterList, self.selectedFile)
                else:
                    pm.confirmDialog(t='Error', b=['OK'], m='This folder name exists.')
                    return None
        # this command checks the side window is open or not.

        def quit_character_win_cmd(*args):
            """ Checks the new character window exists
            :return: None
            """
            if pm.window('newCharacterWin', exists=True):
                pm.deleteUI('newCharacterWin', window=True)
        # side windows tag name
        new_character_win = 'newCharacterWin'
        # activation the delete_set_cmd to check the window
        quit_character_win_cmd()
        # size of the side window
        size = (250, 80)
        # initialize the side window
        pm.window(new_character_win, wh=size, s=False, t='New Character Name')
        # main form layout
        mainForm = pm.formLayout()
        # controls
        new_character_text = pm.text(label='New Character Name')
        new_character_text_field = pm.textField("NewCName", text="")
        new_character_text_btn = pm.button(label='ADD CHARACTER', c=store_character_name_cmd, p=mainForm, w=100, h=26)
        cancel_btn = pm.button(label='CANCEL', c=quit_character_win_cmd, p=mainForm, w=100, h=26)
        # attach the controls to main form
        ac = []
        af = []
        ac.append([new_character_text_field, 'top', 5, new_character_text])
        ac.append([new_character_text_field, 'bottom', 5, new_character_text_btn])
        ac.append([new_character_text_field, 'bottom', 5, cancel_btn])
        af.append([new_character_text, 'top', 5])
        af.append([new_character_text, 'left', 5])
        af.append([new_character_text, 'right', 5])
        af.append([new_character_text_field, 'left', 5])
        af.append([new_character_text_field, 'right', 5])
        af.append([new_character_text_btn, 'left', 5])
        af.append([new_character_text_btn, 'bottom', 5])
        af.append([cancel_btn, 'right', 5])
        af.append([cancel_btn, 'bottom', 5])
        pm.formLayout(mainForm, e=True, attachControl=ac, attachForm=af)
        # force the window size
        pm.window(new_character_win, e=True, wh=size)
        # initialize the window
        pm.showWindow(new_character_win)

    def delete_character_btn_cmd(self, *args):
        """ Delete selected character folder from the text scroll list
        :return: None
        """
        # When it is pressed this condition checks the character is selected or not.
        if self.selectedCharacter is None or len(self.selectedCharacter) < 1:
            pm.confirmDialog(t='Error', b=['OK'], m='Please select the folder to be deleted.')
            return None
        else:
            # if it is selected a confirm dialog appears and give the user a choice for deletion.
            answer = pm.confirmDialog(t='Confirmation', b=['Yes', 'No'],
                                      m="'Do you want to delete " + self.selectedCharacter+" character folder?'",
                                      defaultButton='Yes', cancelButton='No', dismissString='No')
            if answer == 'Yes':
                # if the answer is yes, it also checks the folder is empty or not and gives another confirm dialog if
                # the folder is not empty
                comp_files = os.listdir(self.characterList)
                if comp_files is None or len(comp_files) < 1:
                    pm.confirmDialog(t='Error', b=['OK'], m='this folder is empty.')
                    os.rmdir(self.characterList)
                else:
                    ans = pm.confirmDialog(t='Confirmation', b=['Yes', 'No'],
                                           m="'This " + self.selectedCharacter +
                                             " has files. Do you still want to delete folder and its files?'",
                                           defaultButton='Yes', cancelButton='No', dismissString='No')
                    if ans == 'Yes':
                        for compFile in comp_files:
                            pm.sysFile(str(self.characterList + compFile), delete=True)
                        os.rmdir(self.characterList)
                    else:
                        None
            else:
                None
            # populate_characters(self.dirName, self.selectedCharacter, self.characterList, self.selectedFile)

    def rename_character_btn_cmd(self, *args):
        """ Rename the selected character folder from the text scroll field by opening another window
        :return: None
        """
        def rename_character_name_cmd(*args):
            """ Rename the selected character folder
            :return: None
            """
            src = pm.textField("RenameCName", q=True, tx=True)
            if src is None or len(src) < 1:
                None
            else:
                if src == self.selectedCharacter:
                    new_character = str(self.dirName + src)
                else:
                    new_character = str(self.dirName + src + "/")
                if os.path.exists(self.characterList):
                    os.rename(self.characterList, new_character)
                    quit_character_win_cmd()
                    self.selectedCharacter = src
                    self.characterList = str(new_character+"/")
                    populate_characters(self.dirName, self.selectedCharacter, self.characterList, self.selectedFile)
                else:
                    pm.confirmDialog(t='Error', b=['OK'], m='This folder name exists.')
                    return None

        def quit_character_win_cmd(*args):
            """ This command checks the side window is open or not.
            :return: None
            """
            if pm.window(rename_character_win, exists=True):
                pm.deleteUI(rename_character_win, window=True)
        # side windows tag name
        rename_character_win = 'renameCharacterWin'
        # activation the delete_set_cmd to check the window
        quit_character_win_cmd()
        # size of the side window
        size = (250, 100)
        if len(self.selectedCharacter) > size[0]:
            size[0] = len(self.selectedCharacter)+250
        # initialize the side window
        pm.window(rename_character_win, wh=size, s=False, t='Rename Character Name')
        # main form layout
        main_form = pm.formLayout()
        # controls
        rename_character_layout = pm.columnLayout(cat=['both', 2], cw=size[0], rs=10)
        pm.text(label='Rename Character Name')
        pm.text(label=self.selectedCharacter, w=len(self.selectedCharacter)+50)
        pm.setParent(main_form)
        rename_character_text_field = pm.textField("RenameCName", text=self.selectedCharacter,
                                                   ec=rename_character_name_cmd, aie=True)
        rename_character_text_btn = pm.button(label='RENAME', c=rename_character_name_cmd, p=main_form, w=100, h=26)
        cancel_btn = pm.button(label='CANCEL', c=quit_character_win_cmd, p=main_form, w=100, h=26)
        # attach the controls to main form
        ac = []
        af = []
        ac.append([rename_character_text_field, 'top', 5, rename_character_layout])
        ac.append([rename_character_text_field, 'bottom', 5, rename_character_text_btn])
        ac.append([rename_character_text_field, 'bottom', 5, cancel_btn])
        af.append([rename_character_layout, 'top', 5])
        af.append([rename_character_layout, 'left', 5])
        af.append([rename_character_layout, 'right', 5])
        af.append([rename_character_text_field, 'left', 5])
        af.append([rename_character_text_field, 'right', 5])
        af.append([rename_character_text_btn, 'left', 5])
        af.append([rename_character_text_btn, 'bottom', 5])
        af.append([cancel_btn, 'right', 5])
        af.append([cancel_btn, 'bottom', 5])
        pm.formLayout(main_form, e=True, attachControl=ac, attachForm=af)
        # force the window size
        pm.window(rename_character_win, e=True, wh=size)
        # initialize the window
        pm.showWindow(rename_character_win)

    def new_set_btn_cmd(self, *args):
        """This function is for creating a new selecting set getting the selected component list from get_selection func.
        :return:
        """
        selected_component_list = self.get_selection()
        if selected_component_list is None:
            return
        # this function activates when the user presses the ADD SET btn it gets the file names from the path to compare
        # the new file name otherwise it sends the new file name in the path and the selected component list to
        # export_component function
        if selected_component_list[0].startswith("vtx["):
            suffix = "_vtx"
        elif selected_component_list[0].startswith("vtxFace["):
            suffix = "_vtxFace"
        elif selected_component_list[0].startswith("e["):
            suffix = "_edge"
        elif selected_component_list[0].startswith("f["):
            suffix = "_poly"
        else:
            None

        def store_set_name_cmd(*args):
            """ Stores the new set
            :return: None
            """
            src = pm.textField("NewSName", q=True, tx=True)
            src = src + suffix
            if src is None or len(src) < 1:
                None
            else:
                comp_files = os.listdir(self.characterList)
                if comp_files is None or len(comp_files) < 1:
                    new_path = self.characterList + "/" + src + ".cse"
                    delete_set_cmd()
                    export_component(new_path, selected_component_list)
                    populate_characters(self.dirName, self.selectedCharacter, self.characterList, self.selectedFile)
                else:
                    for comp_file in comp_files:
                        if comp_file.endswith(".cse"):
                            test = str(src+".cse")
                            if test == comp_file:
                                pm.confirmDialog(t='Error', b=['OK'], m='This file name exists.')
                                return None
                            else:
                                new_path = self.characterList + "/" + src + ".cse"
                                delete_set_cmd()
                                export_component(new_path, selected_component_list)
                                populate_characters(self.dirName, self.selectedCharacter, self.characterList,
                                                    self.selectedFile)

        def delete_set_cmd(*args):
            """ This command checks the side window is open or not.
            :return: None
            """
            if pm.window('newSetWin', exists=True):
                pm.deleteUI('newSetWin', window=True)
        # side windows tag name
        new_set_win = 'newSetWin'
        # activation the delete_set_cmd to check the window
        delete_set_cmd()
        # size of the side window
        size = (250, 80)
        # initialize the side window
        pm.window(new_set_win, wh=size, s=False, t='New Set Name')
        # main form layout
        main_form = pm.formLayout()
        # controls
        new_set_text = pm.text(label='New Set Name')
        new_set_text_field = pm.textField("NewSName", text="")
        new_set_text_btn = pm.button(label='ADD SET', c=store_set_name_cmd, p=main_form, w=100, h=26)
        cancel_btn = pm.button(label='CANCEL', c=delete_set_cmd, p=main_form, w=100, h=26)
        # attach the controls to main form
        ac = []
        af = []
        ac.append([new_set_text_field, 'top', 5, new_set_text])
        ac.append([new_set_text_field, 'bottom', 5, new_set_text_btn])
        ac.append([new_set_text_field, 'bottom', 5, cancel_btn])
        af.append([new_set_text, 'top', 5])
        af.append([new_set_text, 'left', 5])
        af.append([new_set_text, 'right', 5])
        af.append([new_set_text_field, 'left', 5])
        af.append([new_set_text_field, 'right', 5])
        af.append([new_set_text_btn, 'left', 5])
        af.append([new_set_text_btn, 'bottom', 5])
        af.append([cancel_btn, 'right', 5])
        af.append([cancel_btn, 'bottom', 5])
        pm.formLayout(main_form, e=True, attachControl=ac, attachForm=af)
        # force the window size
        pm.window(new_set_win, e=True, wh=size)
        # initialize the window
        pm.showWindow(new_set_win)

    def update_set_btn_cmd(self, *args):
        """ This function is getting the last selected files name and path and get the new selected components and merge
        them in together in the end the new file is created by the same name as update the file
        :return: None
        """
        if self.selectedFile is None or len(self.selectedFile) < 1:
            pm.confirmDialog(t='Error', b=['OK'], m='Please select the file to be updated.')
            return None
        else:
            inform = pm.confirmDialog(t='Confirmation', b=['Yes', 'No'], m="'Do you want to update " +
                                                                           self.selectedFile + " this selected set?'",
                                      defaultButton='Yes', cancelButton='No', dismissString='No')
            if inform == 'Yes':
                selected_component_list = self.get_selection()
                if selected_component_list is None:
                    return
                export_component(self.checkList, selected_component_list)
            else:
                None
        populate_characters(self.dirName, self.selectedCharacter, self.characterList, self.selectedFile)

    def delete_set_btn_cmd(self, *args):
        """ This function checks if the file is selected from the list and asks the user to delete that item yes or no
        :return: None
        """
        if self.selectedFile is None or len(self.selectedFile) < 1:
            pm.confirmDialog(t='Error', b=['OK'], m='Please select the file to be deleted.')
            return None
        else:
            answer = pm.confirmDialog(t='Confirmation', b=['Yes', 'No'], m='Do you want to delete this selected set?',
                                      defaultButton='Yes', cancelButton='No', dismissString='No')
            if answer == 'Yes':
                pm.sysFile(self.checkList, delete=True)
            else:
                None
            populate_characters(self.dirName, self.selectedCharacter, self.characterList, self.selectedFile)

    def add_to_selection_btn_cmd(self, *args):
        """This function gets the new selection of the components from the mesh and adds the selected file's stored
        components into the same selection
        :return: None
        """
        selected_list = pm.ls(sl=True, fl=True)
        pm.select(cl=True)
        if pm.selectMode(q=True, object=True):
            None
        else:
            pm.selectMode(object=True)
        obj = get_selected_object()
        import_component(self.checkList, self.selectedObject)
        pm.select(selected_list, add=True)
        pm.selectMode(component=True)
        pm.hilite(obj, r=True)
        populate_characters(self.dirName, self.selectedCharacter, self.characterList, self.selectedFile)

    def sub_from_selection_btn_cmd(self, *args):
        """ This function gets the new selection of the components from the mesh and subtracts the selected file's
        stored components from the same selection
        :return: None
        """
        selected_list = pm.ls(sl=True, fl=True)
        pm.select(cl=True)
        if pm.selectMode(q=True,object=True):
            None
        else:
            pm.selectMode(object=True)
        obj = get_selected_object()
        import_component(self.checkList, self.selectedObject)
        imported_list = pm.ls(sl=True, fl=True)
        pm.select(selected_list)
        pm.select(imported_list, d=True)
        pm.selectMode(component=True)
        pm.hilite(obj, r=True)
        populate_characters(self.dirName, self.selectedCharacter, self.characterList, self.selectedFile)

    def done_btn_cmd(self, *args):
        """ This function closes the selected component manager
        :return: None
        """
        answer = pm.confirmDialog(t='Confirmation', b=['Yes', 'No'], m='Do you want to quit?', defaultButton='Yes',
                                  cancelButton='No', dismissString='No')
        if answer == 'Yes':
            pm.deleteUI(self.window, window=True)
        else:
            None

    def get_s_object(self, *args):
        """ This function gets the object name which is selected
        :return: None
        """
        obj = pm.ls(sl=1)
        if obj is None or len(obj) < 1:
            return False
        else:
            return True
        # end of the class


def populate_characters(path_name, selected_character, characterList, selected_file):
    clear_option_menu("character_menu")
    characters = os.listdir(path_name)
    for characterFolder in characters:
        pm.menuItem(characterFolder, label=characterFolder, parent=("character_menu"+'|OptionMenu'))
    if selected_character is None:
        scroll_list(str(path_name + characters[0] + "/"), selected_file)
    else:
        pm.optionMenuGrp("character_menu", e=True, v=selected_character)
        scroll_list(str(path_name + selected_character + "/"), selected_file)


def get_selected_object():
    """ This function gets the object whether or not has a component in the end of the name eg.pSphere1.vtx[254]
    :return: selected first object
    """
    return pm.ls(sl=1)[0]


def init_folder(path_name):
    return str(path_name + os.listdir(path_name)[0] + "/")


def export_component(file_path, selected_component_list):
    """ This function opens a file and stores the component ID's and the name of the file is at end of the filePath
    :param file_path:
    :param selected_component_list:
    :return:
    """
    try:
        f = open(file_path, 'w')
    except:
        pm.confirmDialog(
            t='Error', b=['OK'],
            m='Unable to write file: %s' % file_path
        )
        raise
    cPickle.dump(selected_component_list, f)
    f.close()


def import_component(file_path, selected_object):
    """ This function opens the selected file and reads the information from the file
    :param file_path:
    :param selected_object:
    :return:
    """
    try:
        f = open(file_path, 'r')
    except:
        pm.confirmDialog(
            t='Error', b=['OK'],
            m='Unable to read file: %s' % file_path
        )
        raise
    component = cPickle.load(f)
    f.close()
    # this list is for storing the unmatched component ID's
    err_comps = []
    # selected objects name
    if selected_object is None:
        selected_object = get_selected_object()
    else:
        None
    # this list is for storing the component ID's with the name of the object
    selection = []
    # clearing any selection on the mesh
    pm.select(clear=True)
    # this for loop is for merging and the storing the component ID's with the object ID unmatched ID's is gonna be
    # stored in errComps list.
    for compValue in component:
        try:
            selection.append(selected_object+"."+compValue)
        except:
            try:
                err_comps.append(compValue[0])
            except:
                err_comps.append(compValue)
    # changing the select mode into component mode
    pm.selectMode(component=True)
    # changing the hilite visibility to true
    pm.hilite(selected_object, r=True)
    # this is for checking the component types and changing the selection type to the chosen component
    if component[0].startswith("vtx["):
        pm.selectType(pv=True)
    elif component[0].startswith("vtxFace["):
        pm.selectType(pvf=True)
    elif component[0].startswith("e["):
        pm.selectType(pe=True)
    elif component[0].startswith("f["):
        pm.selectType(pf=True)
    else:
        None
    # applying the selection by using the list
    pm.select(selection, r=True)
    # checks the component errors if any
    if len(err_comps) > 0:
        import_error_window(err_comps)
        sys.stderr.write('Not all components could be loaded.')
    return selected_object


def scroll_list(file_path, selected_file):
    """ This function is updating the scroll_list when its called and ordering the files by using their modification
    times
    :param file_path:
    :param selected_file:
    :return:
    """
    # this list is for sorting the files from the selected path(filePath)
    sort_list = []
    i_d = None
    # clearing the scroll_list
    pm.textScrollList("txtScrlLs", e=True, ra=True)
    # getting all the files from the path
    comp_files = os.listdir(file_path)
    # searching the files endswith ".cse" which resembles the componentFileExtension
    for setFile in comp_files:
        if setFile.endswith(".cse"):
            # spliting all the time information
            x, m, d, t, y = time.ctime(os.path.getmtime(file_path + "/" + setFile)).split(" ")
            # month,date and time
            file_time = m+d+t
            # adding the file name in the end to keep the file name and its modification
            # time in the same string value
            sort_list.append(file_time + "+" + setFile)
    # sorting the list the order is month(alphabetically) then date then time
    sort_list.sort()
    # spliting the string to get the file name and store into the scroll_list in
    # that sorted order
    for set_f in sort_list:
        set_t, set_f = set_f.split("+")
        file_output = open(str(file_path + set_f), 'r')
        comp_file = cPickle.load(file_output)
        for compID in comp_file:
            if compID.startswith("vtx["):
                i_d = " (V)"
            elif compID.startswith("vtxFace["):
                i_d = " (VF)"
            elif compID.startswith("e["):
                i_d = " (E)"
            elif compID.startswith("f["):
                i_d = " (F)"
            else:
                None
        set_f, extension = set_f.split(".")
        # print(set_f)
        if set_f == selected_file:
            # setFile,suf = setFile.split("_")
            pm.textScrollList("txtScrlLs", e=True, append=(set_f + i_d), si=(set_f + i_d))
        else:
            # setFile,suf = setFile.split("_")
            pm.textScrollList("txtScrlLs", e=True, append=(set_f + i_d))


def clear_option_menu(character_menu):
    """ Clearing option menu
    :param character_menu:
    :return:
    """
    try:
        menu_items = pm.optionMenuGrp(character_menu, q=True, ill=True)
        if menu_items != None and menu_items != []:
            pm.deleteUI(menu_items)
        first_item = menu_items[0]
        first_item[:-len(first_item.split('|')[-1])-1]
    except: pass


def import_error_window(err_comps):
    """ An error window to display if there are unknown compnents when importing the selected components
    :param err_comps:
    :return:
    """
    win = 'anlErrorWindow'
    # a function to dismiss the window

    def dismiss():
        pm.deleteUI(win, window=True)
    # destroy the window if it exists
    if pm.window(win, exists=True):
        dismiss()
    # create the window and the size
    size = (300, 200)
    pm.window(
        win, wh=size, s=False,
        t='Unknown Components'
    )
    main_form = pm.formLayout()
    # info label
    info_l = pm.text(label='The following components could not be found.\nThey are being ignored.', al='left')
    # display a list of components that could not be loaded
    scroll_l = pm.scrollLayout(w=size[0])
    err_str = ''.join('\t- %s\n' % a for a in err_comps).rstrip()
    pm.text(label=err_str, al='left')
    # dismiss button
    btn = pm.button(label='OK', c=dismiss, p=main_form, h=26)
    # attach controls
    ac = []
    af = []
    ac.append([scroll_l, 'top', 5, info_l])
    ac.append([scroll_l, 'bottom', 5, btn])
    af.append([info_l, 'top', 5])
    af.append([info_l, 'left', 5])
    af.append([info_l, 'right', 5])
    af.append([scroll_l, 'left', 0])
    af.append([scroll_l, 'right', 0])
    af.append([btn, 'left', 5])
    af.append([btn, 'right', 5])
    af.append([btn, 'bottom', 5])
    pm.formLayout(
        main_form, e=True,
        attachControl=ac, attachForm=af
    )
    # show the window
    pm.window(win, e=True, wh=size)
    pm.showWindow(win)
