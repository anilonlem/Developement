# -*- coding: utf-8 -*-
"""
===========================================================
AO Two Point v1.0
===========================================================
    Author: Anil Onlem <anilonlem@gmail.com>
    Date: 25-07-2018

    Description: By creating two locators which will be a
    start and an end locator, this tool creates FK, IK or
    IK DRIVER setup.

    How to use:
        1. Create two locators and position them manually,
    naming won't matter
        2. Select the Start Locator
        3. Select the End Locator
        4. Choose the Part
        5. Choose the Type
        6. Choose how many ctrl will be created or jnt
    will be used in setups
        7. Choose a Curve Type
        8. Select a Color for the curve colors
        9. Press "Run"
        10. If you want to close the tool press "Quit"
    or close it from the window

    Installation:
        1. Copy ao_twoPoint.py to
    '\Users\[USER]\Documents\maya\[MAYAVERSION]\prefs\scripts'
        2. Launch / Restart Maya
        3. Type into 'Script Editor' (Python tab) and execute
            import ao_twoPoint
            ao_twoPoint.ui()
===========================================================
"""
import pymel.core as pm


def ui():
    return TwoPoint.ui()


class TwoPoint(object):
    @classmethod
    def ui(cls):
        win = cls()
        win.create()
        return win

    def __init__(self):
        """Two Point Setup Class initializer
        """
        # UI window and frame variables
        self.window = 'ao_two_point_window'
        self.main_form = None
        self.locators_frame = None
        self.part_n_type_frame = None
        self.sub_selection_frame = None
        # title and size of the main window
        self.title = 'AO Two Point'
        self.size = (360, 360)
        # field, menu and radio elements variables
        self.select_sloc_field = None
        self.select_eloc_field = None
        self.part_radio_btn = None
        self.type_radio_btn = None
        self.ctrl_number_menu = None
        self.crv_types_menu = None
        self.color_palette = None
        # number array for ctrl crv number
        self.ctrl_nums = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        # name array for crv types
        self.crv_types = ['cross_crv', 'circle_crv', 'cube_crv', 'sphere_crv', 'rot_180_crv', 'rombus_crv', 'nail_crv']
        # selection variables for the ui elements
        self.part_selection = None
        self.type_selection = None
        self.number = None
        self.crv_type = None
        self.color_index = None
        # scale values from the selected locator scales
        self.ik_ctrl_s_scale = None
        self.ik_ctrl_e_scale = None
        # selected start ctrl name end ctrl name and infix name
        self.infix = None
        self.name = None
        self.name_end = None
        # available start name, end name and infix name arrays
        self.infix_list = ['_fk_', '_ik_', '_ikd_']
        self.name_list = ['neck', 'spine', 'tail']
        self.name_end_list = ['head', 'chest', 'tail_end']
        # stretchy option
        self.stretchy = None
        self.jnt_chain = []
        self.distance = None
        self.ref_jnt = None
        self.ref_jntend = None
        self.top_start_grp = None
        self.top_end_grp = None
        self.check = True
        self.ctrl_list = []

    def create(self):
        """Main UI function
        @ usage: AO2PRigSetup.ui()
        :return: None
        """
        # check the window exists before creating the new one
        if pm.window(self.window, exists=True):
            pm.deleteUI(self.window, window=True)
        # window UI
        self.window = pm.window(self.window, title=self.title, wh=self.size, s=False)
        # main from is formLayout
        self.main_form = pm.formLayout()
        # first frameLayout for locators panel
        self.locators_frame = pm.frameLayout(label='Locators')
        pm.columnLayout(w=self.size[0]/2-2, h=self.size[1]/2-2, cw=self.size[0]/2-2)
        pm.separator(h=5)
        # start locator panels
        pm.text(label='Start Locator', w=self.size[0]/2-2, h=30)
        self.select_sloc_field = pm.textFieldButtonGrp(ed=False, w=self.size[0]/2-2, h=30, bl='Select',
                                                       cl3=['left', 'left', 'left'], cw=[1, self.size[0]/2-50],
                                                       bc=self._select_start_loc)
        # end locator panels
        pm.text(label='End Locator', w=self.size[0] / 2 - 2, h=30)
        self.select_eloc_field = pm.textFieldButtonGrp(ed=False, w=self.size[0] / 2 - 2, h=30, bl='Select',
                                                       cl3=['left', 'left', 'left'], cw=[1, self.size[0] / 2 - 50],
                                                       bc=self._select_end_loc)
        pm.setParent(self.main_form)
        # second part and type frameLayout
        self.part_n_type_frame = pm.frameLayout(label='Part & Type')
        pm.columnLayout(w=self.size[0]/2-2, h=self.size[1]/2-2, cw=self.size[0]/2-2)
        pm.separator(h=5)
        # part radio button panel
        self.part_radio_btn = pm.radioButtonGrp(label='Part', labelArray3=['Neck', 'Spine', 'Tail'], nrb=3, vr=True,
                                                w=self.size[0]/2-2, cl2=['center', 'left'],
                                                cw2=[self.size[0]/4-20, self.size[0]/4], cc=self.get_parts_cmd)
        pm.separator(h=5)
        # type radio button panel
        self.type_radio_btn = pm.radioButtonGrp(label='Type', labelArray3=['FK', 'IK', 'IK DRIVER'], nrb=3, vr=True,
                                                w=self.size[0]/2-2, cl2=['center', 'left'],
                                                cw2=[self.size[0]/4-20, self.size[0]/4], cc=self.get_types_cmd)
        # third ctrl numbers and crv types frameLayout
        pm.setParent(self.main_form)
        self.sub_selection_frame = pm.frameLayout(label='Ctrl Numbers & Crv Types')
        pm.columnLayout(adj=True)
        pm.separator(h=5)
        # ctrl numbers menu panel
        self.ctrl_number_menu = pm.optionMenuGrp('Ctrl Numbers Menu', label='Ctrl Numbers Menu:', w=self.size[0]-2,
                                                 h=30)
        fill_menu(self.ctrl_nums)
        # ctrl types menu panel
        self.crv_types_menu = pm.optionMenuGrp('Crv Types Menu', label='Curve Types Menu:', w=self.size[0]-2, h=30)
        fill_menu(self.crv_types)
        pm.separator(h=5)
        # color palette panel
        self.color_palette = pm.palettePort(dim=(16, 2), t=0, w=self.size[0]-2, h=30, topDown=True, ced=True)
        fill_color_palette(self.color_palette)
        pm.separator(h=5)
        # run button
        pm.button(label='Run', w=self.size[0], h=30, c=self.do_selection_cmd)
        pm.separator(h=5)
        # quit button
        pm.button(label='QUIT', w=self.size[0], h=30, c=self.quit_btn_cmd)
        # organize all the layouts together under the mainForm of the window
        ac = []
        af = []
        ac.append([self.part_n_type_frame, 'left', 0, self.locators_frame])
        ac.append([self.locators_frame, 'bottom', 0, self.sub_selection_frame])
        af.append([self.locators_frame, 'left', 0])
        af.append([self.locators_frame, 'top', 0])
        af.append([self.part_n_type_frame, 'right', 0])
        af.append([self.part_n_type_frame, 'top', 0])
        af.append([self.sub_selection_frame, 'left', 0])
        af.append([self.sub_selection_frame, 'right', 0])
        af.append([self.sub_selection_frame, 'bottom', 0])
        pm.formLayout(self.main_form, e=True, attachControl=ac, attachForm=af)
        # create the window
        pm.showWindow(self.window)
        # resize it
        pm.window(self.window, e=True, wh=self.size)

    def _select_start_loc(self, *args):
        """This stores the selected starting locator's name and shows in text field
        :param args:
        :return: None
        """
        self.start_loc = pm.ls(sl=1)[0]
        pm.textFieldButtonGrp(self.select_sloc_field, e=True, tx=str(self.start_loc))
        self.ik_ctrl_s_scale = transformation_info(self.start_loc)['s']

    def _select_end_loc(self, *args):
        """This stores the selected end locator's name and shows in text field
        :param args:
        :return: None
        """
        self.end_loc = pm.ls(sl=1)[0]
        pm.textFieldButtonGrp(self.select_eloc_field, e=True, tx=str(self.end_loc))
        self.ik_ctrl_e_scale = transformation_info(self.end_loc)['s']

    def get_parts_cmd(self, *args):
        """Collects the selected part when the radio button switched or selected
        :param args:
        :return: None
        """
        # fk ik ikd
        self.part_selection = (pm.radioButtonGrp(self.part_radio_btn, q=True, sl=True)-1)
        self.name = self.name_list[self.part_selection]
        self.name_end = self.name_end_list[self.part_selection]

    def get_types_cmd(self, *args):
        """Collects the selected type part when the radio button switched or selected
        :param args:
        :return: None
        """
        self.type_selection = (pm.radioButtonGrp(self.type_radio_btn, q=True, sl=True)-1)
        self.infix = self.infix_list[self.type_selection]

    def do_selection_cmd(self, *args):
        """Runs the code with the collected data from the buttons, locators and menus of the UI.
        Gathers the number for the ctrls, type of the ctrl crvs, and color of the ctrl crvs.
        :param args:
        :return: None
        """
        # ctrl number menu gives the number of ctrls between the locators
        self.number = pm.optionMenuGrp(self.ctrl_number_menu, q=True, v=True)
        # crv types menu provides the choice of crv types only
        self.crv_type = pm.optionMenuGrp(self.crv_types_menu, q=True, v=True)
        # palette port provides the selected crv color
        self.color_index = pm.palettePort(self.color_palette, q=True, setCurCell=True)
        # right now fk ctrls scale of ikd is divided by 2.
        fk_scale = (self.ik_ctrl_s_scale[0]/2, self.ik_ctrl_s_scale[1]/2, self.ik_ctrl_s_scale[2]/2)
        # if the selection is FK
        if self.type_selection == 0:
            self.check = True
            # fk ctrl creation
            # create jnt chain
            self.jnt_chain = self.create_jnt_chain()
            pm.select(self.jnt_chain[0], r=1)
            root_jnt = pm.ls(sl=1)
            self.ctrl_list = ctrl_chain(root_jnt, "", self.crv_type, self.color_index, fk_scale, self.check)
            pm.group(root_jnt, n='{}{}setup'.format(self.name, self.infix), w=True)
            pm.delete(self.ref_jnt, self.ref_jntend)
        # if the selection is IK
        if self.type_selection == 1:
            # ik ctrl creation
            self.jnt_chain = self.create_jnt_chain()
            self.create_ik_spline()
            pm.select(pm.listRelatives(self.ref_jnt, children=True, path=True), r=True)
            pm.select(self.ref_jntend, d=True)
            pm.select('{}_iks'.format(self.name), add=True)
            pm.group(n='{}_setup'.format(self.name), w=True)
            pm.group(self.top_start_grp, self.top_end_grp, n='{}_ctrl_setup'.format(self.name))
            pm.delete(self.ref_jnt, self.ref_jntend)
            # strechy option
            self.stretchy = True
            if self.stretchy:
                stretchy(self.name, self.jnt_chain, self.distance)
        # if the selection is IKD
        if self.type_selection == 2:
            self.check = False
            # ik driver ctrl creation
            self.jnt_chain = self.create_jnt_chain()
            pm.select(self.jnt_chain[0], r=1)
            root_jnt = pm.ls(sl=1)
            self.ctrl_list = ctrl_chain(root_jnt, "", self.crv_type, self.color_index, fk_scale, False)
            self.create_ik_spline()
            pm.parent(self.top_start_grp, self.ctrl_list[0])
            pm.parent(self.top_end_grp, self.ctrl_list[int(self.number)-1])
            pm.group(root_jnt, n='{}{}_jnt_setup'.format(self.name, self.infix), w=True)
            pm.select(pm.listRelatives(self.ref_jnt, children=True, path=True), r=True)
            pm.select(self.ref_jntend, d=True)
            pm.select('{}_iks'.format(self.name), add=True)
            pm.group(n='{}{}_setup'.format(self.name, self.infix), w=True)
            pm.delete(self.ref_jnt, self.ref_jntend)
            # strechy option
            self.stretchy = True
            if self.stretchy:
                stretchy(self.name, self.jnt_chain, self.distance)

    def quit_btn_cmd(self, *args):
        """When the quit button is pressed ask the user to close the tool
        :param args:
        :return: None
        """
        answer = pm.confirmDialog(t='Confirmation', b=['Yes', 'No'], m='Do you want to quit?', defaultButton='Yes',
                                  cancelButton='No', dismissString='No')
        if answer == 'Yes':
            pm.deleteUI(self.window, window=True)

    def create_jnt_chain(self, *args):
        """Creates a joint chain from the start loc and end loc. First this creates a start and end joint from the
        locators and use its distance info to get the division value.
        :param args:
        :return: jnt chain array for further use of ctrl chain or ik spline
        """
        jnt_chain = []
        self.ref_jnt = '{}start'.format(self.name)
        self.ref_jntend = '{}end'.format(self.name_end)
        pm.joint(n=self.ref_jnt, p=transformation_info(self.start_loc)['t'])
        pm.joint(n=self.ref_jntend, p=transformation_info(self.end_loc)['t'])
        pm.joint(self.ref_jnt, e=True, zso=True, oj="xyz", sao="yup")
        self.distance = pm.getAttr(self.ref_jntend + ".translateX") / float(self.number)

        def recurse_create_jnt_chain(current_jnt, count):
            """ This is a recursive module for creating a chain of jnts by using the division value.
            :param current_jnt: The source joint to start and use it for orient and parent
            :param count: This is the counter till the number reaches.
            :return: recursive module
            """
            if float(self.number) >= count:
                jnt_name = self.name + self.infix + str(count) + '_jnt'
                jnt_chain.append(jnt_name)
                pm.joint(n=jnt_name)
                orient_node(current_jnt, jnt_name)
                pm.parent(jnt_name, current_jnt)
                if count > 0:
                    pm.xform(jnt_name, t=(self.distance, 0, 0))
                current_jnt = jnt_name
            else:
                return None
            return recurse_create_jnt_chain(current_jnt, count + 1)
        recurse_create_jnt_chain(self.ref_jnt, 0)
        return jnt_chain

    def create_ik_spline(self, *args):
        """ Creates an ik spline with ik ctrls from the start and end locators, with the given selection the names will
        be neck,head and else. This uses the crv type, crv color, locator scale for the ctrl crvs. This uses joints from
         the create_jnt_chain, and makes a spline ik handle with advanced twist attributes for every rotation.
        :param args:
        :return: None
        """
        # create ik handle spline solver
        pm.ikHandle(n='{}_iks'.format(self.name), sj=self.jnt_chain[0], ee=self.jnt_chain[int(self.number)],
                    sol='ikSplineSolver', ns=1, ccv=True)
        # get the name for crv
        ik_crv = '{}_ik_crv'.format(self.name)
        # rename the ik spline handle crv
        pm.rename(pm.listConnections('{}_iks'.format(self.name), t='shape'), ik_crv)
        # select the ik crv
        pm.select(ik_crv, r=True)
        # create a curve info
        crv_info = pm.arclen(ik_crv, ch=True)
        # rename the curve info
        pm.rename(crv_info, '{}_ik_crv_info'.format(self.name))
        # enable advanced twist controls in ik handle
        pm.setAttr('{}_iks.dTwistControlEnable'.format(self.name), 1)
        # more advanced twist option changes
        pm.setAttr('{}_iks.dWorldUpType'.format(self.name), 4)
        # creating the ik ctrls by using the ik_ctrl_wloc module
        start_loc_name, start_ctrl_name, self.top_start_grp = ik_ctrl_wloc(self.name, self.ik_ctrl_s_scale,
                                                                           self.jnt_chain[0], self.crv_type,
                                                                           self.color_index)
        end_loc_name, end_ctrl_name, self.top_end_grp = ik_ctrl_wloc(self.name_end, self.ik_ctrl_e_scale,
                                                                     self.jnt_chain[int(self.number)], self.crv_type,
                                                                     self.color_index)
        pm.connectAttr('{}.worldMatrix[0]'.format(start_loc_name),
                       '{}_iks.dWorldUpMatrix'.format(self.name))
        pm.connectAttr('{}.worldMatrix[0]'.format(end_loc_name),
                       '{}_iks.dWorldUpMatrixEnd'.format(self.name))
        # get the span number form the ik crv spans and degrees
        crv_cv = pm.getAttr(ik_crv + '.spans') + pm.getAttr(ik_crv + '.degree')
        # get the position and create a locator to that position
        for x in range(crv_cv):
            source_node = pm.pointPosition(ik_crv + '.cv[{:d}]'.format(x))
            target_loc = '{}_ik_{:d}_loc'.format(self.name, x)
            loc_grp = create_loc(source_node, target_loc)
            pm.connectAttr(('{}Shape.worldPosition[0]'.format(target_loc)),
                           ('{}Shape.controlPoints[{}]'.format(ik_crv, x)))
            if x < 2:
                loc_grp.setParent(start_ctrl_name)
            else:
                loc_grp.setParent(end_ctrl_name)


def fill_menu(items):
    """ This module is to show necessary menu items
    :param items: This is an array of items
    :return: None
    """
    for i in items:
        pm.menuItem(i, label=i)


def fill_color_palette(color_palette):
    """ This module is to fill the color palette of the UI
    :param color_palette: this is the maya's default colors
    :return: None
    """
    for i in range(1, 32):
        color_component = pm.colorIndex(i, q=True)
        pm.palettePort(color_palette, e=True, rgb=(i, color_component[0], color_component[1], color_component[2]))
    pm.palettePort(color_palette, e=True, rgb=(0, 0.6, 0.6, 0.6))


def custom_crv(crv_type, crv_name, crv_color):
    """ This is a crv type creator by selecting the relevant crv type and override the color of the crv and name it.
    :param crv_type: a specific crv type name to match the relavant crv creation.
    :param crv_name: a name for ctrl crv
    :param crv_color: color of the crv
    :return: ctrl name
    """
    if crv_type == 'cross_crv':
        ctrl_name = pm.curve(n=crv_name, d=1, p=[(0.4, 0, -0.4), (0.4, 0, -2), (-0.4, 0, -2), (-0.4, 0, -0.4),
                                                 (-2, 0, -0.4), (-2, 0, 0.4), (-0.4, 0, 0.4), (-0.4, 0, 2), (0.4, 0, 2),
                                                 (0.4, 0, 0.4), (2, 0, 0.4), (2, 0, -0.4), (0.4, 0, -0.4)],
                             k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    elif crv_type == 'circle_crv':
        ctrl_name = pm.circle(n=crv_name, c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=0)[0]
    elif crv_type == 'cube_crv':
        ctrl_name = pm.curve(n=crv_name, d=1, p=[(0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
                                                 (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5),
                                                 (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, -0.5, 0.5),
                                                 (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5),
                                                 (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5)],
                             k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    elif crv_type == 'sphere_crv':
        ctrl_name = pm.curve(n=crv_name, d=1, p=[(0, 0, 1), (0, 0.5, 0.866025), (0, 0.866025, 0.5), (0, 1, 0),
                                                 (0, 0.866025, -0.5), (0, 0.5, -0.866025), (0, 0, -1),
                                                 (0, -0.5, -0.866025), (0, -0.866025, -0.5), (0, -1, 0),
                                                 (0, -0.866025, 0.5), (0, -0.5, 0.866025), (0, 0, 1),
                                                 (0.707107, 0, 0.707107), (1, 0, 0), (0.707107, 0, -0.707107),
                                                 (0, 0, -1), (-0.707107, 0, -0.707107), (-1, 0, 0), (-0.866025, 0.5, 0),
                                                 (-0.5, 0.866025, 0), (0, 1, 0), (0.5, 0.866025, 0), (0.866025, 0.5, 0),
                                                 (1, 0, 0), (0.866025, -0.5, 0), (0.5, -0.866025, 0), (0, -1, 0),
                                                 (-0.5, -0.866025, 0), (-0.866025, -0.5, 0), (-1, 0, 0),
                                                 (-0.707107, 0, 0.707107), (0, 0, 1)],
                             k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                24, 25, 26, 27, 28, 29, 30, 31, 32])
    elif crv_type == 'rot_180_crv':
        ctrl_name = pm.curve(n=crv_name, d=1, p=[(-0.251045, 0, -1.015808), (-0.761834, 0, -0.979696),
                                                 (-0.486547, 0, -0.930468), (-0.570736, 0, -0.886448),
                                                 (-0.72786, 0, -0.774834), (-0.909301, 0, -0.550655),
                                                 (-1.023899, 0, -0.285854), (-1.063053, 0, 9.80765e-009),
                                                 (-1.023899, 0, 0.285854), (-0.909301, 0, 0.550655),
                                                 (-0.72786, 0, 0.774834), (-0.570736, 0, 0.886448),
                                                 (-0.486547, 0, 0.930468), (-0.761834, 0, 0.979696),
                                                 (-0.251045, 0, 1.015808), (-0.498915, 0, 0.567734),
                                                 (-0.440202, 0, 0.841857), (-0.516355, 0, 0.802034),
                                                 (-0.658578, 0, 0.701014), (-0.822676, 0, 0.498232),
                                                 (-0.926399, 0, 0.258619), (-0.961797, 0, 8.87346e-009),
                                                 (-0.926399, 0, -0.258619), (-0.822676, 0, -0.498232),
                                                 (-0.658578, 0, -0.701014), (-0.516355, 0, -0.802034),
                                                 (-0.440202, 0, -0.841857), (-0.498915, 0, -0.567734),
                                                 (-0.251045, 0, -1.015808)],
                             k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                24, 25, 26, 27, 28])
    elif crv_type == 'rombus_crv':
        ctrl_name = pm.curve(n=crv_name, d=1, p=[(0, 1, 0), (1, 0, 0), (0, 0, 1), (-1, 0, 0), (0, 0, -1), (0, 1, 0),
                                                 (0, 0, 1), (0, -1, 0), (0, 0, -1), (1, 0, 0), (0, 1, 0), (-1, 0, 0),
                                                 (0, -1, 0), (1, 0, 0)],
                             k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
    elif crv_type == 'nail_crv':
        ctrl_name = pm.curve(n=crv_name, d=1, p=[(0, 0, 0), (-2, 0, 0), (-2.292893, 0, 0.707107), (-3, 0, 1),
                                                 (-3.707107, 0, 0.707107), (-4, 0, 0), (-3.707107, 0, -0.707107),
                                                 (-3, 0, -1), (-2.292893, 0, -0.707107), (-2, 0, 0),
                                                 (-2.292893, 0, 0.707107), (-3.707107, 0, -0.707107), (-4, 0, 0),
                                                 (-3.707107, 0, 0.707107), (-2.292893, 0, -0.707107)],
                             k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

    pm.setAttr(crv_name+'Shape.overrideEnabled', 1)
    pm.setAttr(crv_name+'Shape.overrideColor', crv_color)
    return ctrl_name


def orient_node(sel_jnt, sel_node):
    """ Get the node, joint and nodes type which is joint or not to implement reset transformation.
    :param sel_jnt: The selected joint to get the orientation.
    :param sel_node: The selected node to be oriented.
    :return: None
    """
    pm.select(sel_node, r=True)
    node_type = pm.nodeType(str(sel_node))
    pm.parent(sel_node, sel_jnt)
    if node_type == 'joint':
        pm.setAttr(sel_node + '.translateX', 0)
        pm.setAttr(sel_node + '.translateY', 0)
        pm.setAttr(sel_node + '.translateZ', 0)
        pm.setAttr(sel_node + '.jointOrientX', 0)
        pm.setAttr(sel_node + '.jointOrientY', 0)
        pm.setAttr(sel_node + '.jointOrientZ', 0)
    else:
        pm.makeIdentity()
    pm.select(cl=True)


def transformation_info(sel_node):
    """ Gets the translate, rotate, scale and joint orient data (if joint) of the selected node.
    :param sel_node: The selected node.
    :return: transformation array which contains the all translate, rotate, scale and if node is a joint joint orient.
    """
    transformation = {}
    if pm.getAttr(sel_node + '.t'):
        transformation['t'] = pm.getAttr(sel_node + '.t')
    if pm.getAttr(sel_node + '.r'):
        transformation['r'] = pm.getAttr(sel_node + '.r')
    if pm.nodeType(str(sel_node)) == 'joint' and pm.getAttr(sel_node + '.jo'):
        transformation['jo'] = pm.getAttr(sel_node + '.jo')
    if pm.getAttr(sel_node + '.s'):
        transformation['s'] = pm.getAttr(sel_node + '.s')
    return transformation


def ctrl_chain(root, parent, crv_type, crv_color, ctrl_scale, check):
    """ Creates a chain of ctrls from given root jnt till the end jnt which has no more child nodes.
    :param root: The root jnt of the jnt chain
    :param parent: parent ctrl which is going to be the newly created ctrl crv group
    :param crv_type: curve type for create ctrl module
    :param crv_color: curve color for create ctrl module
    :param ctrl_scale: ctrl curve scale for curve size
    :param check: to make a parent constraint between the ctrl curves and weight joints
    :return: ctrl_list collects the ctrl names and returns it for parenting purposes
    """
    ctrl_list = []
    for joint in root:
        child = joint.getChildren(type="joint")
        if child:
            top_grp, ctrl = create_ctrl(joint, crv_type, crv_color, ctrl_scale, None)
            ctrl_list.append(ctrl)
            if check:
                pm.parentConstraint(ctrl, joint, mo=1)
            if parent:
                pm.parent(top_grp, parent)
            ctrl_list += ctrl_chain(child, ctrl, crv_type, crv_color, ctrl_scale, check)
    return ctrl_list


def create_ctrl(source_node, crv_type, crv_color, ctrl_scale, ik_name):
    """ Creates a Ctrl crv with two top groups an offset group and a top group.
    :param source_node: Source node for the orientation of the ctrl crv
    :param crv_type: curve type for custom crv module
    :param crv_color: curve color for custom crv module
    :param ctrl_scale: for curve size
    :param ik_name: it exists ik name changes the name of the ctrl curve
    :return: returns top ctrl curve group and ctrl curve name
    """
    if ik_name:
        name = '{}_ik_ctrl'.format(ik_name)
    else:
        name = '{}ctrl'.format(source_node.split("jnt")[0])
    ctrl_name = custom_crv(crv_type, name, crv_color)
    off = pm.group(n='{}_off'.format(ctrl_name), em=True)
    top = pm.group(off, n='{}_grp'.format(ctrl_name))
    pm.parent(ctrl_name, off)
    pm.xform(top, ro=(0, 0, 90), s=ctrl_scale)
    pm.makeIdentity(top, apply=True)
    orient = pm.parentConstraint(source_node, top, mo=0)
    pm.delete(orient)
    return top, ctrl_name


def create_loc(source_node, target_loc):
    """ Creates a locator to given source nodes position and name it with target_loc
    :param source_node: source node is given to move the locators position
    :param target_loc: name of the locator and locator's group
    :return: locator's group name
    """
    pm.spaceLocator(n=target_loc)
    loc_grp = pm.group(target_loc, n=target_loc+'_grp')
    pm.xform(loc_grp, t=source_node)
    return loc_grp


def ik_ctrl_wloc(name, scale, jnt, crv_type, crv_color):
    """ Creates an IK ctrl curve with locator later be used in advanced twist of the ik spline handle.
    :param name: ik ctrl name for create ctrl module
    :param scale: ctrl crv scale for size of the curve
    :param jnt: source node joint for orientation
    :param crv_type: curve type for create ctrl module
    :param crv_color: curve color for create ctrl module
    :return: locators name from the create loc module, ctrl name from the create ctrl module and top ctrl grp from
    create ctrl module
    """
    top_ctrl_grp, ctrl_name = create_ctrl(jnt, crv_type, crv_color, scale, name)
    loc_name = '{}_upvec_loc'.format(ctrl_name.split("_ctrl")[0])
    loc_grp = create_loc(transformation_info(top_ctrl_grp)['t'], loc_name)
    loc_grp.setParent(ctrl_name)
    return loc_name, ctrl_name, top_ctrl_grp


def stretchy(start_name, jnt_chain, distance):
    """ This is an option for ik systems that they are going to be strechy or not.
    :param start_name: selected ctrl name for the system to be used for all the utilities
    :param jnt_chain: needs for the stretchy direct connection
    :param distance: for the joint chains actual distance between them.
    :return: None
    """
    # curve normalize multd
    pm.shadingNode('multiplyDivide', asUtility=True, name='{}_n_multd'.format(start_name))
    pm.connectAttr('{}_ik_crv_info.arcLength'.format(start_name), '{}_n_multd.i1x'.format(start_name))
    pm.setAttr('{}_n_multd.i2x'.format(start_name), pm.getAttr('{}_ik_crv_info.arcLength'.format(start_name)))
    pm.setAttr('{}_n_multd.operation'.format(start_name), 2)
    # curve all multd
    pm.shadingNode('multiplyDivide', asUtility=True, name='{}_all_multd'.format(start_name))
    pm.group(n='{}_master_scale_grp'.format(start_name), em=True)
    pm.connectAttr('{}_n_multd.ox'.format(start_name), '{}_all_multd.i1x'.format(start_name))
    pm.connectAttr('{}_master_scale_grp.sx'.format(start_name), '{}_all_multd.i2x'.format(start_name))
    pm.setAttr('{}_all_multd.operation'.format(start_name), 2)
    # curve jnt distance multd
    pm.shadingNode('multiplyDivide', asUtility=True, name='{}_dis_multd'.format(start_name))
    pm.connectAttr('{}_all_multd.ox'.format(start_name), '{}_dis_multd.i2x'.format(start_name))
    pm.setAttr('{}_dis_multd.i1x'.format(start_name), distance)
    pm.setAttr('{}_dis_multd.operation'.format(start_name), 1)
    # jnt chain translate x connection
    for x in range(1, len(jnt_chain)):
        pm.connectAttr('{}_dis_multd.ox'.format(start_name), '{}.tx'.format(jnt_chain[x]))


def par_cons(jnt_chain, parent_ctrls):
    """ Parent constraint module between the parent ctrls and joints
    :param jnt_chain: given joint chain array
    :param parent_ctrls: given parent ctrl array
    :return: None
    """
    for x in range(0, len(parent_ctrls)):
        pm.parentConstraint(parent_ctrls[x], jnt_chain[x], mo=True)


def create_avg_point_list(start_point, end_point, division):
    """ This module calculates and returns transformation info between the points and this transformation info is a
    incremental/decremental phase.
    :param start_point: start point
    :param end_point: end point
    :param division: division between the ctrl crvs so the inc/dec phase will be meaningful.
    :return: the point list includes the inc/dec values between the start and end points
    """
    point_list = {}
    trans_info = ['x', 'y', 'z']
    for i in range(len(start_point)):
        s1 = float(start_point[i])
        s2 = float(end_point[i])
        distance = abs((s1 - s2) / division)
        point_list[trans_info[i]] = _average(division, s1, s2, distance)
    return point_list


def _average(division, pt1, pt2, distance):
    """ This recursive module uses the two points and distance to calculate the average points and division is used to
    repetition
    :param division: value for repetition
    :param pt1: first point
    :param pt2: second point
    :param distance: distance value between the points
    :return: returns the average list of the given points
    """
    avg_list = []
    avg_list.append(pt1)

    def rec_average(division, pt1, pt2, distance):
        if division > 0:
            if pt1 > pt2:
                pt1 -= distance
                avg_list.append(pt1)
            elif pt1 < pt2:
                pt1 += distance
                avg_list.append(pt1)
            rec_average(division - 1, pt1, pt2, distance)

    rec_average(division, pt1, pt2, distance)
    return avg_list
