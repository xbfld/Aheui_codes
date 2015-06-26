#!/usr/bin/env python
#
# Aheui Editor
# Copyright (c) 2014, Joon Kim
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import sys
import copy
import importlib
ea = importlib.import_module('pyaheui.esotope-aheui')
import AheuiTools as at

import Tkinter as tk

root = tk.Tk()

menubar = tk.Menu(root)

toolfunc=[at.flip_lr, at.flip_ud, at.rotate_L, at.rotate_R, at.rotate_H, at.remove_margin, at.examin_direction]

def new_toolwindow():
	toolwindow = tk.Toplevel(root)
	toolwindow.title('AheuiEditTool')
	toolmenu = tk.Menu(toolwindow)
	text = tk.Text(toolwindow)
	text.pack(expand=True, fill='both')
	def deco(func):
		def tmp():
			v = text.get(1.0,tk.END)
			text.delete(1.0,tk.END)
			text.insert(1.0,at.to_unicode(func(at.get_rect_code(ea.AheuiCode(v)))))
		return tmp
	for func in toolfunc:
		toolmenu.add_command(label=func.__name__, command=deco(func))
	toolwindow.config(menu=toolmenu)


filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Tool", command=new_toolwindow)
filemenu.add_command(label="Exit", command=root.quit)

# display the menu
root.config(menu=menubar)

def main():
	print 'main'
	root.mainloop()

if __name__ == '__main__':
	main()


