from django import forms
from .models import Article, Category, Comment

class NewArticleForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    title = forms.CharField(max_length=100, required=False)
    content = forms.Field(required=False, widget=forms.Textarea)
    class Meta:
        model = Article
        fields = ['title', 'content', 'category']

class CommentForm(forms.ModelForm):
    content = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}))
    class Meta:
        model = Comment
        fields = ['content']

class EditArticleForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    class Meta:
        model = Article
        fields = ['title', 'content', 'category']
        labels = {
            'title': 'Tytuł',
            'content': 'Treść',
            'category': 'Kategoria'
        }
