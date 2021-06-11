# mode_switch.py
#
# Copyright 2021 adi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GObject, Gdk

class ModeSwitch(Gtk.Grid):
    '''Gtk only basic port of https://github.com/elementary/granite/blob/master/lib/Widgets/ModeSwitch.vala'''

    __gtype_name__ = "ModeSwitch"

    CSS = ".modeswitch slider {min-height: 16px; min-width: 16px;}"
    active = GObject.Property(type=bool, default=True)
    
    def __init__(self, primary_icon_name, secondary_icon_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.primary_icon = Gtk.Image().new_from_icon_name(primary_icon_name, Gtk.IconSize.SMALL_TOOLBAR)
        self.secondary_icon = Gtk.Image().new_from_icon_name(secondary_icon_name, Gtk.IconSize.SMALL_TOOLBAR)
        self.switch = Gtk.Switch()
        self.switch.get_style_context().add_class("modeswitch")

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(self.CSS.encode())
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.primary_icon.connect("button-release-event", self.on_primary_icon_pressed)
        self.secondary_icon.connect("button-release-event", self.on_secondary_icon_pressed)

        self.attach(self.primary_icon, 0, 0, 1, 1)
        self.attach(self.switch, 1, 0, 1, 1)
        self.attach(self.secondary_icon, 2, 0, 1, 1)
        self.props.column_spacing = 2
        self.props.margin_top = 4
        self.props.margin_right = 4

    def on_primary_icon_pressed(self, *args):
        self.active = False
        return Gdk.EVENT_STOP

    def on_secondary_icon_pressed(self, *args):
        self.active = True
        return Gdk.EVENT_STOP