#!/opt/local/bin/python2.5
#!/usr/bin/env python2.5
# encoding: utf-8

import sys
import os
import unittest
import vobject
import re
import StringIO


from vcard.vCard import *
from vcard.vCardMatcher import *
from vcard.vCardWithMatches import *

class vCardMatcherTests(unittest.TestCase):
	def setUp(self):
		self.GooglevCard = "vCard-kort.vcf"
		self.ApplevCard = "contacts.vcf"
		self.tonyExpr= re.compile("Dude",re.IGNORECASE)
		self.rasmusExpr= re.compile("rasmus\shalland",re.IGNORECASE)
		
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
		v = parsevCard(x)
		self.assertEqual("Dude  Thedude",v.name)
		self.assertEqual([u"dude.thedude@gmail.com"],v.emails)
		names = getvCardNames(v)
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
		card = parsevCard(x)
		self.assertEqual(set(["syster","mittnamn","asdfadsfjsa"]), getvCardNames(card))
		self.assertEqual(["asdfadsfjsa@domain.com",], card.emails)
	
	def testExtractWords(self):
		self.assertEqual(["test","and","so"],getWords("test and so"))
		
	def testGetIntersection(self):
		self.assertEqual(set(["some","dude"]),\
			set(["test","and","so","some","dude"])&set(["testi","sic","sa","some","dude"]))
	def testgetPotentialEmailNames(self):
		self.assertEqual(["tristan","thedude"], getPotentialEmailNames("tristan.thedude@hotmail.com"))
		self.assertEqual(["some","person"],getPotentialEmailNames("some.person@somedomain.country".lower()))

	def testLCSubstr_set(self):
		self.assertEqual(6, LCSubstr_len("thedude","hedude"))
	
	def testgetvCardNames_NoInput(self):
		vcard = vCard()
		self.assertEqual("",vcard.name)
		self.assertEqual([],vcard.emails)
		self.assertEqual(set([]),getvCardNames(vcard))
	
	def testsimilarity(self):
		vcard = vCardWithMatches(vCard(name="rasmus halland"))
		vcard.emails.add("rasmus@thecompany.dk")
		vcard2 = vCardWithMatches(vCard(name="rasmus lolland"))
		vcard2.emails.add("halland@lolland.dk")
		self.assertTrue(vcard.matches(vcard2))
	
	def testisEmail(self):
		self.assert_( isEmail("Some.Person@somedomain.country"))
	
	def testMatches(self):
		strErik = """BEGIN:VCARD
VERSION:3.0
FN:null
N:;;;;
EMAIL;TYPE=INTERNET:erik.arnwald@domain.com
END:VCARD
"""
		erikcard=vCardWithMatches(parsevCard(vobject.readOne(StringIO.StringIO(strErik))))
		strErik2 = """BEGIN:VCARD
VERSION:3.0
FN:Lars Erik Gewalli
N:Gewalli hotml;Lars;Erik;;
EMAIL;TYPE=INTERNET:lgewalli@domain.com
NOTE:Phone\\:\\nUser 2\\: lgewalli@domain.com\\n
END:VCARD
"""
		erikcard2=vCardWithMatches(parsevCard(vobject.readOne(StringIO.StringIO(strErik2))))
		self.assertFalse(erikcard2.matches(erikcard))
		strErik3="""BEGIN:VCARD
VERSION:3.0
FN:Erik M
N:Erik;M;;;
END:VCARD"""
		erikcard3=vCardWithMatches(parsevCard(vobject.readOne(StringIO.StringIO(strErik3))))
		#higher similarity is better
		self.assertFalse(erikcard3.matches(erikcard))

		pass
if __name__ == '__main__':
	unittest.main()