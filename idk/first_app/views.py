from django.shortcuts import render, redirect
from .models import Expression_result
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import StringAnalysis
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import datetime
import random

from loguru import logger
import os

# Настройка логирования
logger.remove()
logger.add("logs.log", format="{time} {level} {message}", level="INFO", rotation="10 MB")

def log_request(request, view_name):
    logger.info(
        f"User: {request.user} | Time: {datetime.datetime.now()} | View: {view_name} | Method: {request.method} | Params: {request.GET.dict() if request.method == 'GET' else request.POST.dict()}"
    )

def index_page(request):
    log_request(request, "index_page")
    context = {
        "name": "Алымов Ян",
        "pages": 10
    }
    return render(request, "index.html", context)

def time_page(request):
    log_request(request, "time_page")
    context = {
        "date": f"{datetime.date.today().day}.{datetime.date.today().month}.{datetime.date.today().year}",
        "time": f"{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}",
    }
    return render(request, "time.html", context)

def calc_page(request):
    log_request(request, "calc_page")
    try:
        first = request.GET.get('first', 0)
        second = request.GET.get('second', 0)
        numbers_sum = int(first) + int(second)
        context = {
            "first_number": first,
            "second_number": second,
            'numbers_sum': numbers_sum,
        }
    except Exception as e:
        logger.error(f"calc_page: Exception occurred: {e}")
        context = {
            "first_number": 0,
            "second_number": 0,
            'numbers_sum': 0,
            'error': str(e),
        }

    return render(request, "calc.html", context)

def multiply(request):
    log_request(request, "multiply")
    try:
        value = request.GET.get('value')
        if value is not None:
            number = int(value)
            result = [f"{i} * {number} = {i * number}" for i in range(1, 11)]
        else:
            result = None
    except Exception as e:
        logger.error(f"multiply: Exception occurred: {e}")
        result = None

    return render(request, 'multiply.html', {'result': result, 'value': value})

def expression(request):
    log_request(request, "expression")
    try:
        num_terms = random.randint(2, 4)
        terms = [random.randint(10, 99) for _ in range(num_terms)]
        signs = [random.choice(['+', '-']) for _ in range(num_terms - 1)]

        res = terms[0]
        expression_str = str(terms[0])

        for i in range(1, num_terms):
            sign = signs[i - 1]
            term = terms[i]
            expression_str += f" {sign} {term}"
            if sign == '+':
                res += term
            else:
                res -= term

        result = f"{expression_str} = {res}"
        Expression_result.objects.create(expression=result)

    except Exception as e:
        logger.critical(f"expression: Critical error computing expression: {e}")
        result = "Ошибка генерации выражения"

    return render(request, 'expression.html', {'result': result})

def history(request):
    log_request(request, "history")
    try:
        context = {'objects': Expression_result.objects.all()}
    except Exception as e:
        logger.error(f"history: Exception fetching history: {e}")
        context = {'objects': [], 'error': str(e)}

    return render(request, 'history.html', context)

def login_page(request):
    log_request(request, "login_page")
    context = {}
    context['user'] = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info(f"User {user.username} logged in successfully")
            return redirect('/')
        else:
            context['error'] = 'Неверное имя пользователя или пароль'
            logger.warning(f"Login failed for username: {username}")

    return render(request, 'login.html', context)

def logout_page(request):
    log_request(request, "logout_page")
    logger.info(f"User {request.user} logged out")
    logout(request)
    return redirect("/")

@login_required
def str2words_page(request):
    log_request(request, "str2words_page")
    context = {}

    if request.method == "POST":
        try:
            input_text = request.POST.get("input_text", "").strip()
            tokens = input_text.split()

            words = [token for token in tokens if any(ch.isalpha() for ch in token)]
            numbers = [token for token in tokens if token.isdigit()]

            word_count = len(words)
            number_count = len(numbers)
            char_count = len(input_text)

            StringAnalysis.objects.create(
                user=request.user,
                input_text=input_text,
                word_count=word_count,
                char_count=char_count,
            )

            context.update({
                'input_text': input_text,
                'word_count': word_count,
                'number_count': number_count,
                'words': words,
                'numbers': numbers,
            })
        except Exception as e:
            logger.error(f"str2words_page: Error analyzing string: {e}")
            context['error'] = str(e)

    return render(request, 'str2words.html', context)

@login_required
def str_history_view(request):
    log_request(request, "str_history_view")
    try:
        history = StringAnalysis.objects.filter(user=request.user).order_by('-timestamp')
        context = {'history': history}
    except Exception as e:
        logger.error(f"str_history_view: Error fetching string history: {e}")
        context = {'history': [], 'error': str(e)}

    return render(request, 'str_history.html', context)