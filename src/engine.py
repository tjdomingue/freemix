#!/usr/bin/env python

# Copyright (C) 2008 Luis de Bethencourt
# <luis.debethencourt@sun.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 1, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import gobject
gobject.threads_init() 
import gst

class Engine:
    def __init__(self, filesrc):
        def bus_handler(unused_bus, message):
            if message.type == gst.MESSAGE_ASYNC_DONE:
                if self.first:
                  self.AsyncDone()
                  self.first = False
                  self.pipeline.set_state(gst.STATE_PLAYING)
            if message.type == gst.MESSAGE_SEGMENT_DONE:
                self.SeekToLocation(0)
            if message.type == gst.MESSAGE_ERROR:
                print "ERROR"
            return gst.BUS_PASS

        # create our pipeline
        self.pipeline = gst.Pipeline()
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect ('message', bus_handler)
 
        self.src = gst.element_factory_make("filesrc", "src")
        self.pipeline.add(self.src)
        self.src.set_property("location", filesrc)
        
        self.decodebin = gst.element_factory_make("decodebin", "decodebin")
        self.decodebin.connect("new-decoded-pad", self.OnDynamicPad)
        self.pipeline.add(self.decodebin)
        
        self.src.link(self.decodebin)

        self.colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")

        self.vqueue = gst.element_factory_make("queue", "vqueue")
	self.vqueue.set_property ("max-size-buffers", 3)
        
        self.videoscale = gst.element_factory_make("videoscale", "videoscale")

        self.pipeline.add(self.colorspace, self.vqueue, self.videoscale)

        self.colorspace.link(self.vqueue)
        self.vqueue.link(self.videoscale)
 
	self.imagesink = gst.element_factory_make("ximagesink", "imagesink")
        self.imagesink.set_property("force-aspect-ratio", True)
        self.imagesink.set_property("handle-expose", True)
        self.pipeline.add(self.imagesink)
 
        self.videoscale.link(self.imagesink)

	self.first = True
        self.pipeline.set_state(gst.STATE_PAUSED)

    def OnDynamicPad(self, dbin, pad, islast):
        pad.link(self.colorspace.get_pad("sink"))
        print "OnDynamicPad called"

    def AsyncDone(self):
        print self.pipeline.seek (1.0, gst.FORMAT_TIME, \
            gst.SEEK_FLAG_SEGMENT | gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE, \
            gst.SEEK_TYPE_SET, 0, gst.SEEK_TYPE_NONE, 0)
        print "Async"

    def SeekToLocation(self, location):
        self.pipeline.seek_simple(gst.FORMAT_TIME, \
            gst.SEEK_FLAG_SEGMENT, \
            location)
        print "seek to %r" % location


if __name__ == "__main__":
    engine = Engine("your video file")
    gobject.MainLoop().run()