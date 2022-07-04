from django.http import HttpResponse
from django.shortcuts import render
import generator


def get_pattern(request):
    if request.method == 'POST':
        pattern = str(request.POST['pattern'])
        genome = generator.generate_new_genome(pattern)
    return HttpResponse(generator.generate_pattern(genome))


def index(request):
    if request.method == 'POST':
        return render(request, 'PM/index.html')
