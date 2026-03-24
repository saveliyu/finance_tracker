from django import forms
from django.contrib.auth import get_user_model

from .models import Purchase, Category
import datetime


class PurchaseForm(forms.ModelForm):
    category = forms.ModelChoiceField(Category.objects.exclude(parent=None), empty_label='Категория',
                                      widget=forms.Select(
                                          attrs={'class': 'form-control', 'style': 'min-width: 100px;',
                                                 'class': 'form-control select-input'}))
    user = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(), empty_label=None,
        widget=forms.Select(attrs={'style': 'min-width: 70px;', 'class': 'form-control select-input'})
    )
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}))
    price = forms.DecimalField(decimal_places=2, max_digits=10, widget=forms.NumberInput(
        attrs={'type': "number", 'placeholder': "0", 'class': 'form-control'}))
    date = forms.DateField(
        initial=datetime.date.today,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'  # можно добавить класс для стилей
            }
        )
    )

    class Meta:
        model = Purchase
        fields = ('category', 'user', 'name', 'price', 'date')

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # делаем queryset только для текущего пользователя
        if current_user:
            self.fields['user'].queryset = get_user_model().objects.filter(pk=current_user.pk)
            self.fields['user'].initial = current_user


class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='Название категории')
    color = forms.CharField(label='Цвет категории',
                            widget=forms.DateInput(attrs={'type': 'color', 'class': 'color-input'}))
    parent = forms.ModelChoiceField(queryset=Category.objects.none(),
                                    empty_label='Эта категория будет родительской',
                                    label='Выберите родительскую категорию',
                                    widget=forms.Select(attrs={'class': 'select-input category-input'}), required=False)

    class Meta:
        model = Category
        fields = ('name', 'color')

    def __init__(self, *args, **kwargs):
        family = kwargs.pop('family', None)  # достаём family
        super().__init__(*args, **kwargs)

        if family:
            self.fields['parent'].queryset = Category.objects.filter(
                parent=None,
                family=family
            )
