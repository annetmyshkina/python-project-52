from django.http import HttpResponse

def home(request):
    return HttpResponse("Приветствие от task_manager!")
