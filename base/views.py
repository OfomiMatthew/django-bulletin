from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator
from .models import Post,Category, Tag,Contact,Comment
from transformers import pipeline
from .forms import ContactForm,PostForm,CommentForm
from django.utils import timezone 
from django.db.models import Q 
from accounts.models import Profile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.text import slugify
from django.db.models import Count

sentiment_pipeline = pipeline("sentiment-analysis")



def index(request):
    query = request.GET.get('q')
    category_slug = request.GET.get('category')

    # Base queryset for published posts
    posts = Post.objects.filter(status='published').order_by('-publication_date')

    # Apply search filter if `query` is provided
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    # Apply category filter if `category_slug` is provided
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)

    # Pagination
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all categories for the sidebar or filter
    categories = Category.objects.all()

    # Context data
    context = {'page_obj': page_obj, 'categories': categories}
    return render(request, 'index.html', context=context)


   
@login_required 
def PostDetails(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    comments = Comment.objects.filter(post=post).order_by('-created')
    profile = Profile.objects.get(user=request.user)
    
    is_favorite = profile.favorite_posts.filter(slug=post_slug).exists()
    
    if request.method == 'POST':
        if is_favorite:
            profile.favorite_posts.remove(post)
        else:
            profile.favorite_posts.add(post)
        return redirect('bulletins', post_slug=post_slug)  # Redirect to refresh the page
    
    related_posts = Post.objects.filter(
        category=post.category, status='published'
    ).exclude(id=post.id)[:4]

    context = {'posts': post, 'related_posts': related_posts, 'is_favorite': is_favorite, 'comments': comments}
    return render(request, 'post_detail.html', context)




# # Load the sentiment analysis pipeline
# sentiment_pipeline = pipeline("sentiment-analysis")

# def sentiment_analysis_view(request):
#     result = None
#     if request.method == "POST":
#         user_input = request.POST.get("text")
#         if user_input:
#             analysis = sentiment_pipeline(user_input)
#             result = {
#                 "label": analysis[0]["label"],
#                 "score": analysis[0]["score"],
#             }
#     return render(request, "sentiment.html", {"result": result})

def ContactView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.message_date = timezone.now()
            form.save()
            return redirect('contact-success') #contact  page
    else:
        form = ContactForm()
    context ={'form':form}
    return render(request,'contact_form.html',context)


# @login_required
# def CreatePost(request):
#     if not request.user.is_staff and not request.user.is_superuser:
#         return HttpResponseForbidden("You are not authorized to create posts.")
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('bulletins', post_slug=post.slug)
#     else:
#         form = PostForm()
#     context = {'form':form}
#     return render(request,'post.html',context)

@login_required
def CreatePost(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to create posts.")
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'published'
            original_slug = slugify(post.title)
            slug = original_slug
            num = 1

            # Check for uniqueness and increment if necessary
            while Post.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{num}"
                num += 1

            post.slug = slug
            post.save()
            form.save_m2m()  # Save tags (many-to-many fields)
            return redirect('bulletins', post_slug=post.slug)
    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'post.html', context)



        

def ContactSuccess(request):
    return render(request,'contact_success.html')


# def search_post(request):
#     query = request.GET.get('q') if request.GET.get('q') != None else ''
#     # if query:
#     posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
#     # else:
#     #     posts = Post.objects.all()
#     context = {'posts': posts}
#     return render(request, 'search.html', context)

@login_required  
def create_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    sentiment_result = None

    if request.method == "POST":
        form = CommentForm(request.POST)
        if "check_sentiment" in request.POST:
            # Step 1: Only check sentiment
            if form.is_valid():
                comment_text = form.cleaned_data["text"]
                analysis = sentiment_pipeline(comment_text)
                sentiment_result = {
                    "label": analysis[0]["label"],
                    "score": f"{analysis[0]['score'] * 100:.2f}"
                }
            return render(request, 'create_comment.html', {
                'form': form,
                'post': post,
                'sentiment_result': sentiment_result
            })

        elif "submit_comment" in request.POST:
            # Step 2: Save the comment after confirming sentiment
            if form.is_valid():
                newComment = form.save(commit=False)
                newComment.user = request.user
                newComment.post = post
                newComment.save()
                return redirect('bulletins', post_slug=newComment.post.slug)
            else:
                return render(request, 'create_comment.html', {
                    'form': form,
                    'post': post,
                    'error': 'Invalid form data.'
                })

    else:
        return render(request, 'create_comment.html', {
            'form': CommentForm(),
            'post': post
        })  
# def create_comment(request, post_slug):
#     post = get_object_or_404(Post, slug=post_slug)
#     sentiment_result = None

#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         comment_text = request.POST.get('text')

#         if 'check_sentiment' in request.POST and comment_text:
#             # Run sentiment analysis
#             analysis = sentiment_pipeline(comment_text)
#             sentiment_result = {
#                 "label": analysis[0]["label"],
#                 "score": round(analysis[0]["score"] * 100, 2),  # e.g., 97.34%
#             }
#             return render(request, 'create_comment.html', {
#                 'form': form,
#                 'post': post,
#                 'sentiment_result': sentiment_result,
#             })

#         elif 'submit_comment' in request.POST:
#             if form.is_valid():
#                 newComment = form.save(commit=False)
#                 newComment.user = request.user
#                 newComment.post = post
#                 newComment.save()
#                 return redirect('bulletins', post_slug=post.slug)

#     else:
#         form = CommentForm()

#     return render(request, 'create_comment.html', {
#         'form': form,
#         'post': post,
#         'sentiment_result': sentiment_result
#     })       
# def create_comment(request, post_slug):
#     post = get_object_or_404(Post, slug=post_slug)
#     if request.method == 'GET':
#         return render(request, 'create_comment.html', {'form':CommentForm(),'post': post})
#     else:
#         try:
#             form = CommentForm(request.POST)
#             if form.is_valid():
#                 newComment = form.save(commit=False)
#                 newComment.user = request.user
#                 newComment.post = post
#                 newComment.save()
#                 return redirect('bulletins', post_slug=newComment.post.slug)
#             else:
#                 return render(request, 'create_comment.html', {'form': form,'error': 'Bad data passed in. Try again.'})
#         except ValueError:
#             return render(request, 'create_comment.html', {'form': CommentForm(), 'error': 'Bad data passed in. Try again.'})
 
@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id,user=request.user)
    if request.method == 'GET':
        form = CommentForm(instance=comment)
        return render(request, 'update_comment.html', {'form': form, 'comment': comment})
    else:
        try:
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('bulletins', comment.post.slug)
            else:
                return render(request, 'update_comment.html', {'form': form, 'comment': comment, 'error': 'Bad data passed in. Try again.'})
        except ValueError:
            return render(request, 'update_comment.html', {'form': form, 'comment': comment, 'error': 'Bad data passed in. Try again.'})
        
        
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id,user=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.info(request,f'Comment: {comment.text} deleted successfully')
        return redirect('bulletins', comment.post.slug)
    return render(request, 'delete.html', {'obj': comment})