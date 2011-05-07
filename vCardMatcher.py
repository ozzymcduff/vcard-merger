#!/opt/local/bin/python2.5
#!/usr/bin/env python2.5
# encoding: utf-8
"""
vCardMatcher.py

Created by Oskar Gewalli on 2009-09-27.
Copyright (c) 2009 Gewalli. All rights reserved.
"""

import sys
import os
import unittest
import vobject
import re
import StringIO

def find(f, seq):
	"""Return first item in sequence where f(item) == True."""
	for item in seq:
		if f(item): 
			return item
	return None

class vCard:
	def __init__(self,name=""):
		self.name=name
		self.emails=[]
		pass
	
#	def __cmp__(self, other):
#		return vCardHelper.getvCardNames(self).__cmp__( vCardHelper.getvCardNames(other) )
	
	def similarity(self,other):
		return len( vCardHelper.getvCardNames(self) & vCardHelper.getvCardNames(other) )
	
#	def __hash__(self):
#		return vCardHelper.getvCardNames(self).__hash__()
	def __str__(self):
		return u"%(name)s : %(emails)s"%{"name":self.name,"emails":"; ".join(self.emails)}

class vCardWithMatches():
	def __init__(self,vcard):
		self.name   = set(filter(lambda y:len(y)>2,vCardHelper.getWords(vcard.name.lower())))
		self.emails = set(vcard.emails)
		self.apple  = vcard.apple
		#self.vcards = []
		#self.vcards.append(vcard)
	
	def mergevCard(self,vcard):
		self.name.update(set(filter(lambda y:len(y)>2,vCardHelper.getWords(vcard.name.lower()))))
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
			names.update(set(filter(lambda y:len(y)>0, vCardHelper.getPotentialEmailNames(email.lower())) ))
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

class vCardMatcher:
	def __init__(self):
		#^0-9^_^\s^,^\.
		self.nonWordExpr = re.compile(u"[0-9_,\.\s\(\)]+",re.IGNORECASE|re.UNICODE)
		self.firstEmailPart = re.compile(u"([^@]*)@.*")
		self.emailExpr = re.compile(u"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}",re.IGNORECASE|re.UNICODE)
		pass
	
	def getWords(self,input):
		return self.nonWordExpr.split(input)
	
#	def getIntersection(self,x,y):
#		return set(x)&set(y)
	def isEmail(self,input):
		return self.emailExpr.match(input)
		
	def parsevCard(self,x):
		name = unicode( x.n.value ).strip()
		if (self.isEmail(name)):
			name = " ".join(self.getPotentialEmailNames(name))
		v = vCard(name=name)
		
		emailprops = filter(lambda y:y.name=="EMAIL",x.getChildren())
		for email in emailprops:
			v.emails.append( email.value.strip())
		return v
	
	def getPotentialEmailNames(self,x):
		if len(x)==0 : return [] 
		result = self.firstEmailPart.match(x)
		if not result: return []
		return filter(lambda y: len(y)>2,self.nonWordExpr.split(result.group(1)))

	def getvCardNames(self,x):
		try:
			names = set()
			names.update(set(filter(lambda y:len(y)>2,self.getWords(x.name.lower()))))
			if hasattr(x,'emails'):
				for email in x.emails:
					names.update(set(self.getPotentialEmailNames(email.lower()) ))
			if hasattr(x,'email'):
				names.update(set(self.getPotentialEmailNames(x.email.value.lower()) ))
			
			return names
		except:
			print "getvCardNames:"
			print x.name
			print "Unexpected error:", sys.exc_info()[0]
			raise
		
	def LCSubstr_len(self,S, T):
		m = len(S); n = len(T)
		L = [[0] * (n+1) for i in xrange(m+1)]
		lcs = 0
		for i in xrange(m):
			for j in xrange(n):
				if S[i] == T[j]:
					L[i+1][j+1] = L[i][j] + 1
					lcs = max(lcs, L[i+1][j+1])
		return lcs

	def LCSubstr_set(self,S, T):
		m = len(S); n = len(T)
		L = [[0] * (n+1) for i in xrange(m+1)]
		LCS = set()
		longest = 0
		for i in xrange(m):
			for j in xrange(n):
				if S[i] == T[j]:
					v = L[i][j] + 1
					L[i+1][j+1] = v
					if v > longest:
						longest = v
						LCS = set()
					if v == longest:
						LCS.add(S[i-v+1:i+1])
		return LCS

vCardHelper = vCardMatcher()

class vCardMatcherTests(unittest.TestCase):
	def setUp(self):
		self.GooglevCard = "vCard-kort.vcf"
		self.ApplevCard = "contacts.vcf"
		self.tonyExpr= re.compile("Dude",re.IGNORECASE)
		self.rasmusExpr= re.compile("rasmus\shalland",re.IGNORECASE)
		self.matcher = vCardHelper
		
	def testRegexTony(self):
		self.assert_( self.tonyExpr.search("some thing and dude or something else"))
	
	def testReadGooglevCard(self):
		tonyStr = """BEGIN:VCARD
VERSION:3.0
FN:Dude Thedude
N:Thedude;Dude;;;
EMAIL;TYPE=INTERNET:dude.thedude@gmail.com
END:VCARD"""
		x = filter(lambda x:self.tonyExpr.search(unicode(x.n)),\
			vobject.readComponents(StringIO.StringIO(tonyStr)))[0]
		v = self.matcher.parsevCard(x)
		self.assertEqual("Dude  Thedude",v.name)
		self.assertEqual([u"dude.thedude@gmail.com"],v.emails)
		names = self.matcher.getvCardNames(v)
		self.assertEqual(set([u'dude', u'thedude']),names)
			
	def testParseMarie(self):
		x = vobject.readOne(StringIO.StringIO("""BEGIN:VCARD
VERSION:3.0
FN:Syster Mittnamn
N:Mittnamn;Syster;;;
EMAIL;TYPE=INTERNET:asdfadsfjsa@domain.com
NOTE:User 2\: asdfadsfjsa@domain.com\n
END:VCARD
"""))
		card = self.matcher.parsevCard(x)
		self.assertEqual(set(["syster","mittnamn","asdfadsfjsa"]), vCardHelper.getvCardNames(card))
		self.assertEqual(["asdfadsfjsa@domain.com",], card.emails)
	
	def testExtractWords(self):
		self.assertEqual(["test","and","so"],self.matcher.getWords("test and so"))
		
	def testGetIntersection(self):
		self.assertEqual(set(["some","dude"]),\
			set(["test","and","so","some","dude"])&set(["testi","sic","sa","some","dude"]))
	def testgetPotentialEmailNames(self):
		self.assertEqual(["tristan","thedude"], self.matcher.getPotentialEmailNames("tristan.thedude@hotmail.com"))
		self.assertEqual(["some","person"],self.matcher.getPotentialEmailNames("some.person@somedomain.country".lower()))

	def testLCSubstr_set(self):
		self.assertEqual(6, self.matcher.LCSubstr_len("thedude","hedude"))
	
	def testgetvCardNames_NoInput(self):
		vcard = vCard()
		self.assertEqual("",vcard.name)
		self.assertEqual([],vcard.emails)
		self.assertEqual(set([]),self.matcher.getvCardNames(vcard))
	
	def testsimilarity(self):
		vcard = vCard(name="rasmus halland")
		vcard.emails.append("rasmus@thecompany.dk")
		vcard2 = vCard(name="rasmus lolland")
		vcard2.emails.append("halland@lolland.dk")
		self.assertEqual(2,vcard.similarity(vcard2))
	
	def testisEmail(self):
		self.assert_( self.matcher.isEmail("Some.Person@somedomain.country"))
	
	def testMatches(self):
		strErik = """BEGIN:VCARD
VERSION:3.0
FN:null
N:;;;;
EMAIL;TYPE=INTERNET:erik.arnwald@domain.com
END:VCARD
"""
		erikcard=self.matcher.parsevCard(vobject.readOne(StringIO.StringIO(strErik)))
		strErik2 = """BEGIN:VCARD
VERSION:3.0
FN:Lars Erik Gewalli
N:Gewalli hotml;Lars;Erik;;
EMAIL;TYPE=INTERNET:lgewalli@domain.com
NOTE:Phone\\:\\nUser 2\\: lgewalli@domain.com\\n
END:VCARD
"""
		erikcard2=self.matcher.parsevCard(vobject.readOne(StringIO.StringIO(strErik2)))
		self.assertEqual(1, erikcard2.similarity(erikcard))
		strErik3="""BEGIN:VCARD
VERSION:3.0
FN:Erik M
N:Erik;M;;;
END:VCARD"""
		erikcard3=self.matcher.parsevCard(vobject.readOne(StringIO.StringIO(strErik3)))
		#higher similarity is better
		self.assertEqual(1, erikcard3.similarity(erikcard))

		pass
if __name__ == '__main__':
	unittest.main()