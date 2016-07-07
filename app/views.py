from django.shortcuts import render, redirect
from models import *
from forms import *
from django.http import HttpResponse
# Create your views here.
def main(request):
    if request.GET.items():
        action = request.GET.get('action')
        id = request.GET.get('id')
        if action == 'dell':
            Todo.objects.filter(id=id).delete()
            return redirect('main')
        elif action == 'upp':
            if id == 1:
                return redirect('main')
            else:
                taskup = Todo.objects.filter(id=id).get()
                taskdown = Todo.objects.filter(id=int(id) - 1).get()
                Todo.objects.filter(id=taskup.id).update(task=taskdown.task, done=taskdown.done)
                Todo.objects.filter(id=taskdown.id).update(task=taskup.task, done=taskup.done)
                return redirect('main')
        elif action == 'down':
            data = Todo.objects.filter().values('id')
            max_id = 0
            for i in data:
                if i > max_id:
                    max_id = i['id']
            if int(id) == max_id:
                return redirect('main')
            else:
                taskdown = Todo.objects.filter(id=id).get()
                taskup = Todo.objects.filter(id=int(id) + 1).get()
                Todo.objects.filter(id=taskup.id).update(task=taskdown.task, done=taskdown.done)
                Todo.objects.filter(id=taskdown.id).update(task=taskup.task, done=taskup.done)
                return redirect('main')
    else:
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

def update(request):
    pass