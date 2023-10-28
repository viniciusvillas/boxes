#!/usr/bin/env python3
# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *

class Desksign(Boxes):
    """Simple diagonal plate with stands to show name or mesage"""

    description = """Text to be engraved can be genarated by inputing the label and fontsize fields.
                  height represents the area that can be used for writing text, does not match the actual
                  height when standing. Generated text is put in the center. Currently only a single
                  line of text is supported."""

    ui_group = "Misc"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.addSettingsArgs(edges.StackableSettings, width=2.0) # used for feet

        self.argparser.add_argument(
            "--width",  action="store", type=float, default=150,
            help="plate width in mm (excluding holes)")
        self.argparser.add_argument(
            "--height",  action="store", type=float, default=80,
            help="plate height in mm")
        self.argparser.add_argument(
            "--angle",  action="store", type=float, default=60,
            help="plate angle in degrees (90 is vertical)")
        self.argparser.add_argument(
            "--label", action="store", type=str, default="",
            help="optional text to engrave (leave blank to omit)")
        self.argparser.add_argument(
            "--fontsize", action="store", type=float, default=20,
            help="height of text")
        self.argparser.add_argument(
            "--feet", action="store", type=boolarg, default=False,
            help="add raised feet")
        self.argparser.add_argument(
            "--mirror", action="store", type=boolarg, default=True,
            help="mirrors one of the stand so the same side of the material can be placed on the outside")

    def render(self):
        width = self.width
        height = self.height
        angle = self.angle
        feet = self.feet
        mirror = self.mirror
        t = self.thickness

        if not (0 < angle and angle < 90):
            raise ValueError("angle has to between 0 and 90 degrees")

        base =  math.cos(math.radians(angle)) * height
        h = math.sin(math.radians(angle)) * height

        label = self.label
        fontsize = self.fontsize

        if label and fontsize:
            self.rectangularWall(width, height, "eheh", move="right", callback=[
                lambda: self.text("%s" % label, width/2, (height-fontsize)/2,
                    fontsize = fontsize, align="center", color=Color.ETCHING)]) # add text
        else:
            self.rectangularWall(width, height, "eheh", move="right") # front
        
        # stands at back/side
        edge = "šef" if feet else "eef"
        if mirror:
            self.rectangularTriangle(base, h, edge, num=1, move="right")
            self.rectangularTriangle(base, h, edge, num=1, move="mirror right")
        else:
            self.rectangularTriangle(base, h, edge, num=2, move="right")
