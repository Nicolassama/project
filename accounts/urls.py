from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # ログイン・ログアウト
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    # ユーザー登録・プロフィール関連
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('users/profile/', views.profile, name="profile"),
    path('users/profile_edit/', views.profile_edit, name="profile_edit"),

    # 投稿関連
    path('home/', views.home, name="home"),
    path('posts/', views.posts_index, name="posts_index"),
    path('create/', views.posts_create, name="create"),
    path('<int:post_id>/', views.posts_detail, name="posts_detail"),
    path('<int:post_id>/delete_post', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/comments', views.comments_create, name="comments_create"),

    # ユーザー一覧・詳細
    path('users/', views.users_index, name="users_index"),
    path('users/<int:user_id>/', views.users_detail, name="users_detail"),

    # ファイルアップロード
    path('upload/', views.upload_file, name='upload_file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)