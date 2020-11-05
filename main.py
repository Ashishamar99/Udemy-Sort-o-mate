from data import username, login_link, password, courses_link_sorted
import time
from itertools import zip_longest as zp
from scrape_course import scrape_course, generate_csv

# Trying to import modules, if missing then install them and import them again.
for import_tries in range(0,2):
	try:
		from selenium import webdriver
		from selenium.common.exceptions import NoSuchElementException
		import os
	except ImportError:
		os.system('pip install selenium')

class init_driver():
	# Init function only initializes the the driver instance.
	def __init__(self):
		path_to_edge_driver = 'C:\\Users\\Ashish\\Desktop\\Codes For Fun\\Py Automation\\edgedriver_win64\\msedgedriver.exe'
		self.driver = webdriver.Edge(path_to_edge_driver)

class account(init_driver):
	all_courses_links = []
	deleted_course_links = {}
	existing_course_links = []
	image_to_details_dict = {}

	def perform_login(self):
		driver = self.driver
		driver.implicitly_wait(10)
		driver.get(login_link)
		#NOTE: USED XPATH HERE.
		driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div[1]/div/input').send_keys(username) #Sending username to the textbox
		driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div[2]/div/input').send_keys(password) #Sending password to the textbox
		driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div[2]/div/input').click() #Clicking login button
		time.sleep(5)

	def check_login_status(self):
		try:
			self.page = str(1) 
			driver = self.driver
			logged_in_username = driver.find_element_by_class_name('udlite-heading-md')
			driver.implicitly_wait(5)
			driver.get(courses_link_sorted + self.page)
			print('Login Successful')
			time.sleep(5)
		except NoSuchElementException as login_error:
			print(str(login_error))
			print('Login Unsuccessful')

	def fetch_page_number(self):
		driver = self.driver
		#NOTE: USED XPATH HERE.
		total_pages = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/ul/li/div[4]/div/ul/li[7]/a').text
		return total_pages

	def fetch_all_pages(self, total_pages):
		all_pages_list = []
		for page_number in range(1, total_pages):
			all_pages_list.append(courses_link_sorted + str(page_number))
		return all_pages_list

	def scrape_courses_links(self, all_pages_list):
		driver = self.driver
		all_courses_links = self.all_courses_links
		existing_course_links = self.existing_course_links
		deleted_course_links = self.deleted_course_links
		image_to_details_dict = self.image_to_details_dict

		for page in all_pages_list:
			driver.implicitly_wait(5)
			driver.get(page)
			print("Scraping:: " + page)
			#NOTE: USED CLASS NAMES HERE.
			my_course_links = driver.find_elements_by_class_name('card--learning__details')
			my_course_image_links = driver.find_elements_by_class_name('card--learning__image')
			my_course_title_elements = driver.find_elements_by_css_selector('strong.details__name')

			for my_course,image_link,course_title_element in list(zp(my_course_links,my_course_image_links,my_course_title_elements)):
				my_link = my_course.get_attribute('href')
				one_image_link = image_link.get_attribute('href')
				my_course_title = course_title_element.text
				image_to_details_dict[one_image_link] = my_link
				all_courses_links.append(my_link)
				if 'draft' in my_link:
					deleted_course_links[my_course_title] = my_link
					print(my_link, 'is deleted')
				else:
					existing_course_links.append(my_link)

		driver.quit()
		return all_courses_links,deleted_course_links,existing_course_links,image_to_details_dict

if __name__ == '__main__':
	# Perform login and load courses page as well as sort them in alphabetical order.
	my_account = account()
	
	my_account.perform_login()
	my_account.check_login_status()
	page = my_account.fetch_page_number()
	all_pages_list = my_account.fetch_all_pages(int(page) + 1)
	all_courses_links,deleted_course_links,existing_course_links,image_to_details_dict = my_account.scrape_courses_links(all_pages_list)

	"""Start Dev
 	Some random code to check if everything works. """
	file_count = 0
	my_file_counter = []
	for file in os.listdir():
		if 'final_mainop' in file:my_file_counter.append(int(file.split('.')[0][::-1][0]))
		else:pass
	file_count = max(my_file_counter)

	with open(f'final_mainop_v{file_count + 1}.txt', mode = 'w', encoding = 'utf-8') as print_op:
		print_op.write('\n------------------All Courses------------------\n')
		print_op.write(f'{all_courses_links}\t Length = {len(all_courses_links)}')
		print_op.write('\n------------------Deleted Courses------------------\n')
		print_op.write(f'{str(deleted_course_links)}\t Length = {len(deleted_course_links)}')
		print_op.write('\n------------------Existing Courses------------------\n')
		print_op.write(f'{existing_course_links}\t Length =  {len(existing_course_links)}')
		print_op.write(f'\nTotal courses length = {len(all_courses_links)}\nAdded Length = {len(deleted_course_links)+len(existing_course_links)}')
		print_op.write('\n------------------Total Dictionary------------------\n')
		print_op.write(f'{str(image_to_details_dict)}\t Length = {len(image_to_details_dict)}')

	"""Stop Dev"""

	# all_my_links_file = open('all_my_links_file.txt', mode = 'w', encoding = 'utf-8')
	with open('all_my_links_file.txt', mode = 'w', encoding = 'utf-8') as file:
		if len(all_courses_links) == (len(deleted_course_links)+len(existing_course_links)):
			for one_course_link in all_courses_links:
				if 'draft' in one_course_link:
					for one_deleted_link in deleted_course_links:
						file.write(f'Title -> {one_deleted_link} -> {deleted_course_links[one_deleted_link]}' )
						file.write('\n')
				else:
					file.write(one_course_link[::-1][:5:-1])
					file.write('\n')
		else:
			file.write('Existing Links --> \n')
			for one_existing_link in existing_course_links:
				file.write(one_existing_link)
				file.write('\n')

			file.write('Deleted Links --> \n')
			for one_deleted_link in deleted_course_links:
				file.write(f'Title -> {one_deleted_link} -> {deleted_course_links[one_deleted_link]}' )
				file.write('\n')

	#Start scraping the stored links.
	scrape_course = scrape_course()
	
	filter_rating = float(input('Enter the minimum rating you want the course to be: '))
	print(f'Entered rating is: {filter_rating}')
	deleted_course_dictionary, existing_course_dictionary = scrape_course.fetch_link_info(filter_rating)

	#Dumping the data to csv files
	generate_csv = generate_csv(deleted_course_dictionary, existing_course_dictionary)
	
	"""
	TODO: 
	* Needs a front end.
	* Need to save the course_page_number so that this will not scrape the same info again and again.
	* Need to add Multi-threading so that fetching the course pages will take less time.
	"""