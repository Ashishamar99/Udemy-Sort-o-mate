"""
ZOMBIE CODE ->
# import re

>>> char1 = '('
>>> char2 = ')'
>>> mystr = "mystring(123234sample)"
>>> print mystr[mystr.find(char1)+1 : mystr.find(char2)]
123234sample



>>> import re
>>> mystr
'mystring->123234sample->'
>>> findsub='->'
>>> res = [i.start() for i in re.finditer(findsub,mystr)]
>>> res
[8, 22]
>>> mystr[8:22]
'->123234sample'
>>> mystr[8+2:22+2]
'123234sample->'
>>> mystr[8+2:22]
'123234sample'
"""
for import_tries in range(0,2):
	try:
		from bs4 import BeautifulSoup
		import requests
		import os
		import pandas as pd
		import re
	except ImportError:
		os.system('pip install beautifulsoup4')
		os.system('pip install requests')
		os.system('pip install pandas')

class scrape_course:
	# deleted course info 
	deleted_course_titles = []
	deleted_course_links = []
	deleted_course_dictionary = {}

	#existing course info
	existing_course_titles = []
	existing_course_links = []
	existing_course_ratings = []
	existing_course_total_ratings = []
	existing_course_total_students = []
	existing_course_length = []
	existing_course_dictionary = {}

	def __init__(self):
		pass

	def fetch_deleted_link_info(self):
		deleted_course_titles = self.deleted_course_titles
		deleted_course_links = self.deleted_course_links
		deleted_course_dictionary = self.deleted_course_dictionary

		with open('all_my_links_file.txt', mode = 'r', encoding = 'utf-8') as links_file:
			for single_link in links_file:
				if 'draft' in single_link:
					deleted_course_titles.append(single_link.split('->')[1])
					deleted_course_links.append(single_link.split('->')[2])
				else:
					pass

		deleted_course_dictionary = {'Title':deleted_course_titles, 'Link':deleted_course_links}
		return deleted_course_dictionary

	def fetch_existing_course_link_info(self, filter_rating):
		existing_course_titles = self.existing_course_titles
		existing_course_links = self.existing_course_links
		existing_course_ratings = self.existing_course_ratings
		existing_course_total_ratings = self.existing_course_total_ratings
		existing_course_total_students = self.existing_course_total_students
		existing_course_length = self.existing_course_length
		existing_course_dictionary = self.existing_course_dictionary

		with open('all_my_links_file.txt', mode = 'r', encoding = 'utf-8') as links_file:
			for single_link in links_file:
				if 'draft' in single_link:
					pass
				else:
					#scrape page info, check if rating is >= filter_rating , if it is, then scrape info and keep in list 
					#scrape title, rating, total ratings, total students, total time of course length, link
					pass
		return existing_course_dictionary

class generate_csv():
	def __init__(self, my_deleted_dictionary, my_filtered_courses_dictionary):
		data_frame = pd.DataFrame(my_deleted_dictionary)
		data_frame.to_csv('deleted_courses.csv')

		data_frame = pd.DataFrame(my_filtered_courses_dictionary)
		data_frame.to_csv('my_filtered_courses.csv')

if __name__ == '__main__':
	scrape_course = scrape_course()
	
	deleted_course_dictionary = scrape_course.fetch_deleted_link_info()
	filter_rating = float(input('Enter the minimum rating you want the course to be: '))
	print(filter_rating)
	existing_course_dictionary = scrape_course.fetch_existing_course_link_info(filter_rating)

	#Dumping the data to csv files
	generate_csv = generate_csv(deleted_course_dictionary, existing_course_dictionary)