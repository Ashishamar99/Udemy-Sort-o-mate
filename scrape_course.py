# Trying to import and if missing, installing them and importing them.
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

def fetch_text_between_braces(my_string):
	start = '('
	end = ')'
	my_filtered_text = my_string[my_string.find(start)+1 : my_string.find(end)]
	return my_filtered_text

class scrape_course:
	# Deleted course info.
	deleted_course_titles = []
	deleted_course_links = []
	deleted_course_dictionary = {}

	# Existing course info.
	existing_course_titles = []
	existing_course_links = []
	existing_course_ratings = []
	existing_course_total_ratings = []
	existing_course_total_students = []
	existing_course_length = []
	existing_course_dictionary = {}

	def __init__(self):
		pass

	def fetch_link_info(self, filter_rating):
		# Declaring and instantiating deleted course info.
		deleted_course_titles = self.deleted_course_titles
		deleted_course_links = self.deleted_course_links
		deleted_course_dictionary = self.deleted_course_dictionary

		# Declaring and instantiating existing course info.
		existing_course_titles = self.existing_course_titles
		existing_course_links = self.existing_course_links
		existing_course_ratings = self.existing_course_ratings
		existing_course_total_ratings = self.existing_course_total_ratings
		existing_course_total_students = self.existing_course_total_students
		existing_course_length = self.existing_course_length
		existing_course_dictionary = self.existing_course_dictionary

		with open('all_my_links_file.txt', mode = 'r', encoding = 'utf-8') as links_file:
			try:
				for single_link in links_file:
					if 'draft' in single_link:
						deleted_course_titles.append(single_link.split('->')[1])
						deleted_course_links.append(single_link.split('->')[2])
					else:
						#scrape page info, check if rating is >= filter_rating , if it is, then scrape info and keep in list 
						#scrape data - title, rating, total ratings, total students, total time of course length, link
						my_page = requests.get(single_link)
						soup = BeautifulSoup(my_page.content, "lxml")

						course_rating = soup.find(attrs={"data-purpose":"rating-number"}).string #Fetching the course rating.
						course_rating = float(course_rating)
						print(course_rating, type(course_rating)) 

						if filter_rating >= course_rating:
							course_title = soup.h1.string #Fetching the course title.
							total_ratings = soup.find(attrs={"data-purpose":"rating"}).text #Fetching total ratings.
							total_students = soup.find(attrs={"data-purpose":"enrollment"}).text #Fetching total students.
							total_time = soup.find(attrs={"data-purpose":"video-content-length"}).text #Fetching total course length.

							#Appending the scraped data to the lists.
							existing_course_titles.append(course_title)
							existing_course_ratings.append(course_rating)
							existing_course_total_ratings.append(total_ratings)
							existing_course_total_students.append(total_students)
							existing_course_length.append(total_time)
							existing_course_links.append(single_link)

						else:
							pass

			except Exception as e:
				raise Exception

			finally:
				# Creating the dictionaries for existing courses and deleted courses using the scraped data and returning them.
				deleted_course_dictionary = {'Title':deleted_course_titles, 'Link':deleted_course_links}
				existing_course_dictionary = {'Title':existing_course_titles,
											  'Ratings':existing_course_ratings,
									  		  'Total Ratings':existing_course_total_ratings,
									  		  'Total Students':existing_course_total_students,
									  		  'Total Length':existing_course_length,
									  		  'Link':existing_course_links}
				print(deleted_course_dictionary)
				print(existing_course_dictionary)
		return (deleted_course_dictionary, existing_course_dictionary)

class generate_csv():
	def __init__(self, my_deleted_dictionary, my_filtered_courses_dictionary):
		data_frame = pd.DataFrame(my_deleted_dictionary)
		data_frame.to_csv('deleted_courses.csv')

		data_frame = pd.DataFrame(my_filtered_courses_dictionary)
		data_frame.to_csv('my_filtered_courses.csv')

if __name__ == '__main__':
	scrape_course = scrape_course()
	
	filter_rating = float(input('Enter the minimum rating you want the course to be: '))
	print(f'Entered rating is: {filter_rating}')
	deleted_course_dictionary, existing_course_dictionary = scrape_course.fetch_link_info(filter_rating)

	#Dumping the data to csv files
	generate_csv = generate_csv(deleted_course_dictionary, existing_course_dictionary)