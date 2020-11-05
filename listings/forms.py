from .models import Comment, VendorComment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('overall_rate', 'subject', 'comment')


class VendorCommentForm(forms.ModelForm):
    class Meta:
        model = VendorComment
        fields = ('overall_rate', 'subject', 'comment')