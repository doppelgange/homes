#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import urllib2  
import re

def get_house_attribute(url):
	response = urllib2.urlopen(url)
	house_page_html = response.read()

	house_title = re.search('<h1 id="ListingTitle_title">(.*)[\s\S]*<\/h1>', house_page_html)
	if house_title:
	    print 'Title : ',house_title.group(1)
    
	house_list_date = re.search('Listed: (.*?)<', house_page_html)
	if house_list_date:
	    print 'List Date : ',house_list_date.group(1)
	
	house_attributes = re.findall('<th id="ListingAttributes_AttributesRepeater.*?ltHeaderRow">\s*(.*?):\s*<\/th>\s*<td>\s*(.*)\s*<\/td>', house_page_html)
	if house_attributes:
		for house_attribute in house_attributes:
			print re.sub("<.*?>", "", house_attribute[0]),': ',re.sub("(<.*?>)|(\&.*?;)|(This week's open homes in Lower Hutt)", "", house_attribute[1])




def get_ref_price(url):
	print url
	response = urllib2.urlopen(url)
	house_page_html = response.read()
	prices = re.findall('<li>\s*(.*?)\s*\&ndash;\s*(.*)\s*<\/li>', house_page_html)
	r=[]
	if prices:
		for price in prices:
			r.append(re.sub("\$|,", "", price[0])+','+re.sub("\r", "", price[1]))
		print r
		if r:
			return r
		else:
			return ''

def get_url_list(page):
	url = 'http://www.trademe.co.nz/browse/categoryattributesearchresults.aspx?cid=5748&search=1&v=list&nofilters=1&originalsidebar=1&134=15&135=46&rptpath=350-5748-3399-&key=1338944751&sort_order=expiry_desc&page=%d' % page
	response = urllib2.urlopen(url)  
	html = response.read()  
	links = re.findall('/property/residential-property-for-sale/.*?.htm', html)
	# print '\n'.join(map(str, links))
	return links

# get_house_attribute('http://www.trademe.co.nz/property/residential-property-for-sale/auction-988008326.htm')
f_ref = open('ref_price.txt', 'w+')
f_houses = open('houses.txt', 'w+')

for page in (1,2,3):
	for link in get_url_list(page):
		# response = urllib2.urlopen('http://www.trademe.co.nz/'+link)
		link ='http://www.trademe.co.nz'+link
		f_ref.write(get_ref_price(link))
		# f_houses.write(get_house_attribute(link))

f_ref.close()
f_houses.close()
