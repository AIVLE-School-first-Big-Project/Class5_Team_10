from re import T
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Board, Comment
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .forms import PostForm, CommentForm
from user.models import User
import os


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
    post = get_object_or_404(Post, pk=post_id)
    context = {'post':post}
    # 댓글 작성 예외처리
    try:
        comments = Comment.objects.filter(post_table=post_id)
    except:
        comments = None
    if request.method == "POST":
        form = CommentForm(request.POST)
            
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = User.objects.get(pk=request.user.id)
            comment.post = Post.objects.get(pk=post_id)
            comment.create_date = timezone.now()
            comment.save()
        else:
            return render(request, 'post_detail/post_detail_test.html', {'post':post, 'comments':comments})
    return render(request, 'board/post.html', context)


@csrf_exempt
def post_create(request):   # 게시물 작성 함수
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.regdate = timezone.now()
            post.img = request.FILES.get('image')
            post.user = request.user
            post.board = Board.objects.get(ctg=request.POST['category'])
            post.save()
            return redirect('board:post', post_id=post.id)
    else:
        form = PostForm()
    context = {'form':form}
    return render(request, 'board/post_create.html', context)


@csrf_exempt
def post_modify(request, post_id): # 게시물 수정 함수
    post = get_object_or_404(Post, pk=post_id)
    pre_img = post.img
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.moddate = timezone.now()
            if request.FILES.get('image'):
                post.img = request.FILES.get('image')
                # 이미지 삭제 요청이 있으면
            elif request.POST.get('check'):
                    post.img = None
                    try:
                        os.remove('media/board_images/{}/{}_{}'.format(post.board.ctg, pre_img, '.png'))
                    except:
                        pass
            else:
                post.img = pre_img
            post.board = Board.objects.get(ctg=request.POST['category'])
            post.save()
            return redirect('board:post', post_id=post.id)
    else:
        form = PostForm(instance=post)
    context = {'form':form, 'post':post}
    return render(request, 'board/post_modify.html', context)

@csrf_exempt
def post_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('board:post_list')


def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('board:post', post_id=comment.post.id)