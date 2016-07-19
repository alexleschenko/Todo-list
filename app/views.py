#coding=utf-8
from django.shortcuts import render, redirect

from forms import *
from models import *


# Create your views here.
def main(request):
    if request.GET.items():
        action = request.GET.get('action')
        id = request.GET.get('id')
        if action == 'dell': # удаление
            Todo.objects.filter(id=id).delete()
            return redirect('main')
        elif action == 'upp': #поднять вверх
            take_up = Todo.objects.filter(id=id).get()
            if take_up.place == 1:
                return redirect('main')
            else:
                place = int(take_up.place) - 1
                take_down = Todo.objects.filter(place=place).get()
                take_up_id = take_up.id
                take_down_id = take_down.id
                Todo.objects.filter(id=take_down_id).delete()
                Todo.objects.filter(id=take_up_id).update(id=take_down_id)
                Todo.objects.create(id=take_up_id, task=take_down.task, done=take_down.done)
                return redirect('main')
        elif action == 'down': #опустить запись
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
        elif action == 'done': #маркер выполнения и невыполнения
            Todo.objects.filter(id=id).update(done=True)
            return redirect('main')
        elif action == 'undone':
            Todo.objects.filter(id=id).update(done=False)
            return redirect('main')


    else:
        data = Todo.objects.filter()
        place = 1
        for i in data:
            Todo.objects.filter(id=i.id).update(place=place)
            place += 1
        data = Todo.objects.filter()
        context = {'all_data': data}
        return render(request, 'main.html', context)


def add(request): # добавление
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Todo.objects.create(task=data['task'], done=data['done'])
            return redirect(main)
        context = {'my_form': form}
        return render(request, 'add.html', context)
    else:
        context = {'my_form': TaskForm()}
        return render(request, 'add.html', context)


def update(request): #обновление
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if request.session.has_key('data'):
            id = request.session.get('data')
        del request.session['data']
        if form.is_valid():
            data = form.cleaned_data
            Todo.objects.filter(id=id).update(task=data['task'], done=data['done'])
            return redirect(main)
        context = {'my_form': form}
        return render(request, 'update.html', context)
    else:
        id = request.GET.get('id')
        predata = Todo.objects.filter(id=id).get()
        request.session['data'] = id
        context = {'my_form': TaskForm(initial={'task':predata.task})}
        return render(request, 'update.html', context)
