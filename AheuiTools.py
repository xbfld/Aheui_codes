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

class Empty_AheuiCode(ea.AheuiCode):
	def __init__(self, x=0, y=0):
		self.sizex = x
		self.sizey = y
		self.space = [[()]*x]*y
		if self.sizex == 0:
			self.sizex = 1
		if self.sizey == 0:
			self.sizey = 1

def space_to_aheuicode(space, sizex=None, sizey=None):
	acode = Empty_AheuiCode()
	if not space:
		return acode
	acode.space = space
	if not (sizex and sizey):
		sizey = len(space)
		sizex = max([len(line) for line in space])
	acode.sizex = sizex
	acode.sizey = sizey
	return acode

def get_rect_code(acode):
	space = copy.deepcopy(acode.space)
	result = Empty_AheuiCode()
	if not space: return result

	result.sizex = sizex = acode.sizex
	result.sizey = sizey = acode.sizey
	for i in xrange(sizey):
		padl = sizex - len(space[i])
		if padl > 0:
			space[i]+=[()]*padl
	result.space = space
	return result

def flip_lr(acode):
	space = copy.deepcopy(acode.space)
	sizex = acode.sizex
	sizey = acode.sizey
	
	space = [l[::-1] for l in space]
	result = space_to_aheuicode(space, sizex, sizey)
	return result

def flip_ud(acode):
	space = copy.deepcopy(acode.space)
	sizex = acode.sizex
	sizey = acode.sizey
	
	space = space[::-1]
	result = space_to_aheuicode(space, sizex, sizey)
	return result

def rot90(acode, k=1):
	space = copy.deepcopy(acode.space)
	sizex = acode.sizex
	sizey = acode.sizey
	k=k%4
	if k==1:
		sizex = sizey
		sizey = sizex
		space = [list(i) for i in zip(*space)][::-1]
	if k==2:
		space = [line[::-1] for line in space][::-1]
	if k==3:
		sizex = sizey
		sizey = sizex
		space = [list(i)[::-1] for i in zip(*space)]
	result = space_to_aheuicode(space, sizex, sizey)
	return result


def rotate_L(acode):
	space = copy.deepcopy(acode.space)
	sizex = acode.sizey
	sizey = acode.sizex
	
	space = [list(i) for i in zip(*space)][::-1]
	result = space_to_aheuicode(space, sizex, sizey)
	return result

def rotate_R(acode):
	space = copy.deepcopy(acode.space)
	sizex = acode.sizey
	sizey = acode.sizex
	
	space = [list(i)[::-1] for i in zip(*space)]
	result = space_to_aheuicode(space, sizex, sizey)
	return result

def rotate_H(acode):
	space = copy.deepcopy(acode.space)
	sizex = acode.sizex
	sizey = acode.sizey
	
	space = [line[::-1] for line in space][::-1]
	result = space_to_aheuicode(space, sizex, sizey)
	return result

def to_unicode(acode, pad=u'\u3147'):
	#pad U+3147 is ieung
	l=(lambda a,b,c: unichr(a*588+b*28+c+0xac00))
	return '\n'.join(\
		["".join(\
			[l(*char) if char else pad for char in line]\
			) for line in acode.space])

def remove_margin(acode):
	space = copy.deepcopy(acode.space)
	if not space: return Empty_AheuiCode()

	sizex = acode.sizex
	sizey = acode.sizey

	def v(l):#return True if it's emptyrow
		for i in l:
			if i: return False
		return True

	is_empty = True
	for i in xrange(sizey):
		if not v(space[i]):#if i'th row is not emptyrow
			space = space[i:]
			sizey -= i
			is_empty = False
			break
	if is_empty:
		return Empty_AheuiCode()
	while space and v(space[-1]):
		space.pop()
		sizey -= 1

	def h(s,index):#return True if it's emptycloumn
		for l in s:
			if l[index]: return False
		return True

	for i in xrange(sizex):
		if not h(space,i):#if i'th row is not emptycloumn
			space = [line[i:] for line in space]
			sizex -= i
			break
	while space and h(space,-1):
		[line.pop() for line in space]
		sizex -= 1

	result = space_to_aheuicode(space, sizex, sizey)
	return result

def expand_by(acode, t=0, b=0, l=0, r=0):
	space = copy.deepcopy(acode.space)
	sizex = acode.sizex
	sizey = acode.sizey
	if not space:
		sizex = l + r
		sizey = t + b
		if sizex<=0 or sizey<=0:
			raise IndexError('AheuiCode size cannot be negative')
		else:
			space = [[()]*sizex]*sizey
			result = space_to_aheuicode(space, sizex, sizey)
			return result
	sizenx = sizex + l + r
	sizeny = sizey + t + b
	if sizenx<0 or sizeny<0:
		raise IndexError('AheuiCode size cannot be negative')
	elif sizenx==0 or sizeny==0:
		return Empty_AheuiCode()
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

	result = space_to_aheuicode(space, sizex, sizey)
	return result



def main():
	print 'main'
	a=get_rect_code(ea.AheuiCode(u'\n\ns\uac00\ub7a3sss\nss\uafa3\ud7a3ss\n5'))
	print to_unicode(a)
	print a.space
	print a.sizex, a.sizey
	print to_unicode(flip_lr(a))
	print to_unicode(flip_ud(a))
	print to_unicode(rotate_L(a))
	print to_unicode(rotate_R(a))
	print to_unicode(rotate_H(a))
	print to_unicode(remove_margin(a))
	print a.space
	print a.sizex, a.sizey

	print 'main'
	a=get_rect_code(ea.AheuiCode(u'sss\njj'))
	print to_unicode(a)
	print a.space
	print a.sizex, a.sizey
	print to_unicode(flip_lr(a))
	print to_unicode(flip_ud(a))
	print to_unicode(rotate_L(a))
	print to_unicode(rotate_R(a))
	print to_unicode(rotate_H(a))
	print to_unicode(remove_margin(a))
	print a.space
	print a.sizex, a.sizey

	print 'main'
	a=get_rect_code(ea.AheuiCode(u's\n'))
	print to_unicode(a)
	print a.space
	print a.sizex, a.sizey
	print to_unicode(flip_lr(a))
	print to_unicode(flip_ud(a))
	print to_unicode(rotate_L(a))
	print to_unicode(rotate_R(a))
	print to_unicode(rotate_H(a))
	print to_unicode(remove_margin(a))
	print a.space
	print a.sizex, a.sizey

if __name__ == '__main__':
    sys.exit(main())
