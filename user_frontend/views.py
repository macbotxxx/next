from django.shortcuts import render

# Create your views here.

def user_index (request):

    return render( request, 'user_dashboard/index.html')
