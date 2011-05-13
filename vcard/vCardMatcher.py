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
import re
import StringIO

def find(f, seq):
	"""Return first item in sequence where f(item) == True."""
	for item in seq:
		if f(item): 
			return item
	return None

nonWordExpr = re.compile(u"[0-9_,\.\s\(\)]+",re.IGNORECASE|re.UNICODE)
firstEmailPart = re.compile(u"([^@]*)@.*")
emailExpr = re.compile(u"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}",re.IGNORECASE|re.UNICODE)
	
def getWords(input):
	return nonWordExpr.split(input)

def isEmail(input):
	return emailExpr.match(input)
	
def getPotentialEmailNames(x):
	if len(x)==0 : return [] 
	result = firstEmailPart.match(x)
	if not result: return []
	return filter(lambda y: len(y)>2,nonWordExpr.split(result.group(1)))

def getvCardNames(x):
	try:
		names = set()
		names.update(set(filter(lambda y:len(y)>2,getWords(x.name.lower()))))
		if hasattr(x,'emails'):
			for email in x.emails:
				names.update(set(getPotentialEmailNames(email.lower()) ))
		if hasattr(x,'email'):
			names.update(set(getPotentialEmailNames(x.email.value.lower()) ))
		
		return names
	except:
		print "getvCardNames:"
		print x.name
		print "Unexpected error:", sys.exc_info()[0]
		raise
	
def LCSubstr_len(S, T):
	m = len(S); n = len(T)
	L = [[0] * (n+1) for i in xrange(m+1)]
	lcs = 0
	for i in xrange(m):
		for j in xrange(n):
			if S[i] == T[j]:
				L[i+1][j+1] = L[i][j] + 1
				lcs = max(lcs, L[i+1][j+1])
	return lcs

def LCSubstr_set(S, T):
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


