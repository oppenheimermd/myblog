from typing import List
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from .forms import EmailPostForm, CommentForm, SearchForm
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity

# Get all published post
def post_list(request, tag_slug=None):
    # build the initial QuerySet
    object_list = Post.published.all()
    tag = None

    # If filtering by tag slug:
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Fiter the list of posts by the ones that contain the given tag:
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
        
    return render(request,
                 'blog/post/list.html',
                 {'page': page,
                  'posts': posts,
                  'tag': tag})
                  
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    
    # List of active comments for this post(a QuerySet)
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
        
    else:
        comment_form = CommentForm()

    # List of similar posts
    #   Retrieve a Python list of IDs for the tags of the current post.
    #   QuerySet(QS) returns  tuples with the values fro the given fields.  The
    #   values_list() QS returns tuples with values for the given fields. flat=
    #   true to get single values
    post_tags_ids = post.tags.values_list('id', flat=True)
    #   Get all post that contain any of the tags, exclusive current post.
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    #   Use count aggregation function to generate a calculated field -
    #   same_tages - containes the number tags shared with all the tags
    #   queried.
    #
    #   Order results by the number of shared tags in descending order and
    #   by publish to dispaly recent post first for the posts with the same
    #   number of shared tags. Slice the results to retrieve only the first 
    #   four posts.
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                  'comments':comments,
                  'new_comment': new_comment,
                  'comment_form': comment_form,
                  'similar_posts':similar_posts})

def post_share(request, post_id):
    #  Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')

    if request.method == 'POST':
        #  Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #  Form fields passed validation
            cd = form.cleaned_data
            #   Send email
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.htm',
                    {'post':post,
                    'form':form})
                    
#   Class based view             
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
