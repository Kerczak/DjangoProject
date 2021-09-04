from django.forms import (
    ModelForm, CharField, IntegerField
)
from viewer.models import Genre, Movie

from viewer.validators import PastMonthField, capitalized_validator

from django.core.exceptions import ValidationError

import re


class MovieForm(ModelForm):
    class Meta:  # subklasa opisująca dane z których tworzymy formularz
        model = Movie  # model na podstawie tworzymy formularz
        fields = '__all__'  # wykorzystujemy wszystkie pola z modelu

    title = CharField(validators=[capitalized_validator])
    rating = IntegerField(min_value=1, max_value=10)  # input type: number, min: 1, max: 10
    released = PastMonthField()  # input type: date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_description(self):
        initial = self.cleaned_data['description']  # pobranie wartości pola description
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')  # podział tekstu na części od kropki do kropki
        return '. '.join(sentence.capitalize() for sentence in sentences)  # zamiana na wielką literę pierwszej litery każdego zdania, dodanie kropki, powtórzenie operacji dla kolejnego zdania


    def clean(self):
        result = super().clean()
        if result['genre'].name == 'comedy' and result['rating'] > 7:
            # oznaczenie pola jako błędne bez komentarza
            self.add_error('genre', '')
            self.add_error('rating', '')
            # rzucamy ogólny błąd / wyjątek
            raise ValidationError(
                'Commedies aren\'t so good to be over 7'
            )
        return result
