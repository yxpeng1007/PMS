from django import forms
from ..models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "name",
            "day_of_week",
            "time_slot",
            "color",
        ]  # 使用模型中的字段

    DAY_OF_WEEK_CHOICES = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    ]

    TIME_SLOT_CHOICES = [
        (1, "1st Period"),
        (2, "2nd Period"),
        (3, "3rd Period"),
        (4, "4th Period"),
        (5, "5th Period"),
        (6, "6th Period"),
        (7, "7th Period"),
        (8, "8th Period"),
    ]

    day_of_week = forms.ChoiceField(
        choices=DAY_OF_WEEK_CHOICES, label="Day of the Week"
    )
    time_slot = forms.ChoiceField(choices=TIME_SLOT_CHOICES, label="Time Slot")
