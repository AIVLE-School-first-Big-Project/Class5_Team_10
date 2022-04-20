from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.utils import timezone
from .forms import *
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def post_list(request): # 게시물 목록 조회 함수
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    type = request.GET.get('type', '') # 카테고리
    post_list = Post.objects.order_by('-regdate')

    if kw:
        if type == 'title':
            post_list = post_list.filter(Q(title__icontains=kw))# 제목 검색
        if type == 'content':
            post_list = post_list.filter(Q(content__icontains=kw))  # 내용 검색
        if type == 'category':
            post_list = post_list.filter(Q(board__ctg__icontains=kw))
    
    paginator = Paginator(post_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'post_list':page_obj, 'page': page, 'kw': kw, 'type':type}
    return render(request, 'board/post_list.html', context)


def post(request, post_id): # 게시물 상세 조회 함수
    post = Post.objects.get(id=post_id)
    context = {'post':post}
    return render(request, 'board/post.html', context)


def post_create(request):   # 게시물 작성 함수
    if request.method == 'POST':
        form = PostForm(request.Post)
        if form.is_valid(): # 유효성 검사를 통과하면
            post = form.save(commit=False)
            post.save()
            return redirect('/board/')
    else:
        form = PostForm()
    return render(request, 'board/post_create.html', {'form':form})

# def comment_create(request, post_id): # 게시물 댓글 작성 함수

