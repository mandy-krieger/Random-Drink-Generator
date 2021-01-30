from django.http import HttpResponseRedirect
from django.shortcuts import render
from frontendproject.random_drinks_front.forms import NameForm
# Create your views here.


def index(request):

    return render(request, 'random_drinks_front/index.html')



def get_name(request):
    # if this is a POST request we need to process the form data
    print(request)
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})

#def drink(request):

 #   user_prompt = str(request.GET["ingred"])

  #  return render(request, "random_drinks_front", {"your drink": index})

