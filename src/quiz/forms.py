from django import forms
from django.core.exceptions import ValidationError

from .models import Choice


class QuestionInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError(
                f'Questions count must be range '
                f'from {self.instance.QUESTION_MIN_LIMIT} '
                f'to {self.instance.QUESTION_MAX_LIMIT} inclusive'
            )

        order_num_count = list(form.cleaned_data['order_num'] for form in self.forms)
        for order in order_num_count:
            if order > 100:
                raise ValidationError('Order num is only in range from 1 to 100!')
            if order > len(self.forms):
                raise ValidationError('Order_num is bigger than count of questions!')
        lst_order = [i for i in range(1, len(self.forms) + 1)]
        if sorted(order_num_count) != lst_order:
            raise ValidationError('Not correct order num, check again')


class ChoiceInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        # lst = []
        # for form in self.forms:
        #     if form.cleaned_data['is_correct']:
        #         lst.append(1)
        #     else:
        #         lst.append(0)
        #
        # num_correct_answers = sum(lst)

        # num_correct_answers = sum(1 for form in self.forms if form.cleaned_data['is_correct'])

        num_correct_answers = sum(form.cleaned_data['is_correct'] for form in self.forms)

        if num_correct_answers == 0:
            raise ValidationError('Need to choose one option minimum')

        if num_correct_answers == len(self.forms):
            raise ValidationError('It is not allowed to select all options')


class ChoiceForm(forms.ModelForm):
    is_selected = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ('text',)


ChoicesFormSet = forms.modelformset_factory(
    model=Choice,
    form=ChoiceForm,
    extra=0
)
