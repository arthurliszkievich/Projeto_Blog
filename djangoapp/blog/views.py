from django.core.paginator import Paginator
from django.shortcuts import render

posts = list(range(1, 101))


def index(request):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/pages/index.html', {'page_obj': page_obj})


def page(request):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/pages/page.html', {'page_obj': page_obj})


def post(request):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/pages/post.html', {'page_obj': page_obj})


def kitchen_sink(request):
    return render(request, 'blog/pages/kitchen_sink.html', {})
