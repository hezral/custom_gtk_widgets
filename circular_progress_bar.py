# circular_progress_bar.py
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
gi.require_version('PangoCairo', '1.0')
from gi.repository import Gtk, GObject, Gdk, cairo, PangoCairo, Pango

import math

class CircularProgressBar(Gtk.Bin):
    '''Python port of https://github.com/phastmike/vala-circular-progress-bar'''
    MIN_D = 80
    font = "Inter"
    line_cap = cairo.LineCap.BUTT

    _line_width = 1
    _percentage = 0.0
    _center_fill_color = "#adadad"
    _radius_fill_color = "#d3d3d3"
    _progress_fill_color = "#4a90d9"

    center_filled = GObject.Property(type=bool, default=False)
    radius_filled = GObject.Property(type=bool, default=False)
    font = GObject.Property(type=str, default="Inter")
    line_cap = GObject.Property(type=cairo.LineCap, default=cairo.LineCap.BUTT)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        drawing_area = Gtk.DrawingArea()
        drawing_area.set_size_request(300, 300)
        drawing_area.props.expand = True
        drawing_area.props.halign = self.props.valign = Gtk.Align.FILL

        drawing_area.connect("draw", self.draw)
        self.connect("notify", self.on_notify)

        self.add(drawing_area)

    def on_notify(self, *args):
        self.queue_draw()

    @GObject.Property(type=str)
    def center_fill_color(self):
        '''Center pad fill color (Check Gdk.RGBA parse method)'''
        return self._center_fill_color

    @center_fill_color.setter
    def center_fill_color(self, value):
        color = Gdk.RGBA()
        if color.parse(value):
            self._center_fill_color = value

    @GObject.Property(type=str)
    def radius_fill_color(self):
        '''The circular pad fill color (Check GdkRGBA parse method)'''
        return self._radius_fill_color

    @radius_fill_color.setter
    def radius_fill_color(self, value):
        color = Gdk.RGBA()
        if color.parse(value):
            self._radius_fill_color = value

    @GObject.Property(type=str)
    def progress_fill_color(self):
        '''Progress line color (Check GdkRGBA parse method)'''
        return self._progress_fill_color

    @progress_fill_color.setter
    def progress_fill_color(self, value):
        color = Gdk.RGBA()
        if color.parse(value):
            self._progress_fill_color= value

    @GObject.Property(type=int)
    def line_width(self):
        '''The circle radius line width'''
        return self._line_width

    @line_width.setter
    def line_width(self, value):
        if value < 0:
            self._line_width = 0
        else:
            self._line_width = value

    @GObject.Property(type=float)
    def percentage(self):
        '''The percentage value [0.0 ... 1.0]'''
        return self._percentage

    @percentage.setter
    def percentage(self, value):
        if value > 1.0:
            self._percentage = 1.0
        elif value < 0.0:
            self._percentage = 0.0
        else:
            self._percentage = float(value)

    def calculate_radius(self):
        return int(min(self.get_allocated_width() / 2, self.get_allocated_height() / 2) - 1)

    def calculate_diameter(self):
        return int(2 * self.calculate_radius())

    def do_get_request_mode(self):
        return Gtk.SizeRequestMode.CONSTANT_SIZE

    def do_get_preferred_width(self):
        d = self.calculate_diameter()
        min_w = self.MIN_D
        if d > self.MIN_D:
            natural_w = d
        else:
            natural_w = self.MIN_D
        return min_w, natural_w

    def do_get_preferred_height(self):
        d = self.calculate_diameter()
        min_h = self.MIN_D
        if d > self.MIN_D:
            natural_h = d
        else:
            natural_h = self.MIN_D
        return min_h, natural_h

    def draw(self, widget, cr):

        cr.save()

        color = Gdk.RGBA()

        center_x = self.get_allocated_width() / 2
        center_y = self.get_allocated_height() / 2
        radius =  self.calculate_radius()

        if radius - self.line_width < 0:
            delta = 0
            self.set_property("line_width", radius)
        else:
            delta = radius - (self.line_width / 2)

        color = Gdk.RGBA()

        cr.set_line_cap(self.line_cap)
        cr.set_line_width(self.line_width)

        # Center Fill
        if self.center_filled:
            cr.arc(center_x, center_y, delta, 0, 2 * math.pi)
            color.parse(self.center_fill_color)
            Gdk.cairo_set_source_rgba(cr, color)
            cr.fill()

        # Radius Fill
        if self.radius_filled:
            cr.arc(center_x, center_y, delta, 0, 2 * math.pi)
            color.parse(self.radius_fill_color)
            Gdk.cairo_set_source_rgba(cr, color)
            cr.stroke()

        # Progress/Percentage Fill
        if self.percentage > 0:
            color.parse(self.progress_fill_color)
            Gdk.cairo_set_source_rgba(cr, color)

            if self.line_width == 0:
                cr.move_to(center_x, center_y)
                cr.arc(center_x, center_y, delta+1, 1.5 * math.pi, (1.5 + self.percentage * 2 ) * math.pi)
                cr.fill()
            else:
                cr.arc(center_x, center_y, delta, 1.5 * math.pi, (1.5 + self.percentage * 2 ) * math.pi)
                cr.stroke()

        # Textual information
        context = self.get_style_context()
        context.save()
        context.add_class(Gtk.STYLE_CLASS_TROUGH)
        color = context.get_color(context.get_state())
        Gdk.cairo_set_source_rgba(cr, color)

        # Percentage
        layout = PangoCairo.create_layout(cr)
        layout.set_text("{0}".format(int(self.percentage * 100.0)), -1)
        desc = Pango.FontDescription.from_string(self.font + " 24")
        layout.set_font_description(desc)
        PangoCairo.update_layout(cr, layout)
        w, h = layout.get_size() 
        cr.move_to(center_x - ((w / Pango.SCALE) / 2), center_y - 27 )
        PangoCairo.show_layout(cr, layout)

        # Units indicator ('PERCENT')
        layout.set_text("PERCENT", -1)
        desc = Pango.FontDescription.from_string(self.font + " 8")
        layout.set_font_description(desc)
        PangoCairo.update_layout(cr, layout)
        w, h = layout.get_size()
        cr.move_to(center_x - ((w / Pango.SCALE) / 2), center_y + 13)
        PangoCairo.show_layout(cr, layout)

        context.restore()
        cr.restore()
