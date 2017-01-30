from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from lists.models import Item
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class NewVisitorTest(StaticLiveServerTestCase):
    def check_for_row_in_list_table(self, item_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(item_text in row.text for row in rows),
            "New to-do item did not appear in table -- its text was:\n%s" % (
                item_text,
            )
        )

    def setUp(self):
        self.browser = webdriver.Chrome('./webdrivers/chromedriver.exe')
        self.browser.implicitly_wait(3)

    def tearDown(self):
        time.sleep(3)
        self.browser.refresh()
        self.browser.quit()

    def test_only_saves_items_when_necessary(self):
        self.browser.get(self.live_server_url)
        self.assertEqual(Item.objects.count(), 0)

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('Buy peacock feathers')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('Buy peacock feathers')
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.browser.quit()
        self.browser = webdriver.Chrome('./webdrivers/chromedriver.exe')
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('Buy milk')
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=5)
