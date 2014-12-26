#!/usr/bin/env python
#
# Aheui Editor
# Copyright (c) 2014, Joon Kim.
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

class AheuiCodeBlock(object):

	def __init__(self, acode):
		acode = copy.deepcopy(acode)
		if isinstance(acode, unicode):
			acode = ea.AheuiCode(acode)
		if not isinstance(acode, ea.AheuiCode):
			acode = ea.AheuiCode(str(acode).encode('utf-8'))
		self.block = self.make_rect_block(acode)

	def make_rect_block(self, acode):
		sizex = acode.sizex
		space = acode.space
		if not space: return acode
		for i in xrange(acode.sizey):
			padl = sizex - len(space[i])
			if padl > 0:
				space[i]+=[()]*padl
		acode.space = space
		return acode

	def flip_h(self, acode):
		space = acode.space
		for line in space:
			line.reverse()
		return acode
	def flip_v(self, acode):
		acode.space.reverse()
		return acode

	def rotate_L(self, acode):
		acode.sizey, acode.sizex = acode.sizex, acode.sizey
		space = acode.space
		acode.space = [list(i) for i in zip(*space)][::-1]
		return acode

	def rotate_R(self, acode):
		acode.sizey, acode.sizex = acode.sizex, acode.sizey
		space = acode.space
		acode.space = [list(i)[::-1] for i in zip(*space)]
		return acode

	def rotate_H(self, acode):
		space = acode.space
		acode.space = [line[::-1] for line in space][::-1]
		return acode

	def get_unicode(self, acode, pad=u'\u3147'):
		l=(lambda a,b,c: unichr(a*588+b*28+c+0xac00))
		return '\n'.join(\
			["".join([l(*char) if char else pad for char in line\
				]) for line in acode.space])

	make_rect_block = classmethod(make_rect_block)
	flip_h = classmethod(flip_h)
	flip_v = classmethod(flip_v)
	rotate_L = classmethod(rotate_L)
	rotate_R = classmethod(rotate_R)
	rotate_H = classmethod(rotate_H)
	get_unicode = classmethod(get_unicode)



def main():
	a=AheuiCodeBlock(u'\uac00\ub7a3s\ns\uafa3\ud7a3')
	print a.block.space
	AheuiCodeBlock.flip_h(a.block)
	print a.block.space
	AheuiCodeBlock.flip_v(a.block)
	print a.block.space
	AheuiCodeBlock.rotate_L(a.block)
	print a.block.space
	AheuiCodeBlock.rotate_R(a.block)
	print a.block.space
	AheuiCodeBlock.rotate_H(a.block)
	print a.block.space
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	print a.block.space

if __name__ == '__main__':
    sys.exit(main())


