from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from .models import *


def chek_user(users, username, password, repeat_password, age):
    if username in users:
        return 'Пользователь уже существует'
    elif password != repeat_password:
        return 'Пароли не совпадают'
    elif int(age) < 18:
        return 'Вы должны быть старше 18 лет!'
    else:
        return None


def sign_up_by_html(request):
    users = [i.name for i in Buyer.objects.all()]
    info = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')
        erorr = chek_user(users, username, password, repeat_password, age)
        if erorr:
            info = {'error': erorr}
            return render(request, 'registration_page.html', context=info)
        else:
            Buyer.objects.create(name= username, balance=0.00, age=age)
            return HttpResponse(f'Приветствуем, {username}!')
    return render(request, 'registration_page.html')


def sign_up_by_django(request):
    users = [i.name for i in Buyer.objects.all()]
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']
            erorr = chek_user(users, username, password, repeat_password, age)
            if erorr:
                info = {'error': erorr}
                return render(request, 'registration_page.html', context=info)
            else:
                Buyer.objects.create(name=username, balance=0.00, age=age)
                return HttpResponse(f'Приветствуем, {username}!')
    else:
        form = UserRegister()
        info = {'form': form}
    return render(request, 'registration_page.html', context=info)


def index_platform(request):
    title = 'Главная страница'
    context = {
        'title': title,
    }
    return render(request, 'platform.html', context)


def index_cart(request):
    title = 'Корзина'
    text = 'Извините, ваша корзина пуста'
    text2 = 'Вернуться обратно'
    context = {
        'title': title,
        'text': text,
        'text2': text2,
    }
    return render(request, 'cart.html', context)


def index_games(request):
    title = 'Магазин'
    text = 'Игры'
    game = Game.objects.all()
    text_but1 = 'Купить'
    text_but2 = 'Вернуться обратно'
    context = {
        'title': title,
        'text': text,
        'game': game,
        'text_but1': text_but1,
        'text_but2': text_but2,
    }
    return render(request, 'games.html', context)
