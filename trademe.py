#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import urllib2  
import re
import MySQLdb
import time
from re import sub
from decimal import Decimal
########################################################################################################
# Connect to database

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  # your password
                     db="homes")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

########################################################################################################



def get_house_attribute(url):
	response = urllib2.urlopen(url)
	house_page_html = response.read()

	house = {}
	house_title = re.search('<h1 id="ListingTitle_title">(.*)[\s\S]*<\/h1>', house_page_html)
	if house_title:
		house['headline'] = re.sub("(\r)|(\&.*?;)", "",house_title.group(1))
	    #print 'Title : ',house_title.group(1)
    
	house_list_date = re.search('Listed: (.*?)<', house_page_html)
	if house_list_date:
		house['list_date'] = house_list_date.group(1)
	    #print 'List Date : ',house_list_date.group(1)
	
	house_agent = re.search('redirect=http%3a%2f%2fwww\.(.*?)\.', house_page_html)
	if house_agent:
		house['agent'] = house_agent.group(1)
	    #print 'List Date : ',house_agent.group(1)


	house_attributes = re.findall('<th id="ListingAttributes_AttributesRepeater.*?ltHeaderRow">\s*(.*?):\s*<\/th>\s*<td>\s*(.*)\s*<\/td>', house_page_html)
	if house_attributes:
		for house_attribute in house_attributes:
			# print house_attribute[0]
			# print house_attribute[1]
			house[re.sub(" ", "_", re.sub("<.*?>", "", house_attribute[0])).lower()] = re.sub("(<.*?>)|(\r)|(\&.*?;)|(This week's open homes in Lower Hutt)|(View Open Home Planner)|(Save to my Open Home Planner)", "", re.sub("<br ?/>", ", ", house_attribute[1]))
			#print re.sub("<.*?>", "", house_attribute[0]),': ',re.sub("(<.*?>)|(\&.*?;)|(This week's open homes in Lower Hutt)", "", re.sub("<br ?/>", ", ", house_attribute[1]))
			if  house_attribute[0] == "Rooms":
				house_rooms = re.search('(\d)\s*?bedrooms?,\s(\d)\sbathroom', house_attribute[1])
				if house_rooms:
					house['bedrooms'] = house_rooms.group(1)
					house['bathrooms'] = house_rooms.group(2)

	if 'rateable_value_(rv)' in house:
		a = 0
	else:
		house['rateable_value_(rv)'] = "$0.0"


	house_desc = re.search('class="ListingDescription">\s*(.*?)\s*<\/div>', house_page_html)
	if house_desc:
		house['description'] = re.sub("(\r)|(<.*?>)|(\&.*?;)", " ",house_desc.group(1))

	house_agent_ref = re.search('Agency reference #:\s*(.*?)\s', house_page_html)
	if house_agent_ref:
		house['agent_ref'] = house_agent_ref.group(1)
	
	return house


# Get the sales price
def get_trademe_sold_prices(url):
	print url
	response = urllib2.urlopen(url)
	house_page_html = response.read()
	prices = re.findall('<li>\s*(.*?)\s*\&ndash;\s*(.*)\s*<\/li>', house_page_html)
	print "prices is "
	print prices 
	r=[]
	if prices:
		for price in prices:
			r.append(re.sub("\$|,", "", price[0])+','+re.sub("\r", "", price[1]))
		if r:
			return r
		else:
			return ''

# Get trade me url list using given search criteria
def get_trademe_urls(page):
	url = 'http://www.trademe.co.nz/Browse/CategoryAttributeSearchResults.aspx?search=1&cid=5748&sidebar=1&132=PROPERTY&selected135=46&selected136=1618%2C2123%2C2118%2C1767%2C1654%2C1619%2C1448%2C1415%2C1766%2C924%2C1449&134=15&135=46&136=1618&136=2123&136=2118&136=1767&136=1654&136=1619&136=1448&136=1415&136=1766&136=924&136=1449&216=0&216=0&217=0&217=0&153=&122=0&122=0&123=0&123=0&49=0&49=0&178=0&178=0&sidebarSearch_keypresses=0&sidebarSearch_suggested=0'
	url += '&page=%d' % page
	response = urllib2.urlopen(url)  
	html = response.read()  

	#links = re.findall('/property/residential-property-for-sale/.*?.htm', html)
	links = re.findall('dotted" href="(.*?)">',html)
	return links












for page in (1,2):
	home_list = get_trademe_urls(page)
	print home_list
	print "Total", len(home_list),"houses in this page."
	exit()
	print list(set(get_trademe_urls(page)))
	exit()
	for link in get_trademe_urls(page):
		# response = urllib2.urlopen('http://www.trademe.co.nz/'+link)
		# Get the single url 
		link ='http://www.trademe.co.nz'+link

		# Get data from the selling house
		new_selling_home =  get_house_attribute(link)
		
		add_home = ("INSERT INTO homes "
               "(full_address, bathrooms, bedrooms, rv, recent_sold, list_date, agent,agent_ref, headline, description, method) "
               "VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s,%s, %s)")

		# INSERT INTO `homes` (`id`, `uuid`, `full_address`, `latitude`, `longitude`, `bathrooms`, `bedrooms`, `car_space`, `homes_ev`, `rv`, `land_value`, `improvement_value`, `land_area`, `floor_area`, `decade_built`, `recent_sold`, `remarks`, `list_date`, `sold_date`, `sold_price`, `open2view_url`, `agent`, `agent_url`, `agent_ref`, `headline`, `description`, `legal_desc`, `rates`, `chattles`, `method`, `qv_url`, `trademe_url`, `google_street_view_url`, `street`, `suburb`, `state`, `postcode`, `updated_at`)
		# VALUES
		# (1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2016-04-03 23:23:08');
		
		try:
			home_data = (
				new_selling_home['location'],
				new_selling_home['bathrooms'],
				new_selling_home['bedrooms'],
				Decimal(sub(r'[^\d.]', '', new_selling_home['rateable_value_(rv)'])),
				0,
				time.strftime('2016-%m-%d',time.strptime(new_selling_home['list_date'], "%a %d %b, %I:%M %p")),
				new_selling_home['agent'],
				new_selling_home['agent_ref'],
				new_selling_home['headline'],
				new_selling_home['description'],
				new_selling_home['price']
			)
		except KeyError as e:
			print "*****************************************************************"
			print e
			print page
			print link
			print "*****************************************************************"
			
		# cur.execute(add_home,home_data)
		# db.commit()

		# exit()

		# # Get data from reference houses
		# trademe_sold_prices = get_trademe_sold_prices(link)




