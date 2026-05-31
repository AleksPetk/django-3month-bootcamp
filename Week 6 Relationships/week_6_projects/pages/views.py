from django.shortcuts import render, get_object_or_404
from .models import Subject, Article, Teacher, Comment
from django.db.models import Sum, Prefetch

# Create your views here.

def home(request):
    count = {}
    articles = Article.objects.all()
    count["subjects"] = Subject.objects.count()
    count["articles"] = articles.count()
    count["teachers"] = Teacher.objects.count()
    count["comments"] = Comment.objects.count()
    return render(request, "home.html", {
        "count": count,
        "articles": articles[:3]
    })

def teachers(request):
    teachers = Teacher.objects.prefetch_related("articles").annotate(
        total_views = Sum("articles__views")
    ).all()

    return render(request, "teachers.html", {
        "teachers": teachers
    })

def teacher_details(request, id):
    teacher = get_object_or_404(Teacher.objects.prefetch_related(
        Prefetch(
            "articles",
            queryset=Article.objects.filter(published=True),
            to_attr="published_articles"
        ), "articles__subject"
    ).annotate(
        total_views = Sum("articles__views")
    ), id=id)


    return render(request, 'teacher_details.html', {
        "teacher": teacher,
        "total_count": teacher.articles.count
    })

def subject_details(request, id):
    subject = get_object_or_404(Subject, id=id)

    return render(request, "subject_details.html", {
        "subject": subject
    })

def articles(request):
    articles = Article.objects.select_related("subject", "teacher").prefetch_related("comments").all()
    return render(request, "articles.html", {
        "articles": articles
    })