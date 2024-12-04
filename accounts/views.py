from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView, LoginView as BaseLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
from PIL import UnidentifiedImageError
from django.conf import settings



from .forms.signup import SignUpForm, LoginFrom
from .models import Post, Comment

# モデルロードと定数設定
model = load_model('./model.h5')
classes = ["猫", "犬"]
image_size = 100
UPLOAD_FOLDER = os.path.join(settings.MEDIA_ROOT, "media/uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# カスタムユーザーモデル
User = get_user_model()

# ユーティリティ関数
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "accounts/login.html"


class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/login.html"


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("profile")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

def users_index(request):
    users = User.objects.exclude(is_superuser=True).order_by("-created_at")
    return render(request, "accounts/users/index.html", {"users": users})

def users_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = user.post_set.order_by("-created_at")
    return render(request, "accounts/users/detail.html", {"user": user, "posts": posts})

@login_required
def profile(request):
    user_posts = request.user.post_set.order_by('-created_at')  # `post_set`は関連名
    return render(request, "accounts/profile.html", {"user": request.user, "posts": user_posts})

@login_required
def profile_edit(request):
    if request.method == "POST":
        user = request.user
        user.email = request.POST.get("email", user.email)
        user.username = request.POST.get("username", user.username)
        user.description = request.POST.get("description", user.description)
        user.save()
        return redirect("profile")
    return render(request, "accounts/profile_edit.html")

@login_required
def home(request):
    posts = Post.objects.all().order_by('id')
    return render(request, "accounts/home.html", {"posts": posts})


def posts_index(request):
    if request.method == "GET":
        posts = Post.objects.order_by("-created_at")
        return render(request, "accounts/index.html", {"posts": posts})
    elif request.method == "POST":
        return _posts_store(request)


def _posts_store(request):
    if request.method == "POST":
        file = request.FILES.get('image')

        if file:
            post = Post()
            post.image = file
            post.caption = request.POST.get("caption", "")
            post.user = request.user
            post.save()
            return redirect("home")
        else:
            return render(request, "accounts/create.html", {"error": "画像がアップロードされていません。"})
    
    return render(request, "accounts/home.html")


def posts_create(request):
    return render(request, "accounts/create.html")

def posts_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "accounts/detail.html", {"post": post})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('home')

@login_required
def comments_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Comment.objects.create(
        text=request.POST.get("text"),
        user=request.user,
        post=post,
    )
    return redirect("posts_detail", post.id)

# 画像アップロードビュー
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file or not allowed_file(file.name):
            return render(request, "accounts/create.html", {"answer": "無効なファイルです。"})

        # ファイル保存
        filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.name))
        with open(filepath, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # 画像読み込みと予測
        try:
            img = image.load_img(filepath, target_size=(image_size, image_size))
            data = np.array([image.img_to_array(img)])
            predicted = model.predict(data)[0].argmax()
            answer = f"これは {classes[predicted]} の写真です"
        except (UnidentifiedImageError, Exception) as e:
            answer = f"エラーが発生しました: {str(e)}"

        return render(request, "accounts/create.html", {"answer": answer})

    return render(request, "accounts/create.html", {"answer": ""})
