import re
from datetime import date
from django.forms import (
    Form, CharField, ModelChoiceField, IntegerField, DateField, Textarea, ModelForm
)
from django.core.exceptions import ValidationError

from .models import Genre, Movie


# A validator that is not related to a certain Filed type nor to a certain field
def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError('Value must be capitalized.')


def no_special_char_validator(value):
    forbidden = "#!%&/()=?@"
    if any(c in value for c in forbidden):
        raise ValidationError("You can't use special characters.")


# We will create our own Field Type
class PastMonthField(DateField):
    def validate(self, value):
        # The usual validation for the field DateField
        # If you write an date that is not valid, an exception will be raised
        super().validate(value)

        # Then if the date you write is valid, we do our own validations
        # Then the added customised validation we want to have
        if value >= date.today():
            raise ValidationError('You cannot add movies from the future.')

    def clean(self, value):
        # Get the cleaned date value
        result = super().clean(value)  # date(year=2007, month=10, day=25)

        # Change the date value to the first day of the month
        return date(year=result.year, month=result.month, day=1)


# class MovieForm(Form):
#     title = CharField(max_length=128, validators=[capitalized_validator, no_special_char_validator])
#     genre = ModelChoiceField(queryset=Genre.objects)
#     rating = IntegerField(min_value=1, max_value=10)
#     released = PastMonthField()
#     description = CharField(widget=Textarea, required=False)
#
#     # There is a difference between validation and cleaning
#     # Validation is the process of checking that what the client (the user of your
#     # website) wrote in the form is in the correct format.
#
#     # The cleaning happens after the form has been validated.
#     # The cleaning is a way you define your server to process the data.
#     # After your server cleans the data, it's ready to be user:
#     # Either to be written in the DB, or to be sent through some API, or ...
#     def clean_description(self):
#         """
#         This method is special for the field "description"
#         This cleans the filed description after it has been validated
#         :return:
#         """
#         # Force each sentence of the description to be capitalized.
#         initial = self.cleaned_data['description']
#         sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
#         return '. '.join(sentence.capitalize() for sentence in sentences)
#
#     def clean(self):
#         """
#         This is a clean method related to the entire form. -
#         It is not attached to a certain field
#
#         You can also add a validation for the entire form here
#         Or you can just your data
#         """
#         result = super().clean()
#         if result['genre'].name == 'Horror' and result['rating'] > 5:
#             # Raise validation error
#             # self.add_error('genre', "The genre can't be horror")
#             # self.add_error('rating', "The rating of a horror can't be more than 5")
#             # raise ValidationError(
#             #     "Horror movies are usually bad. You can't rate it over 5."
#             # )
#
#             # Clean the data instead of raising a validation error
#             result['rating'] = 5
#         return result


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        exclude = []

    # This overriding the fields that were automatically generated
    title = CharField(validators=[capitalized_validator, no_special_char_validator])
    rating = IntegerField(min_value=1, max_value=10)
    released = PastMonthField()

    def clean_description(self):
        # Force each sentence of the description to be capitalized.
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        cleaned = '. '.join(sentence.capitalize() for sentence in sentences)
        self.cleaned_data['description'] = cleaned
        return cleaned

    def clean(self):
        result = super().clean()
        if result['genre'].name == 'Horror' and result['rating'] > 5:
            raise ValidationError(
                "Horror movies are usually bad. And they don't deserve more than 5 points"
            )
        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = "__all__"


