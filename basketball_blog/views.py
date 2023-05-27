from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import NewArticleForm, CommentForm, EditArticleForm
from .models import Article, Comment
from django.http import Http404
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)

def base_view(request):
    return render(request, 'base.html')

def main_view(request):
    category = request.GET.get('category')
    if category:
        latest_posts = Article.objects.filter(category__name=category).order_by('-created_at')[:10]
    else:
        latest_posts = Article.objects.order_by('-created_at')[:10]
    return render(request, 'main.html',  {'latest_posts': latest_posts})

def logout_view(request):
    logout(request)
    return redirect("/")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        messages.info(request, "Nieprawidłowe dane logowania")
        return render(request, 'login.html')
    return render(request, 'login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')        
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def new_article_view(request):
    if not request.user.is_authenticated:
        messages.info(request, "Musisz być zalogowany aby dodać artykuł")
        return redirect("/login")
    if request.method == 'POST':
        form = NewArticleForm(request.POST)
        if form.is_valid() and form["content"].value() and form["title"].value():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('/', article_id=article.pk)
    else:
        form = NewArticleForm()
    return render(request, 'new_article.html', {'form': form})

def article_view(request, id):
    article = get_object_or_404(Article, article_id=id)
    comments = Comment.objects.filter(article=id)
    can_edit = False
    if article.author == request.user or request.user.is_superuser:
        can_edit = True
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() and form["content"].value():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article = article
            comment.save()
            return redirect(f"/article/{article.article_id}", id=article.pk)
    else:
        form = CommentForm()
    if request.method == 'POST' and 'delete_comment' in request.POST:
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, pk=comment_id)

        if request.user.is_superuser or comment.author == request.user:
            comment.delete()
        return redirect(f"/article/{id}", id=id)
    if request.method == 'POST' and 'delete_article' in request.POST:
        article.delete()
        return redirect("/")
    return render(request, 'article_details.html', {'article': article, 'comments': comments, 'form': form, 'can_edit': can_edit})

def edit_article(request, id):
    article = get_object_or_404(Article, article_id=id)
    if article.author != request.user and not request.user.is_superuser:
        return redirect(f"/article/{id}")
    
    if request.method == 'POST':
        form = EditArticleForm(request.POST, instance=article)
        if form.is_valid() and form["content"].value() and form["title"].value():
            form.save()
            return redirect(f"/article/{id}/")
    else:
        form = EditArticleForm(instance=article)

    return render(request, 'edit_article.html', {"form": form})

