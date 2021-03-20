from django.test import TestCase, Client
from django.urls import reverse
from budget.models import Project, Category, Expense
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args=['project'])
        self.project = Project.objects.create(
            name='project',
            budget=1000,
        )


    
    def test_project_list_GET(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-list.html')


    def test_project_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-detail.html')


    
    def test_project_detail_POST_add_new_expense(self):

        Category.objects.create(
            project = self.project,
            name = 'development'
        )

        response = self.client.post(self.detail_url, {
            'title': 'expense',
            'amount': 1000,
            'category': 'development'
        })

        self.assertEquals(response.status_code, 302)  # redirect status code
        self.assertEqual(self.project.expenses.first().title, 'expense')


    def test_project_detail_POST_no_data(self):
        response = self.client.post(self.detail_url)
        self.assertEquals(response.status_code, 302)  # redirect status code
        self.assertEqual(self.project.expenses.count(), 0)



    def test_project_detail_DELETE_deletes_expense(self):

        category1 = Category.objects.create(
            project = self.project,
            name = 'development'
        )

        Expense.objects.create(
            project=self.project,
            title='expense',
            amount = '1000',
            category=category1
        )

        response = self.client.delete(self.detail_url, json.dumps({
            'id': 1,
        }))
        self.assertEquals(response.status_code, 204)  # delete status code
        self.assertEqual(self.project.expenses.count(), 0)
