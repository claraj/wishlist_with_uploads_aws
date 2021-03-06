import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from django.test import LiveServerTestCase


class TitleTest(LiveServerTestCase):

    fixtures = ['test_users']

    def setUp(self):

        self.browser = webdriver.Chrome()  # Change to .Firefox() if using Firefox
        self.browser.implicitly_wait(3)

        self.browser.get(self.live_server_url)   # expect to be redirected to login page 
        self.browser.find_element_by_id('id_username').send_keys('alice')
        self.browser.find_element_by_id('id_password').send_keys('qwertyuiop')
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
    

    def tearDown(self):
        self.browser.quit()

    def test_title_shown_on_home_page(self):    
        self.browser.get(self.live_server_url)   # get site homepage  
        assert 'Travel Wishlist' in self.browser.title



class AddEditPlacesTests(LiveServerTestCase):

    fixtures = ['test_users', 'test_places']

    def setUp(self):
        self.browser = webdriver.Chrome()  
        self.browser.implicitly_wait(3)
       
        self.browser.get(self.live_server_url)   # expect to be redirected to login page 
        self.browser.find_element_by_id('id_username').send_keys('alice')
        self.browser.find_element_by_id('id_password').send_keys('qwertyuiop')
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
    
        
    def tearDown(self):
        self.browser.quit()

    def test_add_new_place(self):

        self.browser.get(self.live_server_url)   # Load home page
        input_name = self.browser.find_element_by_id('id_name') # find input text box. id was generated by Django forms
        input_name.send_keys('Denver')  # Enter place name 
        add_button = self.browser.find_element_by_id('add-new-place')  # Find the add button
        add_button.click()      # And click it

        # Got to make this test code wait for the server to process the request and for page to reload 
        # Wait for new element to appear on page
        wait_for_denver = self.browser.find_element_by_id('place-name-5')

        # Assert wishlist places from test_places are on page
        assert 'New York' in self.browser.page_source
        assert 'San Francisco' in self.browser.page_source
        
        # And the new place too
        assert 'Denver' in self.browser.page_source


    def test_mark_place_as_visited(self):

        self.browser.get(self.live_server_url)  # Load home page
        
        # find visited button. It will have the id visited_pk
        # Where pk = primary key of item. This was configured in the template
        # In this test, mark New York, pk=2 visited
        visited_button = self.browser.find_element_by_id('visited-button-2')
       
        # new_york = self.browser.find_element_by_id('place-name-2')  # find the place name text 

        visited_button.click()  # click button 

        # But now page has to reload. How to get Selenium to wait,
        # And to realize it's a new page, so refresh it's
        # knowledge of the elements on it?
        # Can use an Explicit Wait for a particular condition - in this case, the
        # absence of an element with id = place-name-2

        wait = WebDriverWait(self.browser, 3)
        ny_has_gone = wait.until(EC.invisibility_of_element_located((By.ID, 'place-name-2')))

        # Assert San Francisco is still on page
        assert 'San Francisco' in self.browser.page_source

        # But New York is not
        assert 'New York' not in self.browser.page_source

        # Load visited page
        self.browser.get(self.live_server_url + '/visited')

        # New York should be on the visited page
        assert 'New York' in self.browser.page_source

        # As well as our other visited places
        assert 'Tokyo' in self.browser.page_source
        assert 'Moab' in self.browser.page_source



class PageContentTests(LiveServerTestCase):

    fixtures = ['test_users', 'test_places']

    def setUp(self):
        self.browser = webdriver.Chrome()  
        self.browser.implicitly_wait(3)
        
        self.browser.get(self.live_server_url)   # expect to be redirected to login page 
        self.browser.find_element_by_id('id_username').send_keys('alice')
        self.browser.find_element_by_id('id_password').send_keys('qwertyuiop')
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
    

    def tearDown(self):
        self.browser.quit()

    def test_get_home_page_list_of_wishlist_places(self):

        self.browser.get(self.live_server_url)
        assert 'Tokyo' not in self.browser.page_source
        assert 'New York' in self.browser.page_source
        assert 'San Francisco' in self.browser.page_source
        assert 'Moab' not in self.browser.page_source


    def test_get_list_of_visited_places(self):
        self.browser.get(self.live_server_url + '/visited')
        assert 'Tokyo' in self.browser.page_source
        assert 'New York' not in self.browser.page_source
        assert 'San Francisco' not in self.browser.page_source
        assert 'Moab' in self.browser.page_source

