# -*- coding: utf-8 -*-
"""
========================================================================================================================
AO Auto Rig v1.0
========================================================================================================================
    Author: Anil Onlem <anilonlem@gmail.com>
    Date: 10-10-2018
    
    Description: This is a working in process auto rig setup which uses a dummy or weight skeleton to create a simple 
        ik fk driven autorig. The updates will revise this code and fix the current faults and simplifies the whole 
        setup and then an UI setup to get a better control of the setup.  
========================================================================================================================
"""
import pymel.core as pm
fkdict = {'Ct_Root_0_JNT': {'scale': (18, 18, 18), 'crv_color': 17, 'crv_type': 'circle_crv'},
          'Ct_Pelvis_0_JNT': {'scale': (18, 18, 18), 'crv_color': 17, 'crv_type': 'circle_crv'},
          'Ct_Spine_0_JNT': {'scale': (18.5, 18.5, 18.5), 'crv_color': 17, 'crv_type': 'circle_crv'},
          'Ct_Spine_1_JNT': {'scale': (19, 19, 19), 'crv_color': 17, 'crv_type': 'circle_crv'},
          'Ct_Spine_2_JNT': {'scale': (19.5, 19.5, 19.5), 'crv_color': 17, 'crv_type': 'circle_crv'},
          'Ct_Spine_3_JNT': {'scale': (20, 20, 20), 'crv_color': 17, 'crv_type': 'circle_crv'},
          'Ct_Chest_0_JNT': {'scale': (20.5, 20.5, 20.5), 'crv_color': 17, 'crv_type': 'circle_crv'},
          'Ct_Neck_0_JNT': {'scale': (10, 10, 10), 'crv_color': 17, 'crv_type': 'circle_crv'},
          'Lf_Clavicle_0_JNT': {'scale': (8, 8, 8), 'crv_color': 17, 'crv_type': 'rot_180_crv'},
          'Rt_Clavicle_0_JNT': {'scale': (8, 8, 8), 'crv_color': 17, 'crv_type': 'rot_180_crv'},
          'Lf_Arm_0_JNT': {'scale': (8, 8, 8), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Arm_1_JNT': {'scale': (8, 8, 8), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Arm_2_JNT': {'scale': (8, 8, 8), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Hand_1_JNT': {'scale': (8, 8, 8), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Arm_0_JNT': {'scale': (8, 8, 8), 'crv_color': 4, 'crv_type': 'circle_crv'},
          'Rt_Arm_1_JNT': {'scale': (8, 8, 8), 'crv_color': 4, 'crv_type': 'circle_crv'},
          'Rt_Arm_2_JNT': {'scale': (8, 8, 8), 'crv_color': 4, 'crv_type': 'circle_crv'},
          'Rt_Hand_1_JNT': {'scale': (8, 8, 8), 'crv_color': 4, 'crv_type': 'circle_crv'},
          'Lf_Thumb_0_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Thumb_1_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Thumb_2_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Index_0_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Index_1_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Index_2_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Index_3_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Middle_0_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Middle_1_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Middle_2_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Middle_3_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Ring_0_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Ring_1_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Ring_2_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Ring_3_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Pinky_0_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Pinky_1_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Pinky_2_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Lf_Pinky_3_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Thumb_0_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Thumb_1_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Thumb_2_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Index_0_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Index_1_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Index_2_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Index_3_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Middle_0_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Middle_1_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Middle_2_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Middle_3_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Ring_0_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Ring_1_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Ring_2_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Ring_3_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Pinky_0_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Pinky_1_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Pinky_2_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'},
          'Rt_Pinky_3_JNT': {'scale': (2, 2, 2), 'crv_color': 15, 'crv_type': 'circle_crv'}
          }


def convert_to_fk(rootnode, suffix='fk_', _parent=None, dict = fkdict):
    """Get the orientation and transformation info of a node(jnt) hierarchy to create a fk ctrl setup with their name
    suffixed.
    Return the newly created root node.
    The new hierarchy will share the same parent as rootnode.

    :param rootnode: str, dummy or weighted joint name
    :param suffix: str, renaming the new joints and control curves
    :param _parent: str, parent of the joint chain
    :param dict: dict, dictionary for the prepared ctrl crv scale and color info
    :return None
    """

    if filter((lambda x: (str(rootnode) == x)), dict.keys()):
        children = pm.listRelatives(rootnode, children=True, path=True) or []
        # Create a fk setup hierarchy from bottom to top joint,joint offset group, control curve, control offset group,
        # control group with the suffixed given name of the node.
        newnode = suffix + rootnode.split("JNT")[0]
        pm.group(pm.joint(n=(newnode + 'JNT')), n=newnode + 'jnt_grp')
        newroot = newnode + 'ctrl'
        jrot = (0, 0, -90)
        jscale = dict[str(rootnode)]['scale']
        crv_color = dict[str(rootnode)]['crv_color']
        crv_type = dict[str(rootnode)]['crv_type']
        custom_crv(crv_type, newroot, crv_color)
        pm.parent((newnode + 'jnt_grp'), newroot)
        con = pm.group(pm.group((newnode + 'ctrl'), n=(newnode + 'ctrl_off')), n=newnode + 'ctrl_grp')
        # Copy the orientation and transformation info to the top group of the newly created control group
        con.setParent(rootnode)
        pm.makeIdentity(con)
        pm.xform(con, ro=jrot, s=jscale)
        pm.makeIdentity(con, apply=True)
        # Set the parent to rootnode's parent if _parent is None.
        # Otherwise set it to _parent.
        if _parent is None:
            _parent = rootnode.getParent()
        con.setParent(_parent)
        pm.select(cl=1)
        # Convert all the children recursively using the newly created control node as a parent.
        for each in children:
            convert_to_fk(each, suffix, newroot, dict=fkdict)
        return newroot


def custom_crv(crv_type, crv_name, crv_color):
    """ This is a crv type creator by selecting the relevant crv type and override the color of the crv and name it.
    :param crv_type: str, a specific crv type name to match the relavant crv creation.
    :param crv_name: str, a name for ctrl crv
    :param crv_color: str, color of the crv
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


def sub_group(name, selected_joint, parent_node, sub_type):
    """
    This module works as a utility to parent, orient node between source and targets
    :param name: str, name of the target
    :param selected_joint: str, joint name for orient info
    :param parent_node: str, parent node to parent the target
    :param sub_type: str, sub_type is for orient node module 't', 'r', 'b'
    :return: None
    """
    pm.select(cl=True)

    def sub_group_base(child_node, sel_jnt, par_node, o_type):
        if not pm.objExists(child_node):
            pm.group(n=child_node, em=True)
        if sel_jnt:
            orient_node(sel_jnt, child_node, o_type)
        if par_node:
            pm.parent(child_node, par_node)
        else:
            pm.parent(child_node, w=True)
    if isinstance(name, list):
        for each in name:
            sub_group_base(each, selected_joint, parent_node, sub_type)
    else:
        sub_group_base(name, selected_joint, parent_node, sub_type)
    pm.select(cl=True)


def orient_node(source_node, target_node, o_type):
    """ Get the node, joint and nodes type which is joint or not to implement reset transformation.
    :param source_node: str, the selected node to be translated and/or oriented.
    :param target_node: str, the selected node to get the translate and/or orient info
    :param o_type: Orientation types 't':translate, 'r':rotate, 'b':both
    :return: None
    """
    pm.select(target_node, r=True)

    def translate_reset(s_node, t_node):
        if (pm.nodeType(str(t_node))) == 'joint':
            pm.setAttr(t_node + '.translateX', 0)
            pm.setAttr(t_node + '.translateY', 0)
            pm.setAttr(t_node + '.translateZ', 0)
        else:
            pm.setAttr(('{}.translate'.format(t_node)), (pm.xform(s_node, q=True, rp=True)))

    def rotate_reset(t_node):
        if (pm.nodeType(str(t_node))) == 'joint':
            pm.setAttr(t_node + '.jointOrientX', 0)
            pm.setAttr(t_node + '.jointOrientY', 0)
            pm.setAttr(t_node + '.jointOrientZ', 0)
        else:
            pm.setAttr(t_node + '.rotateX', 0)
            pm.setAttr(t_node + '.rotateY', 0)
            pm.setAttr(t_node + '.rotateZ', 0)

    pm.parent(target_node, source_node)
    if o_type == 't':
        translate_reset(source_node, target_node)
    if o_type == 'r':
        rotate_reset(target_node)
    if o_type == 'b':
        translate_reset(source_node, target_node)
        rotate_reset(target_node)
    pm.select(cl=True)


def transformation_info(sel_node):
    """ Gets the translate, rotate, scale and joint orient data (if joint) of the selected node.
    :param sel_node: str, the selected node.
    :return: float array, contains the all translate, rotate, scale and if node is a joint joint orient.
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


def create_ctrl(source_node, crv_type, crv_color, ctrl_scale, ik_name):
    """ Creates a Ctrl crv with two top groups an offset group and a top group.
    :param source_node: str, Source node for the orientation of the ctrl crv
    :param crv_type: str, curve type for custom crv module
    :param crv_color: str, curve color for custom crv module
    :param ctrl_scale: float array, curve size
    :param ik_name: str, ik name changes the name of the ctrl curve
    :return: top ctrl curve group and ctrl curve name
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


def create_loc(source_pos, target_loc):
    """ Creates a locator to given source nodes position and name it with target_loc
    :param source_pos: float array, position of the source node
    :param target_loc: str, target loc name
    :return: str, loc_grp locator's group name
    """
    pm.spaceLocator(n=target_loc)
    loc_grp = pm.group(target_loc, n=target_loc+'_grp')
    pm.xform(loc_grp, t=source_pos)
    return loc_grp


def create_jnt_chain(name, ref_jnt, ref_jnt_end, number, suffix):
    """
    This module creates a joint chain by given to points' position and number of the joints in between these.
    :param name: str, base_name of the joints
    :param ref_jnt: str, start reference joint name
    :param ref_jnt_end: str, end reference joint name
    :param number: int, number of the joints in between the ref points
    :param suffix: str, suffix of the joint chain
    :return jnt_chain: str array, array of the newly created joints
    :return distance: float, distance between the ref joints
    """
    jnt_chain = []
    start_jnt = pm.duplicate(ref_jnt, n='{}_ref'.format(ref_jnt), parentOnly=True)[0]
    pm.parent(start_jnt, w=True)
    end_jnt = pm.duplicate(ref_jnt_end, n='{}_ref'.format(ref_jnt_end), parentOnly=True)[0]
    pm.parent(end_jnt, start_jnt)
    pm.joint(start_jnt, e=True, zso=True, oj="xyz", sao="yup")
    distance = pm.getAttr('{}.translateX'.format(end_jnt))/number

    def recurse_jnt_chain(base_name, current_jnt, suf, count):
        if number >= count:
            jnt_name = '{}_{}_{}_jnt'.format(base_name, str(count), suf)
            jnt_chain.append(jnt_name)
            pm.joint(n=jnt_name)
            orient_node(current_jnt, jnt_name, 'b')
            pm.parent(jnt_name, current_jnt)
            if count > 0:
                pm.xform(jnt_name, t=(distance, 0, 0))
            current_jnt = jnt_name
        else:
            return None
        return recurse_jnt_chain(name, current_jnt, suf, count + 1)
    recurse_jnt_chain(name, start_jnt, suffix, 0)
    return jnt_chain, distance


def stretchy(start_name, jnt_chain, distance):
    """ This is an option for ik systems that they are going to be strechy or not.
    :param start_name: str, selected ctrl name for the system to be used for all the utilities
    :param jnt_chain: str array, needs for the stretchy direct connection
    :param distance: float, for the joint chains actual distance between them.
    :return master_scale_name: str, main scale node name
    """
    # curve normalize multd
    pm.shadingNode('multiplyDivide', asUtility=True, name='{}_n_multd'.format(start_name))
    pm.connectAttr('{}_ik_crv_info.arcLength'.format(start_name), '{}_n_multd.i1x'.format(start_name))
    pm.setAttr('{}_n_multd.i2x'.format(start_name), pm.getAttr('{}_ik_crv_info.arcLength'.format(start_name)))
    pm.setAttr('{}_n_multd.operation'.format(start_name), 2)
    # curve all multd
    pm.shadingNode('multiplyDivide', asUtility=True, name='{}_all_multd'.format(start_name))
    master_scale_name = '{}_master_scale_grp'.format(start_name)
    pm.group(n=master_scale_name, em=True)
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
    return master_scale_name


def mid_ik_loc_setup(name, par_node, target):
    """
    This module is creating the mid ik locators' set groups
    :param name: str, name of the groups
    :param par_node: str, parent node
    :param target: str, target node to parent
    :return: None
    """
    old_name = None
    g_name = None
    grp_list = ['_rot_grp', '_crv_grp', '_ik_grp', '_fk_grp', '_off_grp']
    for grp_name in grp_list:
        g_name = '{}{}'.format(name, grp_name)
        if grp_name == '_rot_grp':
            sub_group(g_name, target, par_node, 'b')
        else:
            sub_group(g_name, name, par_node, 'b')
        if old_name:
            sub_group(old_name, None, g_name, None)
        else:
            sub_group(name, None, g_name, None)
        pm.makeIdentity(g_name, apply=True)
        old_name = g_name


def source_joints(start_jnt, end_jnt, except_jnt):
    """
    This module is collect the name of the source joints from start_jnt to end_jnt excludes except_jnt
    :param start_jnt: str, start joint
    :param end_jnt: str, end joint
    :param except_jnt: str, except joint
    :return jnt_list: str array, the list of the chosen joint array
    """
    jnt_list = []
    if pm.nodeType(start_jnt) == 'joint':
        jnt_list.append(start_jnt)

    def recurse_joints(current_jnt, stop_jnt):
        children = pm.listRelatives(current_jnt, children=True, path=True) or []
        for each in children:
            if pm.nodeType(str(each)) == 'joint':
                if not each == except_jnt:
                    if each == stop_jnt:
                        jnt_list.append(str(each))
                    else:
                        jnt_list.append(str(each))
                        recurse_joints(each, stop_jnt)
    recurse_joints(start_jnt, end_jnt)
    return jnt_list


def fk_ik_switch(attr_name):
    """
    This module creates an fk_ik switch ctrl crv and also an attr for selected fk_ik switch
    :param attr_name: str, attribute name for the selected fk ik switch node
    :return: str, attribute values of the default selection and reverse of the selection
    """
    switch_ctrl_name = 'fk_ik_master_switch_ctrl'
    if not pm.objExists(switch_ctrl_name):
        custom_crv('cross_crv', switch_ctrl_name, 4)
        top_grp = pm.group(switch_ctrl_name, n='{}_grp'.format(switch_ctrl_name))
        pm.xform(top_grp, t=(15, 0, 15), s=(3, 3, 3))
        sub_group(top_grp, None, 'main_ctrl', None)
        pm.setAttr('{}.translateX'.format(switch_ctrl_name), lock=True, k=False, cb=False)
        pm.setAttr('{}.translateY'.format(switch_ctrl_name), lock=True, k=False, cb=False)
        pm.setAttr('{}.translateZ'.format(switch_ctrl_name), lock=True, k=False, cb=False)
        pm.setAttr('{}.rotateX'.format(switch_ctrl_name), lock=True, k=False, cb=False)
        pm.setAttr('{}.rotateY'.format(switch_ctrl_name), lock=True, k=False, cb=False)
        pm.setAttr('{}.rotateZ'.format(switch_ctrl_name), lock=True, k=False, cb=False)
        pm.setAttr('{}.scaleX'.format(switch_ctrl_name), lock=True, k=False, cb=False)
        pm.setAttr('{}.scaleY'.format(switch_ctrl_name), lock=True, k=False, cb=False)
        pm.setAttr('{}.scaleZ'.format(switch_ctrl_name), lock=True, k=False, cb=False)
        pm.setAttr('{}.visibility'.format(switch_ctrl_name), lock=True, k=False, cb=False)

    pm.addAttr(switch_ctrl_name, ln='{}_switch'.format(attr_name), at='enum', en='FK:IK:')
    pm.setAttr('{}.{}_switch'.format(switch_ctrl_name, attr_name), e=True, k=True)
    pm.shadingNode('reverse', asUtility=True, name='{}_switch_rev'.format(attr_name))
    pm.connectAttr('{}.{}_switch'.format(switch_ctrl_name, attr_name), '{}_switch_rev.ix'.format(attr_name))
    return '{}.{}_switch'.format(switch_ctrl_name, attr_name), '{}_switch_rev.ox'.format(attr_name)


def jnt_connect(weight_jnts, switch, child_node):
    """
    This module connects the ik, fk joint controls to the weight joints
    :param weight_jnts: str array, the list of the weight joints
    :param switch: str array, the ik fk switch attribute array for direct connection
    :param child_node: str, if exists connects the child node with selection
    :return: None
    """
    if isinstance(weight_jnts, list):
        for wgt in weight_jnts:
            fk_node = 'fk_{}'.format(wgt)
            ik_node = 'ik_{}_con'.format(wgt)
            if pm.objExists(fk_node):
                if pm.objExists(ik_node):
                    parent_cons = pm.parentConstraint(fk_node, ik_node, wgt, mo=True)
                    pm.connectAttr(switch[1], '{}.{}W0'.format(parent_cons, fk_node))
                    pm.connectAttr(switch[0], '{}.{}W1'.format(parent_cons, ik_node))
                else:
                    pm.parentConstraint(fk_node, wgt, mo=True)
    else:
        if child_node:
            parent_cons = pm.parentConstraint('fk_{}'.format(weight_jnts), 'ik_{}_con'.format(weight_jnts), child_node,
                                              mo=True)
            pm.connectAttr(switch[1], '{}.{}W0'.format(parent_cons, 'fk_{}'.format(weight_jnts)))
            pm.connectAttr(switch[0], '{}.{}W1'.format(parent_cons, 'ik_{}_con'.format(weight_jnts)))


def ik_spline_base(name, start_jnt, end_jnt, number, infix):
    """
    This is the base module of the creation of ik spline setup
    :param name: str, name of the ik spline setup
    :param start_jnt: str, name of the start reference joint
    :param end_jnt: str, name of the end reference joint
    :param number: int, numbers of the joint chain
    :param infix: str, infix of the ik spline
    :return: None
    """
    loc_list = []
    points = []
    # create a jnt chain from the start and end jnts with given number and infix
    jnt_chain, distance = create_jnt_chain(name, start_jnt, end_jnt, number, infix)
    # create crv groups for start and end positions
    sub_group('start_crv_grp', jnt_chain[0], None, 'b')
    sub_group('end_crv_grp', jnt_chain[-1], None, 'b')
    points.append(transformation_info('start_crv_grp')['t'])
    points.append(transformation_info('end_crv_grp')['t'])
    # create a curve for ik spline
    pm.curve(n='{}_crv'.format(name), d=1, p=points, k=[0, 1])
    # rebuild it for extra division and spans
    pm.rebuildCurve('{}_crv'.format(name), rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=3, d=3, tol=0.01)
    # curve info
    crv_info = pm.arclen('{}_crv'.format(name), ch=True)
    pm.rename(crv_info, '{}_ik_crv_info'.format(name))
    # curve vector numbers
    crv_cv = pm.getAttr('{}_crv.spans'.format(name)) + pm.getAttr('{}_crv.degree'.format(name))
    # ik spline handle creation
    pm.ikHandle(n='{}_iks'.format(name), sj=jnt_chain[0], ee=jnt_chain[-1], c='{}_crv'.format(name),
                sol='ikSplineSolver', ns=1, ccv=False)
    # extra twist enable
    pm.setAttr('{}_iks.dTwistControlEnable'.format(name), 1)
    pm.setAttr('{}_iks.dWorldUpType'.format(name), 4)
    # strechy jnt chain
    master_scale_grp = stretchy(name, jnt_chain, distance)

    # start ik loc grp for the start position
    start_ik = '{}_{}'.format(name, 0)
    start_ik_loc_grp = '{}_loc_grp'.format(start_ik)
    sub_group(start_ik_loc_grp, 'start_crv_grp', None, 't')

    # end ik loc grp for the end position
    end_ik = '{}_{}'.format(name, crv_cv)
    end_ik_loc_grp = '{}_loc_grp'.format(end_ik)
    sub_group(end_ik_loc_grp, 'end_crv_grp', None, 't')

    # mid ik loc grp for the mid position
    mid_ik = '{}_{}'.format(name, crv_cv/2)
    mid_ik_loc_grp = '{}_loc_grp'.format(mid_ik)
    sub_group(mid_ik_loc_grp, None, None, None)
    sub_group('start_crv_grp', None, mid_ik_loc_grp, None)
    sub_group('end_crv_grp', None, mid_ik_loc_grp, None)
    pm.xform(mid_ik_loc_grp, cp=1)
    pm.parent('start_crv_grp', w=True)
    pm.parent('end_crv_grp', w=True)
    sub_group(mid_ik_loc_grp, 'start_crv_grp', None, 'r')

    # for each curve vector this loops creates a locator to control that cv
    # and extra locators to start and end called up vectors for advanced twist option of the spline ik handle
    for each in range(crv_cv):
        source_pos = pm.pointPosition('{}_crv.cv[{:d}]'.format(name, each))
        target_loc_name = '{}_ik_{:d}_loc'.format(name, each)
        loc_list.append(target_loc_name)
        loc_grp = create_loc(source_pos, target_loc_name)
        pm.connectAttr('{}Shape.worldPosition[0]'.format(target_loc_name),
                       '{}_crvShape.controlPoints[{}]'.format(name, each))
        if each < 2:
            if each is 0:
                start_upvec_loc_name = '{}_ik_upvec_loc'.format(start_jnt)
                start_upvec_loc_grp = create_loc(source_pos, start_upvec_loc_name)
                sub_group(start_upvec_loc_grp, jnt_chain[0], None, 'b')
                pm.connectAttr('{}.worldMatrix[0]'.format(start_upvec_loc_name), '{}_iks.dWorldUpMatrix'.format(name))
            sub_group(loc_grp, None, start_ik_loc_grp, 't')
        elif each > (crv_cv-3):
            if each is (crv_cv-1):
                end_upvec_loc_name = '{}_ik_upvec_loc'.format(end_jnt)
                end_upvec_loc_grp = create_loc(source_pos, end_upvec_loc_name)
                sub_group(end_upvec_loc_grp, jnt_chain[-1], None, 'b')
                pm.connectAttr('{}.worldMatrix[0]'.format(end_upvec_loc_name), '{}_iks.dWorldUpMatrixEnd'.format(name))
            sub_group(loc_grp, None, end_ik_loc_grp, 't')
        else:
            sub_group(loc_grp, 'start_crv_grp', None, 'r')
            mid_ik_loc_setup(target_loc_name, loc_grp, mid_ik_loc_grp)
            sub_group(loc_grp, None, mid_ik_loc_grp, 't')

    # creation of start, mid and end ctrl for the ik spine setup
    start_ctrl_grp, start_ctrl = create_ctrl(start_ik_loc_grp, 'cube_crv', 4, (5, 30, 30), start_ik)
    end_ctrl_grp, end_ctrl = create_ctrl(end_ik_loc_grp, 'cube_crv', 4, (5, 30, 30), end_ik)
    mid_ctrl_grp, mid_ctrl = create_ctrl(mid_ik_loc_grp, 'sphere_crv', 4, (5, 5, 5), mid_ik)

    sub_group('ik_setup_grp', None, 'main_ctrl', None)
    sub_group('spine_ik_handle_grp', None, 'ik_setup_grp', None)
    sub_group(['{}'.format(start_ctrl_grp), '{}'.format(end_ctrl_grp)], None, 'spine_ik_handle_grp', None)
    pm.parentConstraint('Ct_Cog_ctrl_zero', 'spine_ik_handle_grp', mo=True)
    sub_group('ik_spine_jnt_grp', None, 'ik_setup_grp', None)
    sub_group(jnt_chain[0], None, 'ik_spine_jnt_grp', None)
    sub_group(mid_ik_loc_grp, None, 'ik_setup_grp', None)

    sub_group('{}_iks_grp'.format(name), None, 'ik_setup_grp', None)
    sub_group('{}_crv_grp'.format(name), None, None, None)
    sub_group('{}_iks'.format(name), None, '{}_iks_grp'.format(name), None)
    sub_group('{}_crv'.format(name), None, '{}_crv_grp'.format(name), None)
    sub_group(master_scale_grp, None, 'rig_grp', None)
    sub_group('{}_crv_grp'.format(name), None, 'rig_grp', None)

    # parenting the ik loc grps to ik ctrls
    sub_group(start_ik_loc_grp, None, start_ctrl, None)
    sub_group(start_upvec_loc_grp, None, start_ctrl, None)
    sub_group(end_ik_loc_grp, None, end_ctrl, None)
    sub_group(end_upvec_loc_grp, None, end_ctrl, None)
    sub_group('{}_global_scale_grp'.format(mid_ctrl), start_ik_loc_grp, 'ik_setup_grp', 't')
    sub_group('{}_par_grp'.format(mid_ctrl), mid_ik_loc_grp, '{}_global_scale_grp'.format(mid_ctrl), 'b')
    sub_group(mid_ctrl_grp, None, '{}_par_grp'.format(mid_ctrl), None)
    pm.setAttr('{}_off.translateY'.format(mid_ctrl), -30)

    start_par_cons = '{}_par_cons'.format(start_ctrl)
    end_par_cons = '{}_par_cons'.format(end_ctrl)
    sub_group(start_par_cons, 'Spine_ik_2_loc', start_ctrl, 't')
    sub_group(end_par_cons, 'Spine_ik_3_loc', end_ctrl, 't')

    pm.pointConstraint(start_par_cons, end_par_cons, '{}_par_grp'.format(mid_ctrl), mo=True)
    pm.orientConstraint(start_ctrl, end_ctrl, '{}_par_grp'.format(mid_ctrl), mo=True)
    pm.pointConstraint(start_par_cons, '{}_ik_grp'.format(loc_list[2]), mo=True)
    pm.connectAttr('{}.rotateX'.format(mid_ctrl), '{}_rot_grp.rotateX'.format(loc_list[2]))
    pm.connectAttr('{}.rotateZ'.format(mid_ctrl), '{}_rot_grp.rotateZ'.format(loc_list[2]))
    pm.pointConstraint(end_par_cons, '{}_ik_grp'.format(loc_list[3]), mo=True)
    pm.connectAttr('{}.rotateX'.format(mid_ctrl), '{}_rot_grp.rotateX'.format(loc_list[3]))
    pm.connectAttr('{}.rotateZ'.format(mid_ctrl), '{}_rot_grp.rotateZ'.format(loc_list[3]))
    pm.connectAttr('{}.translate'.format(mid_ctrl), '{}_crv_grp.translate'.format(loc_list[2]))
    pm.connectAttr('{}.translate'.format(mid_ctrl), '{}_crv_grp.translate'.format(loc_list[3]))

    pm.scaleConstraint('Spine_master_scale_grp', 'spine_ik_handle_grp')
    pm.scaleConstraint('Spine_master_scale_grp', 'ik_spine_jnt_grp')
    pm.scaleConstraint('Spine_master_scale_grp', '{}_global_scale_grp'.format(mid_ctrl))
    pm.scaleConstraint('main_ctrl', 'Spine_master_scale_grp')

    r_jnt_list = source_joints('Ct_Root_0_JNT', 'Ct_Chest_0_JNT', 'Ct_Pelvis_0_JNT')
    for i, each in enumerate(r_jnt_list, 0):
        ik_con_grp = 'ik_{}_con'.format(each)
        sub_group(ik_con_grp, each, jnt_chain[i], 'b')
        if each is r_jnt_list[-1]:
            sub_group(ik_con_grp, None, end_ctrl, None)

    ik_switch, fk_switch = fk_ik_switch('spine')
    jnt_connect(r_jnt_list, [ik_switch, fk_switch], None)
    jnt_connect('Ct_Chest_0_JNT', [ik_switch, fk_switch], 'fk_chest_grp')

    pm.connectAttr(fk_switch, 'fk_spine_grp.v')
    pm.connectAttr(ik_switch, 'spine_ik_handle_grp.v')
    pm.connectAttr(ik_switch, '{}_global_scale_grp.v'.format(mid_ctrl))

    pm.setAttr('ik_spine_jnt_grp.v', 0)
    pm.setAttr('{}.v'.format(mid_ik_loc_grp), 0)
    pm.setAttr('{}_iks_grp.v'.format(name), 0)
    pm.setAttr('{}_crv_grp.v'.format(name), 0)
    pm.setAttr('{}.v'.format(start_ik_loc_grp), 0)
    pm.setAttr('{}_ik_upvec_loc_grp.v'.format(start_jnt), 0)
    pm.setAttr('{}.v'.format(end_ik_loc_grp), 0)
    pm.setAttr('{}_ik_upvec_loc_grp.v'.format(end_jnt), 0)

    # clean up refs
    pm.delete('start_crv_grp', 'end_crv_grp', '{}_ref'.format(start_jnt))


def dup_jnts(real_joints, prefix):
    """
    This module duplicates the selected joint hierarchy.
    :param real_joints: str array, the list of the real joint hierarchy
    :param prefix: str, prefix for the duplicated joints
    :return: str array, duplicated joint list
    """
    if isinstance(real_joints, list):
        duplicate_joints = []
        first = None
        second = None
        for each in real_joints:
            second = first
            first = pm.duplicate(each, n='{}{}'.format(prefix, each), parentOnly=True)[0]
            duplicate_joints.append(first)
            if second:
                pm.parent(first, second)

    else:
        duplicate_joints = pm.duplicate(real_joints, n='{}{}'.format(prefix, real_joints), parentOnly=True)[0]
    return duplicate_joints


def ik_arm_base(side, start_jnt, end_jnt):
    """
    This module is the base of creation the ik arm setup.
    :param side: str, side string for the arms
    :param start_jnt: str, start joint for the ik arm setup.
    :param end_jnt:  str, end joint for the ik arm setup.
    :return: None
    """
    ik_joints = []
    real_joints = source_joints(start_jnt, end_jnt, None)
    ik_joints = dup_jnts(real_joints, 'ik_')
    parent_arm_jnt = pm.listRelatives(real_joints[0], p=True)[0]
    sub_group('ik_{}_arm_jnt_grp'.format(side), parent_arm_jnt, 'ik_setup_grp', 'b')
    sub_group(ik_joints[0], None, 'ik_{}_arm_jnt_grp'.format(side), None)
    pm.ikHandle(n='ik_{}_arm_iks'.format(side), sj=ik_joints[0], ee=ik_joints[-1], sol='ikRPsolver')

    target_loc_name = 'ik_{}_pv_loc'.format(side)
    sub_group('ik_pv_loc_ref', ik_joints[1], None, 't')
    loc_grp = create_loc(transformation_info('ik_pv_loc_ref')['t'], target_loc_name)
    pm.poleVectorConstraint(target_loc_name, 'ik_{}_arm_iks'.format(side))
    pv_ctrl_grp, pv_ctrl = create_ctrl(target_loc_name, 'rombus_crv', 15, (5, 5, 5), '{}_Pv'.format(side))
    pm.xform(pv_ctrl_grp, r=True, t=(0, 0, -40))
    pm.parent(loc_grp, pv_ctrl)

    sub_group('ik_handle_ref', ik_joints[-1], None, 't')
    ik_handle_ctrl_grp, ik_handle_ctrl = create_ctrl('ik_handle_ref', 'cube_crv', 15, (10, 10, 10),
                                                     '{}_Hand'.format(side))
    pm.parent('ik_{}_arm_iks'.format(side), ik_handle_ctrl)

    for i, each in enumerate(real_joints, 0):
        ik_con_grp = 'ik_{}_con'.format(each)
        sub_group(ik_con_grp, each, ik_joints[i], 'b')

    pm.group('ik_{}_con'.format(real_joints[-1]), n='ik_{}_wrist_off'.format(side))
    sub_group('ik_{}_wrist_off'.format(side), ik_joints[-1], ik_handle_ctrl, 'b')

    pm.addAttr(ik_handle_ctrl, ln="Ulna", at=float, dv=0)
    pm.setAttr('{}.Ulna'.format(ik_handle_ctrl), e=True, k=True)
    pm.connectAttr('{}.Ulna'.format(ik_handle_ctrl), '{}_con.rotateX'.format(ik_joints[-2]))

    ik_switch, fk_switch = fk_ik_switch('{}_arm'.format(side))
    jnt_connect(real_joints, [ik_switch, fk_switch], None)

    ulna_cons = pm.parentConstraint('fk_{}'.format(real_joints[1]), 'ik_{}_con'.format(real_joints[2]),
                                    'fk_{}_Arm_2_ctrl_grp'.format(side), mo=True)
    pm.connectAttr(fk_switch, '{}.{}W0'.format(ulna_cons, 'fk_{}'.format(real_joints[1])))
    pm.connectAttr(ik_switch, '{}.{}W1'.format(ulna_cons, 'ik_{}_con'.format(real_joints[2])))

    pm.parentConstraint(real_joints[-1], 'finger_{}_grp'.format(side), mo=True)

    sub_group(pv_ctrl_grp, None, 'ik_setup_grp', None)
    sub_group(ik_handle_ctrl_grp, None, 'ik_setup_grp', None)
    pm.parentConstraint(parent_arm_jnt, 'ik_{}_arm_jnt_grp'.format(side), mo=True)

    pm.connectAttr(fk_switch, 'fk_{}_Hand_1_ctrl_grp.v'.format(side))
    pm.connectAttr(fk_switch, 'fk_{}_Arm_0_ctrl_grp.v'.format(side))

    pm.connectAttr(ik_switch, '{}.v'.format(ik_handle_ctrl_grp))
    pm.connectAttr(ik_switch, '{}.v'.format(pv_ctrl_grp))

    pm.setAttr('ik_{}_arm_jnt_grp.v'.format(side), 0)
    pm.setAttr('{}.v'.format(loc_grp), 0)
    pm.setAttr('ik_{}_arm_iks.v'.format(side), 0)

    pm.delete('ik_pv_loc_ref', 'ik_handle_ref')


#test part
sel = 'Ct_Root_0_JNT'
pm.select(sel, r=1)
rootnode = pm.ls(sl=1)[0]
pm.select(cl=1)
convert_to_fk(rootnode, 'fk_', None, dict=fkdict)
#additional ctrl crv positioning
pm.select(cl=True)
pm.xform('fk_Lf_Clavicle_0_ctrlShape.cv[0:28]', r=True, ro=(-60, 0, 0))
pm.xform('fk_Lf_Clavicle_0_ctrlShape.cv[0:28]', r=True, t=(-18, 7, -2))
pm.xform('fk_Rt_Clavicle_0_ctrlShape.cv[0:28]', r=True, ro=(120, 0, 0))
pm.xform('fk_Rt_Clavicle_0_ctrlShape.cv[0:28]', r=True, t=(18, -7, 2))
pm.select(cl=True)
sub_group('rig_grp', None, None, None)
# main_ctrl (top ctrl of the rig setup)
pm.circle(n='main_ctrl', nr=(0, 1, 0), ch=False, r=30)
sub_group('main_ctrl_grp', None, 'rig_grp', None)
sub_group('main_ctrl', None, 'main_ctrl_grp', None)
sub_group('fk_setup_grp', None, 'main_ctrl', None)
sub_group('fk_spine_grp', 'Ct_Root_0_JNT', 'fk_setup_grp', 'b')
sub_group('fk_chest_grp', 'Ct_Chest_0_JNT', 'fk_setup_grp', 'b')
sub_group('fk_arm_grp', None, 'fk_setup_grp', None)
sub_group('fk_Ct_Root_0_ctrl_grp', None, 'fk_spine_grp', None)
sub_group(['fk_Lf_Clavicle_0_ctrl_grp', 'fk_Rt_Clavicle_0_ctrl_grp', 'fk_Ct_Neck_0_ctrl_grp'],
          None, 'fk_chest_grp', None)
sub_group(['fk_Lf_Hand_1_ctrl_grp', 'fk_Lf_Arm_0_ctrl_grp', 'fk_Rt_Hand_1_ctrl_grp', 'fk_Rt_Arm_0_ctrl_grp'],
          None, 'fk_arm_grp', None)
pm.parentConstraint('fk_Lf_Clavicle_0_JNT', 'fk_Lf_Arm_0_ctrl_grp', mo=True)
pm.parentConstraint('fk_Lf_Arm_2_JNT', 'fk_Lf_Hand_1_ctrl_grp', mo=True)
pm.parentConstraint('fk_Rt_Clavicle_0_JNT', 'fk_Rt_Arm_0_ctrl_grp', mo=True)
pm.parentConstraint('fk_Rt_Arm_2_JNT', 'fk_Rt_Hand_1_ctrl_grp', mo=True)

sub_group('forearm_setup_grp', None, 'main_ctrl', None)
sub_group('fk_Lf_Arm_2_ctrl_grp', None, 'forearm_setup_grp', None)
sub_group('fk_Rt_Arm_2_ctrl_grp', None, 'forearm_setup_grp', None)
sub_group('wrist_setup_grp', None, 'main_ctrl', None)
sub_group('finger_Lf_grp', 'Lf_Hand_1_JNT', 'wrist_setup_grp', 'b')
sub_group(['fk_Lf_Thumb_0_ctrl_grp', 'fk_Lf_Index_0_ctrl_grp', 'fk_Lf_Middle_0_ctrl_grp', 'fk_Lf_Ring_0_ctrl_grp',
           'fk_Lf_Pinky_0_ctrl_grp'], None, 'finger_Lf_grp', None)
sub_group('finger_Rt_grp', 'Rt_Hand_1_JNT', 'wrist_setup_grp', 'b')
sub_group(['fk_Rt_Thumb_0_ctrl_grp', 'fk_Rt_Index_0_ctrl_grp', 'fk_Rt_Middle_0_ctrl_grp', 'fk_Rt_Ring_0_ctrl_grp',
           'fk_Rt_Pinky_0_ctrl_grp'], None, 'finger_Rt_grp', None)
sub_group('Ct_Cog_jnt', 'Ct_Root_0_JNT', 'main_ctrl', 't')
pm.xform('Ct_Cog_jnt', ro=(0, 0, 90))
cog_ctrl_top, cog_ctrl = create_ctrl('Ct_Cog_jnt', 'cross_crv', 17, (15, 15, 15), None)
pm.makeIdentity(cog_ctrl_top, apply=True, rotate=True)
sub_group('Ct_Cog_ctrl_zero', 'Ct_Cog_jnt', cog_ctrl, 't')
sub_group(cog_ctrl_top, None, 'main_ctrl', None)

pm.parentConstraint('Ct_Cog_ctrl_zero', 'fk_spine_grp', mo=True)

pm.delete('Ct_Cog_jnt')

# IK Setup
# this section is for ik arm and spine setup creation, they are going to use the given jnts orientation info to
# create a ik handles with ik ctrls
pm.select(cl=True)

ik_spline_base('Spine', 'Ct_Root_0_JNT', 'Ct_Chest_0_JNT', 5, 'ik')

ik_arm_base('Lf', 'Lf_Arm_0_JNT', 'Lf_Hand_1_JNT')
ik_arm_base('Rt', 'Rt_Arm_0_JNT', 'Rt_Hand_1_JNT')

# connects the rest of the joints to its fk ctrls
rest_jnt_list = []
for each in source_joints('Ct_Root_0_JNT', None, None):
    if not pm.listConnections(each, d=False, t='parentConstraint', et=True):
        rest_jnt_list.append(each)

jnt_connect(rest_jnt_list, None, None)

sub_group('Ct_Root_0_JNT', None, 'main_ctrl', None)
