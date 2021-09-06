from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Food

class FoodModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='tester_1',password='123')
        test_user.save()

        test_food = Food.objects.create(
            author = test_user,
            title = 'Yummy Food',
            recepi = 'All yummy food'
        )
        test_food.save()

    def test_foods_content(self):
        food = Food.objects.get(id=1)

        self.assertEqual(str(food.author), 'tester_1')
        self.assertEqual(food.title, 'Yummy Food')
        self.assertEqual(food.recepi, 'All yummy food')


# Testing API
class APITest(APITestCase):
    def test_list(self):
        response = self.client.get(reverse('foods_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):
        """
        Test if api can detail the food recepi
        """

        test_user = get_user_model().objects.create_user(username='tester_1',password='123')
        test_user.save()

        test_post = Food.objects.create(
            author = test_user,
            title = 'Yummy Food',
            recepi = 'All yummy food'
        )
        test_post.save()

        response = self.client.get(reverse('foods_detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id':1,
            'title': test_post.title,
            'recepi': test_post.recepi,
            'author': test_user.id,
        })


    def test_create(self):
        """
        Test if api can create food recepi"""
        test_user = get_user_model().objects.create_user(username='tester_1',password='123')
        test_user.save()

        url = reverse('foods_list')
        data = {
            "title":"All is good",
            "recepi":"Eat and be happy",
            "author":test_user.id,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, test_user.id)

        self.assertEqual(Food.objects.count(), 1)
        self.assertEqual(Food.objects.get().title, data['title'])

    def test_update(self):
        """
        Test if the api can update a food """
        test_user = get_user_model().objects.create_user(username='tester_1',password='123')
        test_user.save()

        test_food = Food.objects.create(
            author = test_user,
            title = 'Cinnamon Balls',
            recepi = 'Full of sugar'
        )

        test_food.save()

        url = reverse('foods_detail',args=[test_food.id])
        data = {
            "title":"Bannana Fried Stick",
            "author":test_food.author.id,
            "recepi":test_food.recepi,
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, url)

        self.assertEqual(Food.objects.count(), test_food.id)
        self.assertEqual(Food.objects.get().title, data['title'])


    def test_delete(self):
        """Test the api can delete a food."""

        test_user = get_user_model().objects.create_user(username='tester_1',password='123')
        test_user.save()

        test_food = Food.objects.create(
            author = test_user,
            title = 'Meat Balls',
            recepi = 'Deleciuos high protein meal'
        )

        test_food.save()

        post = Food.objects.get()

        url = reverse('foods_detail', kwargs={'pk': post.id})


        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)


