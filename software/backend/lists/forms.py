from django import forms
from lists.models import Item

EMPTY_ITEM_ERROR = "you can't have an empty item"


class text_form(forms.Form):
    class Meta:
        model = Item
        fields = ('text')
        widgets = {'text': forms.fields.TextInput(attrs={'placeholder': 'Enter a to-do item',
                                                         'class': 'form-control input-lg'})}
        error_messages = {
            'text': {'required': "You can't have an empty list item"}
        }