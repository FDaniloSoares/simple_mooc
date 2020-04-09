from django.shortcuts import render, get_object_or_404
#importacao dos models de cursos
from .models import Course
#importando formularios
from .forms import ContactCourse
# Create your views here.

def index(request):
    courses = Course.objects.all()
    template_name = 'courses/index.html'
    context = {
        'courses':courses
    }

    return render(request, template_name, context)

# Para passar parametro como ID
#def details(request, pk):
#    course = get_object_or_404(Course, pk=pk)
#    context = {
#        'course':course
#    }
#    template_name = 'courses/details.html'
#    return render(request, template_name, context)

# Para passar parametro como Slug
def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()
    context['form'] = form
    context['course'] = course
    template_name = 'courses/details.html'
    return render(request, template_name, context)