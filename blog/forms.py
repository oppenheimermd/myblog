from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                                widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        # To create a from from a model, you just need to indicate 
        # which model to used to build the form.  Django introspects the 
        # model and build the form dynamically for you.
        model = Comment
        fields = ('name', 'email', 'body')