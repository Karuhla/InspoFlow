from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.urls import reverse
from .models import Image, Like, Category, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .models import Board
from .forms import BoardForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import ImageForm
from .forms import CustomUserCreationForm

# Create your views here.
def home(request):
    images = Image.objects.all() 
    return render(request, "home.html", {"images": images})
    
def category_view(request, category_name):
    category = Category.objects.get(name=category_name)
    images = category.images.all()
    return render(request, 'category_page.html', {'category': category, 'images': images})

def homepage_view(request):
    categories = Category.objects.all()
    return render(request, 'base.html', {'categories': categories})

def home_view(request):
    images = Image.objects.all()
    return render(request, 'home.html', {'images': images})

def register_view(request):
    next_url = request.POST.get('next', request.GET.get('next', '/'))
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form, 'next': next_url})

def login_view(request):
    next_url = request.POST.get('next', request.GET.get('next', '/'))  

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url)  

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'next': next_url})

def register(request):
    next_url = request.POST.get('next', request.GET.get('next', '/')) 

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect(next_url) 
    else:
        form = UserCreationForm()
        
    return render(request, 'register.html', {'form': form, 'next': next_url})
@login_required
def like_image(request, image_id):
    if request.method == "POST":
        image = get_object_or_404(Image, pk=image_id)

        if request.user.is_authenticated:
            like, created = image.likes.get_or_create(user=request.user)

            if not created:
                like.delete()

        return redirect('image_detail', image_id=image.id)

    return redirect('home')

@login_required
def comment_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(image=image, user=request.user, text=comment_text)

    return redirect('image_detail', image_id=image.id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user == request.user:
        comment.delete()

    return redirect('image_detail', image_id=comment.image.id)



def image_detail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)

    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = image.likes.filter(user=request.user).exists()
        boards = Board.objects.filter(user=request.user)
    else:
        boards = None

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(image=image, user=request.user, text=comment_text)
            return redirect('image_detail', image_id=image.id)

    comments = Comment.objects.filter(image=image).order_by('-created_at')

    context = {
        'image': image,
        'user_has_liked': user_has_liked,
        'boards': boards,
        'comments': comments,
    }

    return render(request, 'image_detail.html', context)


@login_required
def user_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    boards = Board.objects.filter(user=request.user) 
    return render(request, 'profile.html', {'profile': profile, 'boards': boards})


@login_required
def save_image_to_board(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    
    boards = Board.objects.filter(user=request.user)

    if request.method == 'POST':
        board_id = request.POST.get('selected_board_id')
        new_board_title = request.POST.get('new_board_name')

        if new_board_title:
            new_board = Board.objects.create(title=new_board_title, user=request.user)
            new_board.images.add(image)
        elif board_id:
            selected_board = get_object_or_404(Board, id=board_id, user=request.user)
            selected_board.images.add(image)

        return redirect('image_detail', image_id=image.id)

    return render(request, 'image_detail.html', {'image': image, 'boards': boards})





@login_required
def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id, user=request.user)
    images = board.images.all() 
    return render(request, 'board_detail.html', {'board': board, 'images': images})




@login_required
def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user  
            board.save()
            form.save_m2m() 
            return redirect('board_detail', board_id=board.id)
    else:
        form = BoardForm()

    return render(request, 'create_board.html', {'form': form})

@login_required
def update_board(request, board_id):
    board = get_object_or_404(Board, id=board_id, user=request.user)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            form.save_m2m() 
            return redirect('board_detail', board_id=board.id)
    else:
        form = BoardForm(instance=board)

    return render(request, 'update_board.html', {'form': form, 'board': board})


@login_required
def profile(request):
    profile = request.user.profile  
    boards = Board.objects.filter(user=request.user)  

    if request.method == "POST":
        new_url = request.POST.get("profile_picture_url")
        print(f"Received URL: {new_url}")
        
        if new_url:
            profile.profile_picture_url = new_url
            profile.save()
            print(f"Updated Profile Picture URL: {profile.profile_picture_url}")  
            messages.success(request, "Profile picture updated successfully!")
            return redirect('user_profile')  
        else:
            messages.error(request, "Please provide a valid URL for the profile picture.")
    
    return render(request, "profile.html", {"boards": boards, "profile": profile})



def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    if request.method == "POST":
        image.delete()
        messages.success(request, "Image successfully deleted.")
        return redirect("home")  

    return redirect("image_detail", image_id=image_id)

def is_admin(user):
    return user.is_staff  

@user_passes_test(is_admin)
def add_image(request):
    if request.method == "POST":
        form = ImageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Image added successfully!")
            return redirect("home")  
    else:
        form = ImageForm()

    return render(request, "add_image.html", {"form": form})


@login_required
def remove_image_from_board(request, board_id, image_id):
    board = get_object_or_404(Board, id=board_id, user=request.user)
    image = get_object_or_404(Image, id=image_id)

    if request.method == "POST":
        board.images.remove(image)  
        messages.success(request, f"Image with URL '{image.url}' removed from board '{board.title}'.")
        return redirect('board_detail', board_id=board.id)

@login_required
def delete_board(request, board_id):
    board = get_object_or_404(Board, id=board_id, user=request.user)
    if request.method == "POST":
        board.delete()
        messages.success(request, "Board deleted successfully.")
        return redirect('user_profile') 
    return render(request, 'confirm_delete.html', {'board': board})
