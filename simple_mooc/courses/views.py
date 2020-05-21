from django.shortcuts import render, get_object_or_404, redirect
#importacao dos models de cursos
from .models import Course, Enrollment, Announcement, Lesson, Material
#importando formularios
from .forms import ContactCourse, CommentForm
from django.contrib.auth.decorators import login_required
#colocando app de mensagens do django 
from django.contrib import messages
from .decotators import enrollment_required

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

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )
    if created:
        enrollment.active()
        messages.success(request, 'Voce foi inscrito com sucesso')
    else:
        messages.info(request,'Voce ja esta inscrito no curso')
    return redirect('accounts:dashboard')

@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
            Enrollment, user=request.user, course=course
    )
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua Incrinção foi Cancelada')
        return redirect('accounts:dashboard')
    template = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course
    }
    return render(request, template, context)

@login_required
@enrollment_required
def announcements(request, slug):
    course = request.course
    template = 'courses/announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(request, template, context )

@login_required
def show_announcements(request, slug, pk):
    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(
            Enrollment, user=request.user, course=course
        )
        if not enrollment.is_approved():
            messages.erros(request, 'Inscricao Pendente')
            return redirect('accounts:dashboard')
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'Seu comentario foi enviado')
    template = 'courses/show_announcements.html'
    context = {
        'course': course,
        'announcement': announcement,
        'form': form

    }
    return render(request, template, context )


@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    template = 'courses/lessons.html'
    lessons = course.release_lessons()
    if request.user.is_staff:
        lessons = course.lessons.all()
    context = {
        'course': course,
        'lessons': lessons
    }
    return render(request, template, context)


@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(Lesson, pk=pk, course=course)
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esta aula não esta disponivel')
        return redirect('courses:lessons', slug=course.slug)
    template = 'courses/lesson.html'
    context = {
        'course': course,
        'lesson': lesson
    }
    return render(request, template, context)


@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esre material não esta disponivel')
        return redirect('courses:lesson', slug=course.slug, pk=lesson.pk)
    if not material.is_embedded():
        return redirect(material.file.url)
    template = 'courses/material.html'
    context = {
        'course': course,
        'lesson': lesson,
        'material': material
    }
    return render(request, template, context)