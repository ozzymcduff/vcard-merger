#!/opt/local/bin/python2.5
#!/usr/bin/env python2.5
# encoding: utf-8
"""
untitled.py

Created by Oskar Gewalli on 2009-08-28.
Copyright (c) 2009 Gewalli. All rights reserved.
"""

import sys
import os
import vobject

from vcard.vCard import *
from vcard.vCardWithMatches import *
import math

def main():
	applelist = []
	for x in vobject.readComponents(file("vCard-kort.vcf")):
		card=parsevCard(x)
		card.apple = True
		applelist.append(vCardWithMatches(card))
	
	googlelist = []
	for x in vobject.readComponents(file("contacts.vcf")):
		card = parsevCard(x)
		card.apple = False
		googlelist.append(vCardWithMatches(card))
	
	
	merged = []
	all = []
	all.extend(applelist)
	all.extend(googlelist)
	for vcard in all:
		match = filter(lambda m:vcard.matches(m),merged)
		if not match:
			merged.append(vcard)
		else:
			match[0].merge(vcard)
			
			if len(match)>1 :
				if (len( match[0].name & match[1].name )>=2 and len(match)<=2):
					match[0].merge(match[1])
					merged.remove(match[1])
				else:
					raise Exception("Length %(l)d > 1, first two elements are %(a)s and %(b)s,"%{"l":len(match),"a":match[0],"b":match[1]})
	
	
	import codecs
	f = codecs.open('result.txt', encoding='utf-16', mode='w+')
	
	
	try:
		for x in merged:
			if (len(x.name)>0 and len(x.emails)>0 and x.apple):
				
				f.write(unicode( u"%(name)s: %(emails)s\n"%{"name":list(x.name), "emails":list(x.emails)}))
			
	finally:
	    f.close()

	
		

if __name__ == '__main__':
	main()
	

