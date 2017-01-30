from django import forms

class FileForm(forms.Form):
    file = forms.FileField(widget=forms.fields.ClearableFileInput(
        attrs={'placeholder': 'Select file to upload', 'class': 'form-control '}))
