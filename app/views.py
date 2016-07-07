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
        if action == 'upp':
            take_up = Todo.objects.filter(id=id).get()
            if take_up.place == 1:
                return redirect('main')
            else:
                place = int(take_up.place)-1
                take_down = Todo.objects.filter(place=place).get()
                take_up_id = take_up.id
                take_down_id = take_down.id
                Todo.objects.filter(id=take_down_id).delete()
                Todo.objects.filter(id=take_up_id).update(id=take_down_id)
                Todo.objects.create(id=take_up_id, task=take_down.task, done=take_down.done)
                return redirect('main')
        elif action == 'down':
            take_up = Todo.objects.filter(id=id).get()
            count_db = Todo.objects.filter().count()
            if take_up.place == count_db:
                return redirect('main')
            else:
                place = int(take_up.place) + 1
                take_down = Todo.objects.filter(place=place).get()
                take_up_id = take_up.id
                take_down_id = take_down.id
                Todo.objects.filter(id=take_down_id).delete()
                Todo.objects.filter(id=take_up_id).update(id=take_down_id)
                Todo.objects.create(id=take_up_id, task=take_down.task, done=take_down.done)
                return redirect('main')

    else:
        data = Todo.objects.filter()
        place = 1
        for i in data:
            Todo.objects.filter(id=i.id).update(place=place)
            place += 1
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