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

	EMPTYAHEUICODE = ea.AheuiCode('')

	def __init__(self, acode):
		acode = copy.deepcopy(acode)
		if isinstance(acode, unicode):
			acode = ea.AheuiCode(acode)
		if not isinstance(acode, ea.AheuiCode):
			acode = ea.AheuiCode(str(acode).encode('utf-8'))
		self.block = self.make_rect_block(acode)

	# def space_to_aheuicode(cls, space):

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

	def remove_margin(self, acode):
		space = acode.space
		if not space: return acode

		sizex = acode.sizex
		sizey = acode.sizey

		def v(l):#return True if it's emptyrow
			for i in l:
				if i: return False
			return True

		is_empty = True
		for i in xrange(acode.sizey):
			if not v(space[i]):
				space = space[i:]
				sizey -= i
				is_empty = False
				break
		if is_empty:
			acode.space = self.EMPTYAHEUICODE.space
			acode.sizex = self.EMPTYAHEUICODE.sizex
			acode.sizey = self.EMPTYAHEUICODE.sizey
			return acode
		while space and v(space[-1]):
			space.pop()
			sizey -= 1

		def h(s,index):#return True if it's emptycloumn
			for l in s:
				if l[index]: return False
			return True

		for i in xrange(acode.sizex):
			if not h(space,i):
				space = [line[i:] for line in space]
				sizex -= i
				is_empty = False
				break
		while space and h(space,-1):
			[line.pop() for line in space]
			sizex -= 1

		acode.space = space
		acode.sizex = sizex
		acode.sizey = sizey
		return acode

	def expand_by(self, acode, t=0, b=0, l=0, r=0):
		space = acode.space
		sizex = acode.sizex
		sizey = acode.sizey
		if not space:
			sizex = l + r
			sizey = t + b
			if sizex<=0 or sizey<=0:
				raise IndexError('AheuiCode size cannot be negative')
			else:
				acode.space = [[()]*sizex]*sizey
				acode.sizex = sizex
				acode.sizey = sizey
				return acode
		sizenx = sizex + l + r
		sizeny = sizey + t + b
		if sizenx<0 or sizeny<0:
			raise IndexError('AheuiCode size cannot be negative')
		elif sizenx==0 or sizeny==0:
			acode.space = self.EMPTYAHEUICODE.space
			acode.sizex = self.EMPTYAHEUICODE.sizex
			acode.sizey = self.EMPTYAHEUICODE.sizey
			return acode
		if t>=0:
			space = [[()]*sizex]*t + space
			if b>=0:
				space += [[()]*sizex]*b
			else:
				space = space[:b]
		else:
			if b>=0:
				space += [[()]*sizex]*b
			else:
				space = space[:b]
			space = space[-t:]
		if l>=0:
			space = [[()]*l+line for line in space]
			if r>=0:
				space = [line+[()]*r for line in space]
			else:
				space = [line[:r] for line in space]
		else:
			if r>=0:
				space = [line+[()]*r for line in space]
			else:
				space = [line[:r] for line in space]
			space = [line[-l:] for line in space]

		acode.space = space
		acode.sizex = sizenx
		acode.sizey = sizeny

		return acode

	# def union(self, acode1, acode2, xpos, ypos):
	# 	if xpos>=0 and ypos>=0






	make_rect_block = classmethod(make_rect_block)
	flip_h = classmethod(flip_h)
	flip_v = classmethod(flip_v)
	rotate_L = classmethod(rotate_L)
	rotate_R = classmethod(rotate_R)
	rotate_H = classmethod(rotate_H)
	get_unicode = classmethod(get_unicode)
	remove_margin = classmethod(remove_margin)
	expand_by = classmethod(expand_by)



def main():
	print 'main'
	a=AheuiCodeBlock(u'\n\ns\uac00\ub7a3sss\nss\uafa3\ud7a3ss\n5')
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	print a.block.space
	print a.block.sizex, a.block.sizey
	AheuiCodeBlock.flip_h(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.flip_v(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.rotate_L(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.rotate_R(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.rotate_H(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.remove_margin(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	print a.block.space
	print a.block.sizex, a.block.sizey

	print 'main'
	a=AheuiCodeBlock(u'sss\njj')
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	print a.block.space
	print a.block.sizex, a.block.sizey
	AheuiCodeBlock.flip_h(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.flip_v(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.rotate_L(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.rotate_R(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.rotate_H(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.remove_margin(a.block)
	print a.block.space
	print a.block.sizex, a.block.sizey

	print 'main'
	a=AheuiCodeBlock(u's\n')
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	print a.block.space
	print a.block.sizex, a.block.sizey
	AheuiCodeBlock.flip_h(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.flip_v(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.rotate_L(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.rotate_R(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.rotate_H(a.block)
	print AheuiCodeBlock.get_unicode(a.block, u'\u3147')
	AheuiCodeBlock.remove_margin(a.block)
	print a.block.space
	print a.block.sizex, a.block.sizey

if __name__ == '__main__':
    sys.exit(main())


