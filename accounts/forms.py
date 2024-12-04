from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']  # 投稿に含めるフィールドを指定
        widgets = {
            'caption': forms.TextInput(attrs={
                'placeholder': 'キャプションを入力してください',
                'class': 'form-control',
            }),
        }
