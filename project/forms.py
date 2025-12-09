# File: project/forms.py
# Author: Louise Lee, llouise@bu.edu 11/24/2025
# Description: Define forms that we use for creation/update/delete operations
# Forms for creating and updating digital desk items

from django import forms
from .models import Profile, TimerRecord, WaterLog, DiaryEntry, PhotoItem, StickyNote


class ProfileForm(forms.ModelForm):
    """Form to create/update user profile"""

    # Standard user profile includes their name, bio and default settings for pomodoro/water intake

    class Meta:
        model = Profile
        fields = [
            "display_name",
            "bio",
            "default_focus_minutes",
            "default_break_minutes",
            "daily_water_goal_ml",
        ]
        widgets = {
            "display_name": forms.TextInput(
                attrs={"placeholder": "Your display name", "class": "form-input"}
            ),
            "bio": forms.Textarea(
                attrs={
                    "placeholder": "About you: Set your goals, desires, anything you'd like!",
                    "rows": 4,
                    "class": "form-textarea",
                }
            ),
            "default_focus_minutes": forms.NumberInput(
                attrs={"min": 1, "max": 60, "class": "form-input"}
            ),
            "default_break_minutes": forms.NumberInput(
                attrs={"min": 1, "max": 30, "class": "form-input"}
            ),
            "daily_water_goal_ml": forms.NumberInput(
                attrs={"min": 500, "max": 5000, "step": 100, "class": "form-input"}
            ),
        }


class TimerRecordForm(forms.ModelForm):
    """Form to create a new timer/focus session"""

    # User set what they work on, how long the focus and break sessions are and number of cycles

    class Meta:
        model = TimerRecord
        fields = [
            "label",
            "focus_duration_minutes",
            "break_duration_minutes",
            "planned_cycles",
        ]
        widgets = {
            "label": forms.TextInput(
                attrs={"placeholder": "What are you working on?", "class": "form-input"}
            ),
            "focus_duration_minutes": forms.NumberInput(
                attrs={"min": 1, "max": 60, "class": "form-input"}
            ),
            "break_duration_minutes": forms.NumberInput(
                attrs={"min": 1, "max": 30, "class": "form-input"}
            ),
            "planned_cycles": forms.NumberInput(
                attrs={"min": 1, "max": 10, "class": "form-input"}
            ),
        }


class AddCyclesForm(forms.Form):
    """Form to add more cycles to existing timer"""

    # Allow user to add more cycles to their session

    additional_cycles = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        label="Want additional cycles?",
        widget=forms.NumberInput(
            attrs={"placeholder": "How many", "class": "form-input"}
        ),
    )


# ----- WATER LOG FORMS -----


class WaterLogForm(forms.ModelForm):
    """Form to CREATE a water log (user can pick date)"""

    # Extra helper: amount to set as starting intake
    add_amount = forms.IntegerField(
        required=False,
        min_value=50,
        max_value=1000,
        initial=250,
        label="Add water (ml)",
        widget=forms.NumberInput(attrs={"placeholder": "250", "class": "form-input"}),
    )

    class Meta:
        model = WaterLog
        fields = ["date", "daily_goal_ml"]  # date + goal come from the model
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-input",
                }
            ),
            "daily_goal_ml": forms.NumberInput(
                attrs={
                    "min": 500,
                    "max": 5000,
                    "class": "form-input",
                }
            ),
        }


class WaterLogUpdateForm(forms.ModelForm):
    """Form to UPDATE a water log (date fixed; only goal + add water)."""

    add_amount = forms.IntegerField(
        required=False,
        min_value=50,
        max_value=1000,
        initial=250,
        label="Add water (ml)",
        widget=forms.NumberInput(attrs={"placeholder": "250", "class": "form-input"}),
    )

    class Meta:
        model = WaterLog
        fields = ["daily_goal_ml"]  # no 'date' here → user can't change it
        widgets = {
            "daily_goal_ml": forms.NumberInput(
                attrs={
                    "min": 500,
                    "max": 5000,
                    "class": "form-input",
                }
            ),
        }


class DiaryEntryForm(forms.ModelForm):
    """Form to create or update diary entries"""

    # Diary entry contains a title and content

    class Meta:
        model = DiaryEntry
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Entry title...", "class": "form-input"}
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Write your thoughts here...",
                    "rows": 8,
                    "class": "form-textarea",
                }
            ),
        }


class PhotoItemForm(forms.ModelForm):
    """Form to upload a photo to the desk"""

    # Picture to show on a desk

    class Meta:
        model = PhotoItem
        fields = ["image", "caption"]
        widgets = {
            "caption": forms.TextInput(
                attrs={"placeholder": "Optional caption...", "class": "form-input"}
            ),
        }


class StickyNoteForm(forms.ModelForm):
    """Form to create or update sticky notes"""

    # Stickynote title, content, due_date and if completed

    class Meta:
        model = StickyNote
        fields = ["title", "content", "due_date", "is_completed"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Note title...", "class": "form-input"}
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Note details...",
                    "rows": 4,
                    "class": "form-textarea",
                }
            ),
            "due_date": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }
