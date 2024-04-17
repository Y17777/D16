from django import forms
from django.forms import Textarea
from .models import Category, Bullets, Comment


class PostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 empty_label="Выберите категорию",
                                 label='Категории')

    class Meta:
        model = Bullets
        fields = ['title', 'content', 'photo', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'size': 100}),
            'content': forms.Textarea(attrs={'cols': 100, 'rows': 5}),
        }
        labels = {'pk': 'URL'}


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['text'].widget = Textarea(attrs={'rows': 5})


class CommentUserForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',
                  'commentAuthor']
        labels = {
            'text': 'Комментарий',
        }
        widgets = {
            'text': forms.Textarea(attrs={'cols': 100, 'rows': 2}),
        }
