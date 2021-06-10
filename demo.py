# demo.py
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
from gi.repository import Gtk, GObject, Gdk, cairo, Gio, GLib

from circular_progress_bar import CircularProgressBar
from granite_mode_switch import ModeSwitch

class Demo(Gtk.ApplicationWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header = self.generate_headerbar()
        self.demo_settings = self.generate_demo_settings()
        self.circularprogressbar = CircularProgressBar()
        self.circularprogressbar.props.margin = 6

        color = Gdk.RGBA()
        color.parse(str(self.circularprogressbar.center_fill_color))
        self.colorbutton1.set_rgba(color)
  
        color.parse(str(self.circularprogressbar.radius_fill_color))
        self.colorbutton1.set_rgba(color)

        color.parse(str(self.circularprogressbar.progress_fill_color))
        self.colorbutton3.set_rgba(color)

        self.button_center_filled.bind_property("active", self.circularprogressbar, "center_filled", GObject.BindingFlags.DEFAULT)
        self.button_radius_filled.bind_property("active", self.circularprogressbar, "radius_filled", GObject.BindingFlags.DEFAULT)

        self.colorbutton1.connect("color-set", self.on_color_set)
        self.colorbutton2.connect("color-set", self.on_color_set)
        self.colorbutton3.connect("color-set", self.on_color_set)

        self.button_cap.connect("toggled", self.on_toggled)

        self.s_progr.connect("value-changed", self.on_value_changed)
        self.s_linew.connect("value-changed", self.on_value_changed)

        main_grid = Gtk.Grid()
        main_grid.props.expand = True
        main_grid.attach(self.circularprogressbar, 0, 1, 1, 1)
        main_grid.attach(self.demo_settings, 0, 2, 1, 1)

        self.set_titlebar(self.header)
        self.get_style_context().add_class("rounded")
        self.get_style_context().add_class("tint")
        self.add(main_grid)
        self.props.name = "main"
        self.show_all()

        self.connect("configure-event", self.on_configure_event)
        self.connect("destroy", Gtk.main_quit)

    def generate_headerbar(self):

        modeswitch = ModeSwitch(primary_icon_name="display-brightness-symbolic", secondary_icon_name="weather-clear-night-symbolic")
        gtk_settings = Gtk.Settings().get_default()
        modeswitch.switch.bind_property("active", gtk_settings, "gtk_application_prefer_dark_theme", GObject.BindingFlags.DEFAULT)

        header = Gtk.HeaderBar()
        header.props.name = "main"
        header.props.hexpand = True
        header.props.spacing = 0
        header.props.has_subtitle = False
        header.props.show_close_button = True
        header.props.decoration_layout = "close:"
        header.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)
        header.pack_end(modeswitch)
        return header

    def generate_demo_settings(self):

        self.progr_adj = Gtk.Adjustment()
        self.progr_adj.props.upper = 1
        self.progr_adj.props.step_increment = 0.01
        self.progr_adj.props.page_increment = 10

        self.linew_adj = Gtk.Adjustment()
        self.linew_adj.props.upper = 100
        self.linew_adj.props.value = 1
        self.linew_adj.props.step_increment = 1
        self.linew_adj.props.page_increment = 10

        grid = Gtk.Grid()
        grid.props.visible = True
        grid.props.can_focus = False
        grid.props.halign = Gtk.Align.FILL
        grid.props.valign = Gtk.Align.END
        grid.props.row_spacing = 6
        grid.props.column_spacing = 6
        grid.props.margin = 10

        box = Gtk.Grid()
        box.props.hexpand = False
        box.props.visible = True
        box.props.can_focus = False
        box.props.halign = Gtk.Align.CENTER
        box.props.row_spacing = 6
        box.props.column_spacing = 6

        labelc = Gtk.Label()
        labelc.props.hexpand = True
        labelc.props.can_focus = False
        labelc.props.label = "<b> W x H </b>"
        labelc.props.use_markup = True
        box.attach(labelc, 0, 0, 1, 1)
                  
        self.pbar_w = Gtk.Label()
        self.pbar_w.props.hexpand = True
        self.pbar_w.props.can_focus = False
        self.pbar_w.props.label = "80"
        self.pbar_w.props.use_markup = True
        box.attach(self.pbar_w, 1, 0, 1, 1)

        self.pbar_h = Gtk.Label()
        self.pbar_h .props.hexpand = True
        self.pbar_h .props.can_focus = False
        self.pbar_h .props.label = "80"
        self.pbar_h .props.use_markup = True
        box.attach(self.pbar_h, 2, 0, 1, 1)

        grid.attach(box, 0, 0, 2, 1)

        box0 = Gtk.Grid()
        box0.props.hexpand = True
        box0.props.visible = True
        box0.props.can_focus = False
        box0.props.halign = Gtk.Align.FILL
        box0.props.row_spacing = 6
        box0.props.column_spacing = 6

        self.s_linew = Gtk.Scale()
        self.s_linew.props.name = "s_linew"
        self.s_linew.props.visible = True
        self.s_linew.props.can_focus = True
        self.s_linew.props.hexpand = True
        self.s_linew.props.adjustment = self.linew_adj
        self.s_linew.props.round_digits = 1
        self.s_linew.props.digits = 0
        self.s_linew.props.value_pos = Gtk.PositionType.BOTTOM
        box0.attach(self.s_linew, 1, 0, 2, 1)

        labela = Gtk.Label()
        labela.props.visible = True
        labela.props.can_focus = False
        labela.props.halign = Gtk.Align.START
        labela.props.valign = Gtk.Align.CENTER
        labela.props.label = "Line Width"
        box0.attach(labela, 0, 0, 1, 1)

        grid.attach(box0, 0, 1, 1, 1)

        box1 = Gtk.Grid()
        box1.props.hexpand = True
        box1.props.visible = True
        box1.props.can_focus = False
        box1.props.halign = Gtk.Align.FILL
        box1.props.row_spacing = 6
        box1.props.column_spacing = 6

        self.s_progr = Gtk.Scale()
        self.s_progr.props.name = "s_progr"
        self.s_progr.props.visible = True
        self.s_progr.props.can_focus = True
        self.s_progr.props.hexpand = True
        self.s_progr.props.adjustment = self.progr_adj
        self.s_progr.props.round_digits = 1
        self.s_progr.props.digits = 2
        self.s_progr.props.value_pos = Gtk.PositionType.BOTTOM
        box1.attach(self.s_progr, 1, 1, 2, 1) 

        labelb = Gtk.Label()
        labelb.props.visible = True
        labelb.props.can_focus = False
        labelb.props.halign = Gtk.Align.START
        labelb.props.valign = Gtk.Align.CENTER
        labelb.props.label = "Percentage"
        box1.attach(labelb, 0, 1, 1, 1)

        grid.attach(box1, 0, 2, 1, 1)

        box2 = Gtk.Grid()
        box2.props.hexpand = True
        box2.props.visible = True
        box2.props.can_focus = False
        box2.props.halign = Gtk.Align.FILL
        box2.props.row_spacing = 6
        box2.props.column_spacing = 6

        label1 = Gtk.Label()
        label1.props.hexpand = True
        label1.props.can_focus = False
        label1.props.label = "Center"
        box2.attach(label1, 0, 0, 1, 1)

        label2 = Gtk.Label()
        label2.props.hexpand = True
        label2.props.can_focus = False
        label2.props.label = "Radius"
        box2.attach(label2, 1, 0, 1, 1)

        label3 = Gtk.Label()
        label3.props.hexpand = True
        label3.props.can_focus = False
        label3.props.label = "Progress"
        box2.attach(label3, 2, 0, 1, 1)

        self.button_center_filled = Gtk.ToggleButton()
        self.button_center_filled.props.name = "button_center_filled"
        self.button_center_filled.props.label = "Fill"
        self.button_center_filled.props.hexpand = True
        self.button_center_filled.props.can_focus = True
        self.button_center_filled.props.receives_default = True
        box2.attach(self.button_center_filled, 0, 1, 1, 1)

        self.button_radius_filled = Gtk.ToggleButton()
        self.button_radius_filled.props.name = "button_radius_filled"
        self.button_radius_filled.props.label = "Fill"
        self.button_radius_filled.props.hexpand = True
        self.button_radius_filled.props.can_focus = True
        self.button_radius_filled.props.receives_default = True
        box2.attach(self.button_radius_filled, 1, 1, 1, 1)

        self.button_cap = Gtk.ToggleButton()
        self.button_cap.props.name = "button_cap"
        self.button_cap.props.label = "LineCap"
        self.button_cap.props.hexpand = True
        self.button_cap.props.can_focus = True
        self.button_cap.props.receives_default = True
        box2.attach(self.button_cap, 2, 1, 1, 1)

        self.colorbutton1 = Gtk.ColorButton()
        self.colorbutton1.props.name = "colorbutton1"
        self.colorbutton1.props.hexpand = True
        self.colorbutton1.props.can_focus = True
        self.colorbutton1.props.receives_default = True
        box2.attach(self.colorbutton1, 0, 2, 1, 1)
                
        self.colorbutton2 = Gtk.ColorButton()
        self.colorbutton2.props.name = "colorbutton2"
        self.colorbutton2.props.hexpand = True
        self.colorbutton2.props.can_focus = True
        self.colorbutton2.props.receives_default = True
        box2.attach(self.colorbutton2, 1, 2, 1, 1)

        self.colorbutton3 = Gtk.ColorButton()
        self.colorbutton3.props.name = "colorbutton3"
        self.colorbutton3.props.hexpand = True
        self.colorbutton3.props.can_focus = True
        self.colorbutton3.props.receives_default = True
        box2.attach(self.colorbutton3, 2, 2, 1, 1)

        grid.attach(box2, 0, 3, 2, 1)

        self.fontbutton = Gtk.FontButton().new_with_font("Inter")
        self.fontbutton.props.name = "fontbutton"
        self.fontbutton.props.hexpand = True
        self.fontbutton.props.show_size = True
        self.fontbutton.props.show_style = True
        self.fontbutton.props.use_font = True
        self.fontbutton.props.use_size = True

        grid.attach(self.fontbutton, 0, 4, 2, 1)

        return grid

    def on_color_set(self, colorbutton):
        c = colorbutton.get_rgba()
        if colorbutton.props.name == "colorbutton1":
            self.circularprogressbar.set_property("center_fill_color", c.to_string())
        elif colorbutton.props.name == "colorbutton2":
            self.circularprogressbar.set_property("radius_fill_color", c.to_string())
        elif colorbutton.props.name == "colorbutton3":
            self.circularprogressbar.set_property("progress_fill_color", c.to_string())
        colorbutton.set_tooltip_text(self.convert_rgba_to_webcolor(c))

    def on_toggled(self, togglebutton):
        if togglebutton.props.name == "button_cap":
            if self.circularprogressbar.line_cap == cairo.LineCap.ROUND:
                self.circularprogressbar.set_property("line_cap", cairo.LineCap.BUTT)
            else:
                self.circularprogressbar.set_property("line_cap", cairo.LineCap.ROUND)
            # togglebutton.set_tooltip_text(self.circularprogressbar.line_cap.to_string())

    def on_value_changed(self, scale):
        if scale.props.name == "s_progr":
            self.circularprogressbar.set_property("percentage", scale.get_value())
        if scale.props.name == "s_linew":
            self.circularprogressbar.set_property("line_width", scale.get_value())

    def on_configure_event(self, window, event):
        w = self.circularprogressbar.get_allocated_width()
        h = self.circularprogressbar.get_allocated_height()

        wstr = "{0}".format(w)
        hstr = "{0}".format(h)

        # // The lowest is the indicator of the size
        # // because the widget keeps the aspect ratio

        if w > h:
            hstr = "<b><u>" + hstr + "</u></b>"
        elif h > w:
            wstr = "<b><u>" + wstr + "</u></b>"
        else:
            wstr = "<b><u>" + wstr + "</u></b>"
            hstr = "<b><u>" + hstr + "</u></b>"

        self.pbar_w.set_markup(wstr)
        self.pbar_h.set_markup(hstr)

        self.linew_adj.set_upper(float(min(w, h) / 2))

        return False

    def convert_color_component_to_string(self, color_component):
        return "{0}".format(str(float(color_component * 255)))

    def convert_rgba_to_webcolor(self, c):
        red   = self.convert_color_component_to_string(c.red)
        green = self.convert_color_component_to_string(c.green)
        blue  = self.convert_color_component_to_string(c.blue)
        return "#" + red + green + blue


def main():
    app = Demo()
    Gtk.main()
        
if __name__ == "__main__":    
    main()


