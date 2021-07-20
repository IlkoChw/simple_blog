from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'id': 'InputTitle'
            }))

    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'md-textarea form-control form-control-sm',
                'id': 'InputText',
                'rows': '3'
            }))

    class Meta:
        model = Post
        fields = ('title', 'text')
