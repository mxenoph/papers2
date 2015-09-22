#! /bin/env python

import re
import io

from papers2.schema import Papers2
db = Papers2()

f = open(u'references.bib', 'w')

for ind, pub in enumerate(db.get_publications()):
	print pub.citekey
	authors = pub.full_author_string.split(',')
	formatted_authors = ''
	for i, au in enumerate(authors):
		if i == (len(authors)-1):
			au = re.sub(r' and ', '', au)
		au = re.sub(r'^\s', '', au)
		au = au.split(' ')
		first_name = ' '.join(au[:-1])
		last_name = au[-1]
		au =  ', '.join([last_name, first_name])
		if i == 0:
			formatted_authors = au
		else:
			formatted_authors = ' and '.join([formatted_authors, au])
	pattern = re.compile('(\d+)\s*vol.\s*(\d+)\s*\((\d+)\)\s*pp.(.*)$')
	matching = pattern.match(pub.publication_string)
	if matching:
		year, volume, number, pages = matching.groups()
		pages = re.sub(r'-', '--', pages)
#		title = re.sub(r'\xa0', '', title)
		print >>f, '@articel{%s,\n author={%s},\n title={{%s}},\n journal={%s},\n year={%s},\n volume={%s},\n number={%s},\n pages={%s}\n}\n' % (pub.citekey, formatted_authors, title, pub.bundle_string, year, volume, number, pages)
	else:
		print 'No information on year of publication etc'

f.close()
