from django.shortcuts import render

# Create your views here.


def index(request):

    return render(request, 'random_drinks_front/index.html')

def drink(request):

    user_prompt = str(request.GET["ingred"])

    return render(request, "index.html", {"your drink": name_generator.py})

