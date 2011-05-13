#!/opt/local/bin/python2.5
#!/usr/bin/env python2.5
# encoding: utf-8

from vcard.vCardMatcher import *

class vCard:
	def __init__(self,name=""):
		self.name=name
		self.emails=[]
		self.apple=False
		pass
	
	def __str__(self):
		return u"%(name)s : %(emails)s"%{"name":self.name,"emails":"; ".join(self.emails)}
		
def parsevCard(x):
	"""Parses a vobject to a simplified vCard."""
	name = unicode( x.n.value ).strip()
	if (isEmail(name)):
		name = " ".join(getPotentialEmailNames(name))
	v = vCard(name=name)

	emailprops = filter(lambda y:y.name=="EMAIL",x.getChildren())
	for email in emailprops:
		v.emails.append( email.value.strip())
	return v
