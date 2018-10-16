"""
module for control curve shapes and colors
"""

import pymel.core as pm


class Curve:
    """
    class for building curve shapes and colors
    """

    def __init__(self,
                 curve_type,
                 curve_color,
                 curve_name
                 ):
        """
        :param curve_type: str, curve shape types for selection
        :param curve_color: str, curve colors
        :param curve_name: str, curve name
        :return None
        """
        self.curve_type = curve_type
        self.curve_color = curve_color
        self.curve_name = curve_name
        self.ctrl_name = None
        self.color_dict = {'yellow': 17, 'red': 4, 'blue': 15}

    def type(self):
        """
        module for creating the selected curve type with selected color otherwise both will be default
        :return self.ctrl_name: str, the created ctrl curves name
        """
        if self.curve_type == 'cross':
            self.ctrl_name = pm.curve(n='{}_ctrl'.format(self.curve_name), d=1,
                                      p=[(0.4, 0, -0.4), (0.4, 0, -2), (-0.4, 0, -2), (-0.4, 0, -0.4), (-2, 0, -0.4),
                                         (-2, 0, 0.4), (-0.4, 0, 0.4), (-0.4, 0, 2), (0.4, 0, 2), (0.4, 0, 0.4),
                                         (2, 0, 0.4), (2, 0, -0.4), (0.4, 0, -0.4)],
                                      k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
            self.color()
        elif self.curve_type == 'cube':
            self.ctrl_name = pm.curve(n='{}_ctrl'.format(self.curve_name), d=1,
                                      p=[(0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5),
                                         (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5),
                                         (0.5, 0.5, 0.5), (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5),
                                         (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5)],
                                      k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
            self.color()
        elif self.curve_type == 'sphere':
            self.ctrl_name = pm.curve(n='{}_ctrl'.format(self.curve_name), d=1,
                                      p=[(0, 0, 1), (0, 0.5, 0.866025), (0, 0.866025, 0.5), (0, 1, 0),
                                         (0, 0.866025, -0.5),
                                         (0, 0.5, -0.866025), (0, 0, -1), (0, -0.5, -0.866025), (0, -0.866025, -0.5),
                                         (0, -1, 0), (0, -0.866025, 0.5), (0, -0.5, 0.866025), (0, 0, 1),
                                         (0.707107, 0, 0.707107), (1, 0, 0), (0.707107, 0, -0.707107), (0, 0, -1),
                                         (-0.707107, 0, -0.707107), (-1, 0, 0), (-0.866025, 0.5, 0),
                                         (-0.5, 0.866025, 0),
                                         (0, 1, 0), (0.5, 0.866025, 0), (0.866025, 0.5, 0), (1, 0, 0),
                                         (0.866025, -0.5, 0),
                                         (0.5, -0.866025, 0), (0, -1, 0), (-0.5, -0.866025, 0), (-0.866025, -0.5, 0),
                                         (-1, 0, 0), (-0.707107, 0, 0.707107), (0, 0, 1)],
                                      k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                                         22,
                                         23, 24, 25, 26, 27, 28, 29, 30, 31, 32])
            self.color()
        elif self.curve_type == 'rot_180':
            self.ctrl_name = pm.curve(n='{}_ctrl'.format(self.curve_name), d=1,
                                      p=[(-0.251045, 0, -1.015808), (-0.761834, 0, -0.979696),
                                         (-0.486547, 0, -0.930468),
                                         (-0.570736, 0, -0.886448), (-0.72786, 0, -0.774834), (-0.909301, 0, -0.550655),
                                         (-1.023899, 0, -0.285854), (-1.063053, 0, 9.80765e-009),
                                         (-1.023899, 0, 0.285854),
                                         (-0.909301, 0, 0.550655), (-0.72786, 0, 0.774834), (-0.570736, 0, 0.886448),
                                         (-0.486547, 0, 0.930468), (-0.761834, 0, 0.979696), (-0.251045, 0, 1.015808),
                                         (-0.498915, 0, 0.567734), (-0.440202, 0, 0.841857), (-0.516355, 0, 0.802034),
                                         (-0.658578, 0, 0.701014), (-0.822676, 0, 0.498232), (-0.926399, 0, 0.258619),
                                         (-0.961797, 0, 8.87346e-009), (-0.926399, 0, -0.258619),
                                         (-0.822676, 0, -0.498232),
                                         (-0.658578, 0, -0.701014), (-0.516355, 0, -0.802034),
                                         (-0.440202, 0, -0.841857),
                                         (-0.498915, 0, -0.567734), (-0.251045, 0, -1.015808)],
                                      k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                                         22,
                                         23, 24, 25, 26, 27, 28])
            self.color()
        elif self.curve_type == 'rombus':
            self.ctrl_name = pm.curve(n='{}_ctrl'.format(self.curve_name), d=1,
                                      p=[(0, 1, 0), (1, 0, 0), (0, 0, 1), (-1, 0, 0), (0, 0, -1), (0, 1, 0), (0, 0, 1),
                                         (0, -1, 0), (0, 0, -1), (1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0),
                                         (1, 0, 0)],
                                      k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
            self.color()
        elif self.curve_type == 'nail':
            self.ctrl_name = pm.curve(n='{}_ctrl'.format(self.curve_name), d=1,
                                      p=[(0, 0, 0), (-2, 0, 0), (-2.292893, 0, 0.707107), (-3, 0, 1),
                                         (-3.707107, 0, 0.707107), (-4, 0, 0), (-3.707107, 0, -0.707107), (-3, 0, -1),
                                         (-2.292893, 0, -0.707107), (-2, 0, 0), (-2.292893, 0, 0.707107),
                                         (-3.707107, 0, -0.707107), (-4, 0, 0), (-3.707107, 0, 0.707107),
                                         (-2.292893, 0, -0.707107)],
                                      k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
            self.color()
        else:
            self.curve_type = 'circle'
            self.ctrl_name = pm.circle(n='{}_ctrl'.format(self.curve_name), c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3,
                                       ut=0, tol=0.01, s=8, ch=0)[0]
            self.color()
        # print 'curve_type:{}'.format(self.curve_type)
        # print 'ctrl_name:{}'.format(self.ctrl_name)
        return self.ctrl_name

    def color(self):
        """
        module for overwrite the color of the curve shape within the given color_dict
        :return: None
        """
        ctrl_shape = pm.listRelatives(self.ctrl_name, s=1)[0]
        if self.curve_color in self.color_dict:
            pm.setAttr('.ove'.format(ctrl_shape), 1)
            pm.setAttr('.ovc'.format(ctrl_shape), self.color_dict[self.curve_color])
            # print 'curve_color:{}'.format(self.curve_color)
        else:
            print 'this is a new color or not even a color.'
