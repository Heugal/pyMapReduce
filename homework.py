#!/usr/bin/python python
import mincemeat
from stopwords import allStopWords
from collections import defaultdict
import os
import string
import sys

global_author_list = []
global_author_word_mapping = {}
global_author_word_reducing = {}
target_authors = sys.argv[1:len(sys.argv)]

def mapfn(file):
	for line in file:
		entry = line.split(':::')
		words = entry[2]
		words = words.translate(None, '.,:()!?\'0123456789')
		author_list = entry[1].split('::')
		new_title = ""
		for title in words.split():
			if title.lower() not in allStopWords:
				new_title = new_title + ' ' + title + ' '
		for author in author_list:
			global_author_word_mapping[author] = new_title.lower()

def reducefn(author):
	long_title = ""
	for author_list, title in global_author_word_mapping.items():
		if author_list == author:
			long_title = long_title + ' ' + title + ' '
	listing = long_title.split()
	d = defaultdict(int)
	for word in listing:
		d[word] = d[word] + 1
	global_author_word_reducing[author] = d
i = 0
output = open('hw_output.txt', 'w')
os.chdir('./hw3data')
for files in os.listdir('.'):
	open_file = open(files, 'r')
	print("Opening file #%d: %s\n" % (i, open_file))
	mapfn(open_file)
	open_file.close()
	i += 1
for new_author in target_authors:
	reducefn(new_author)

output.write(repr(global_author_word_reducing))
output.close()
