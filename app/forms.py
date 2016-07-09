#coding=utf-8
from django import forms

class TaskForm(forms.Form):
    task = forms.CharField(label='Задача', max_length=100)
    done = forms.BooleanField(label='Выполнить?', required=False)
