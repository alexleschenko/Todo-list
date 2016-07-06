from django.shortcuts import render, redirect
from models import *
from forms import *
# Create your views here.
def main(request):
    data = Todo.objects.filter()
    context = {'all_data':data}
    return render(request, 'main.html', context)

def add(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Todo.objects.create(task=data['task'], done=data['done'])
            return redirect(main)
        context = {'my_form':form}
        return render(request, 'add.html', context)
    else:
        context = {'my_form':TaskForm()}
        return render(request, 'add.html', context)