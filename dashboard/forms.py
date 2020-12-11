from django import forms


class NewGroupCategoryForm(forms.Form):
    category_name = forms.CharField(label='Название категории', max_length=100, required=True)
    keyword_1 = forms.CharField(label='Тег 1', max_length=100, required=True)
    keyword_2 = forms.CharField(label='Тег 2', max_length=100, required=False)
    keyword_3 = forms.CharField(label='Тег 3', max_length=100, required=False)
