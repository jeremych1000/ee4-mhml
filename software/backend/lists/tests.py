from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from lists.models import Item
from lists.models import List


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'ml_homepage.html')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        l =  List.objects.create()
        response = self.client.get('/lists/%d/'%l.id)
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        list1 = List.objects.create()
        Item.objects.create(text='one', list=list1)
        Item.objects.create(text='two', list=list1)
        response1 = self.client.get('/lists/%d/' % (list1.id))
        list2 = List.objects.create()
        Item.objects.create(text='other one', list=list2)
        Item.objects.create(text='other two', list=list2)
        response2 = self.client.get('/lists/%d/' % (list2.id))
        self.assertIn('one', response1.content.decode())
        self.assertIn('two', response1.content.decode())
        self.assertIn('other one', response2.content.decode())
        self.assertIn('other two', response2.content.decode())


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/1/')


class ListandItemModelTest(TestCase):
    def testing_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        first_item = Item()
        first_item.list = list_
        first_item.text = 'one'
        first_item.save()
        second_item = Item()
        second_item.text = 'two'
        second_item.list = list_
        second_item.save()
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        self.assertEqual(Item.objects.all()[0].text, 'one')
        self.assertEqual(Item.objects.all()[1].text, 'two')


