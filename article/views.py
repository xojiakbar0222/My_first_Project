from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Comment
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from .forms import PostShareForm, CommentForm


# Create your views here.

def index(request):
    return HttpResponse('Hello world')

def new(request):
    posts = Post.objects.all()
    return HttpResponse('Hello Hojiakbar aka')

def base_view(request):
   categories = Category.objects.filter(status = 'active')
   context = {
      'categories':categories,
   }
   return render(request, 'base.html', context)

def list_view(request):
    latest_post = Post.objects.filter(status='active').first()
    posts = Post.objects.filter(status='active')[7:]
    categories = Category.objects.filter(status='active')
    last6 = Post.objects.filter(status='active')[1:7:1]
    videos = Post.objects.filter(status = 'active').exclude(video__exact='')[:6]
    #paginator
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
       posts = paginator.page(page)
    except PageNotAnInteger:
       posts = paginator.page(1)
    except EmptyPage:
       posts = paginator.page(paginator.num_pages)
    #paginator
    context = {
       'maqolalar':posts, 
       'page':page, 
       'categories':categories,
       'latest_post' : latest_post,
       'last6': last6,
       'videos': videos,
       }
    return render(request, 'article/list.html', context)

def detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    categories = Category.objects.filter(status='active')
    comments = post.izohlar.filter(status=True)

    new_comment = None
    if request.method == 'POST':
       comment_form = CommentForm(request.POST)
       if comment_form.is_valid():
          new_comment = comment_form.save(commit=False)
          new_comment.post = post #new_comment.post(name,email...) - modelda commentga berilgan maydonlardan biri
          new_comment = comment_form.save()
    else:
       comment_form = CommentForm()

    context = {
       'maqola':post, 
       'izohlar': comments,
       'izoh_maydoni': comment_form,
       'yangi_izoh': new_comment,
       'categories': categories
       }

    return render(request, 'article/detail.html', context)


def post_share(request, id):
  categories = Category.objects.filter(status = 'active')
  # id bo'yicha maqola olinadi
  post = get_object_or_404(Post, id=id)
  sent = False
  if request.method == 'POST':
    # forma saqlash  uchun yuboriladi
    form = PostShareForm(request.POST)
    if form.is_valid():
      # barcha maydonlar tasdiqlandi
      cd = form.cleaned_data
      
      post_url = request.build_absolute_uri(post.get_absolute_url())
      email = cd['email']
      subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
      message = 'Read "{}" at {}\n\n{}\'s comment:{}'.format(post.title, post_url, cd['name'], cd['comment'])
      send_mail(subject, message, email, [cd['to']])
      sent = True
  else:
    form = PostShareForm()

  context = {
      'maqola': post, 
      'form': form,
      'sent': sent,
      'categories': categories,
      }

  return render(request, 'article/share.html', context)

def categories_list(request, id):
   category_object = get_object_or_404(Category, id = id)
   posts = Post.objects.filter(category = category_object.id)
   categories = Category.objects.filter(status='active')

   #paginator
   paginator = Paginator(posts, 6)
   page = request.GET.get('page')
   try:
      posts = paginator.page(page)
   except PageNotAnInteger:
      posts = paginator.page(1)
   except EmptyPage:
      posts = paginator.page(paginator.num_pages)

   context = {
      'category_object':category_object,
      'posts':posts,
      'page':page,
      'categories':categories
   }

   return render(request, 'article/categories_list.html', context)
