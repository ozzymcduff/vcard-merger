#!/opt/local/bin/python2.5
#!/usr/bin/env python2.5
# encoding: utf-8
from vCardMatcher import *

class vCardWithMatches():
	def __init__(self,vcard):
		self.name   = set(filter(lambda y:len(y)>2,getWords(vcard.name.lower())))
		self.emails = set(vcard.emails)
		self.apple  = vcard.apple
	
	def mergevCard(self,vcard):
		self.name.update(set(filter(lambda y:len(y)>2,getWords(vcard.name.lower()))))
		self.apple |= vcard.apple
		self.emails.update(set(vcard.emails))

	def merge(self,other):
		self.name.update(other.name)
		self.apple |= other.apple
		self.emails.update(other.emails)

	def names(self):
		names = set()
		names.update(self.name)
		for email in self.emails:
			names.update(set(filter(lambda y:len(y)>0, getPotentialEmailNames(email.lower())) ))
		return names
		
	def nameContainedInEmail(self,email):
		#if at least two of the names are present in the email, then it is considered contained in the email
		count = 0
		for n in self.name:
			if email.lower().find(n)>=0:
				count +=1
		return count>=2
		
	def nameIsInOthersEmail(self,other):
		for email in other.emails:
			if (self.nameContainedInEmail(email)):
				return True
		return False

	def matches(self,other):
		if len( self.names() & other.names() )>=2 : return True
		
		if len( self.emails & other.emails )>0 : return True
		
		if len(self.name)>=2:
			for email in other.emails: 
				if (self.nameContainedInEmail(email)):
					return True
		elif len(other.name)>=2:
			for email in self.emails: 
				if (other.nameContainedInEmail(email)):
					return True
		
		return False
	
	def __str__(self):
		return u"%(name)s : %(emails)s"%{"name":", ".join(self.name),"emails":"; ".join(self.emails)}