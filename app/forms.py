from django import forms

class TaskForm(forms.Form):
    task = forms.CharField(label='Task', max_length=100)
    done = forms.BooleanField(label='Done?')
