#coding=utf-8
from django.test import TestCase
from models import *
# Create your tests here.
class ProjectTest(TestCase):

    def test_ok_create_task(self):  # создание записи

        data = {'task':'my_task', 'done':False}
        self.client.post('/add/', data)
        q_task = Todo.objects.filter()
        self.assertEquals(q_task.count(), 1)
        task = q_task.get()
        self.assertEquals(task.task, data['task'])
        self.assertEquals(task.done, data['done'])

    def test_ok_delete_task(self): # удаление записи

        Todo.objects.create(task='my_task', done=True)
        task = Todo.objects.filter().last()
        self.client.get('', {'action':'dell', 'id':task.id})
        q_task = Todo.objects.filter()
        self.assertEquals(q_task.count(), 0)

    def test_ok_update_task(self): # обновление записи
        Todo.objects.create(task='my_task', done=True)
        task = Todo.objects.filter().last()
        self.client.get('/update/', { 'id': task.id})
        data = {'task':'new_task', 'done':False}
        self.client.post('/update/', data)
        task = Todo.objects.filter().get()
        self.assertEquals(task.task, data['task'])
        self.assertEquals(task.done, data['done'])