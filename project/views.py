# File: project/views.py
# Author: Louise Lee, llouise@bu.edu 11/24/2025
# Description: Defines view function, handles rendering of the different pages by using
# context data
# View functions for digital desk app

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import date
import requests

from .models import (
    Profile,
    TimerRecord,
    WaterLog,
    DiaryEntry,
    PhotoItem,
    StickyNote,
    DeskBuddy,
)
from .forms import (
    ProfileForm,
    TimerRecordForm,
    AddCyclesForm,
    WaterLogForm,
    DiaryEntryForm,
    PhotoItemForm,
    StickyNoteForm,
)


class DeskView(LoginRequiredMixin, TemplateView):
    """Main desk view showing all desk items"""

    template_name = "project/desk.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        """Add additional context data"""
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        # Overall check if user has a profile already
        # If so, we can pull their defaults/continue from their activity

        # Get or create profile
        profile, created = Profile.objects.get_or_create(
            user=user, defaults={"display_name": user.username}
        )

        # Get today's water log or create one
        today_water, created = WaterLog.objects.get_or_create(
            user=user,
            date=date.today(),
            defaults={
                "total_intake_ml": 0,
                "daily_goal_ml": profile.daily_water_goal_ml,
            },
        )

        # Get active timer (if any)
        active_timer = TimerRecord.objects.filter(user=user, status="active").first()

        ctx["profile"] = profile
        ctx["sticky_notes"] = StickyNote.objects.filter(user=user, is_completed=False)[
            :5
        ]
        ctx["recent_timers"] = TimerRecord.objects.filter(
            user=user, status="completed"
        )[:3]
        ctx["active_timer"] = active_timer
        ctx["recent_diary"] = DiaryEntry.objects.filter(user=user).first()
        ctx["current_photo"] = PhotoItem.objects.filter(user=user).first()
        ctx["water_log"] = today_water
        ctx["unread_messages"] = DeskBuddy.objects.filter(
            user=user, is_read=False
        ).count()

        return ctx


# Profile Views
class ProfileDetailView(LoginRequiredMixin, DetailView):
    """View user profile with weekly statistics"""

    model = Profile
    template_name = "project/profile_detail.html"
    context_object_name = "profile"
    login_url = "login"

    def get_object(self):
        """Profile for the logged-in user"""
        profile, created = Profile.objects.get_or_create(
            user=self.request.user,
            defaults={"display_name": self.request.user.username},
        )
        return profile


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """View class to handle update of post based on PK"""

    model = Profile
    form_class = ProfileForm
    template_name = "project/update_profile.html"
    login_url = "login"

    def get_object(self):
        """Profile for the logged-in user"""
        profile, created = Profile.objects.get_or_create(
            user=self.request.user,
            defaults={"display_name": self.request.user.username},
        )
        return profile

    def get_success_url(self):
        """Redirect back to the updated profile page"""
        messages.success(self.request, "Profile updated successfully!")
        return reverse("profile_detail", kwargs={"pk": self.object.pk})


# Timer Views
class TimerListView(LoginRequiredMixin, ListView):
    """List all timer records"""

    model = TimerRecord
    template_name = "project/timer_list.html"
    context_object_name = "timers"
    login_url = "login"

    def get_queryset(self):
        return TimerRecord.objects.filter(user=self.request.user)


class TimerDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a single timer record"""

    model = TimerRecord
    template_name = "project/timer_detail.html"
    context_object_name = "timer"
    login_url = "login"

    def get_queryset(self):
        return TimerRecord.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Add additional context data"""
        ctx = super().get_context_data(**kwargs)
        ctx["add_cycles_form"] = AddCyclesForm()
        return ctx


class CreateTimerView(LoginRequiredMixin, CreateView):
    """Create a new timer/focus session"""

    model = TimerRecord
    form_class = TimerRecordForm
    template_name = "project/create_timer.html"
    login_url = "login"

    def get_initial(self):
        initial = super().get_initial()
        profile = Profile.objects.filter(user=self.request.user).first()
        if profile:
            initial["focus_duration_minutes"] = profile.default_focus_minutes
            initial["break_duration_minutes"] = profile.default_break_minutes
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "active"
        messages.success(self.request, "Timer session started! Good luck! 🎯")
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect back to timer detail"""
        return reverse("timer_detail", kwargs={"pk": self.object.pk})


class CompleteCycleView(LoginRequiredMixin, View):
    """Mark a cycle as completed"""

    login_url = "login"

    def post(self, request, pk):
        timer = get_object_or_404(
            TimerRecord, pk=pk, user=request.user, status="active"
        )
        timer.complete_cycle()

        if timer.status == "completed":
            messages.success(
                request,
                f"🎉 Congratulations! You completed all {timer.planned_cycles} cycles!",
            )
        else:
            remaining = timer.planned_cycles - timer.cycles_completed
            messages.success(
                request,
                f"Great work! Cycle {timer.cycles_completed} complete. {remaining} cycle(s) remaining.",
            )

        return redirect("timer_detail", pk=timer.pk)


class AddCyclesView(LoginRequiredMixin, View):
    """Add more cycles to an active timer"""

    login_url = "login"

    def post(self, request, pk):
        timer = get_object_or_404(TimerRecord, pk=pk, user=request.user)
        form = AddCyclesForm(request.POST)

        if form.is_valid():
            additional = form.cleaned_data["additional_cycles"]
            timer.planned_cycles += additional

            # If timer was completed, reactivate it
            if timer.status == "completed":
                timer.status = "active"

            timer.save()
            messages.success(
                request, f"Added {additional} more cycle(s)! Keep going! 💪"
            )

        return redirect("timer_detail", pk=timer.pk)


class FinishTimerEarlyView(LoginRequiredMixin, View):
    """Finish timer session early"""

    login_url = "login"

    def post(self, request, pk):
        timer = get_object_or_404(
            TimerRecord, pk=pk, user=request.user, status="active"
        )
        timer.finish_early()

        messages.info(
            request,
            f"Session ended. You completed {timer.cycles_completed} cycle(s). Great effort! 👏",
        )
        return redirect("timer_detail", pk=timer.pk)


class CancelTimerView(LoginRequiredMixin, View):
    """Cancel an active timer"""

    login_url = "login"

    def post(self, request, pk):
        timer = get_object_or_404(
            TimerRecord, pk=pk, user=request.user, status="active"
        )
        timer.cancel()

        messages.info(request, "Timer session cancelled.")
        return redirect("timer_list")


class DeleteTimerView(LoginRequiredMixin, DeleteView):
    """Delete a timer record"""

    model = TimerRecord
    template_name = "project/delete_timer.html"
    success_url = reverse_lazy("timer_list")
    login_url = "login"

    def get_queryset(self):
        return TimerRecord.objects.filter(user=self.request.user)


# Water Log Views
class WaterLogListView(LoginRequiredMixin, ListView):
    """List all water logs"""

    model = WaterLog
    template_name = "project/water_log_list.html"
    context_object_name = "water_logs"
    login_url = "login"

    def get_queryset(self):
        return WaterLog.objects.filter(user=self.request.user)


class WaterLogDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a water log"""

    model = WaterLog
    template_name = "project/water_log_detail.html"
    context_object_name = "water_log"
    login_url = "login"

    def get_queryset(self):
        return WaterLog.objects.filter(user=self.request.user)


class UpdateWaterLogView(LoginRequiredMixin, View):
    """Update today's water intake"""

    login_url = "login"

    def post(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        water_log, created = WaterLog.objects.get_or_create(
            user=request.user,
            date=date.today(),
            defaults={
                "total_intake_ml": 0,
                "daily_goal_ml": profile.daily_water_goal_ml if profile else 2000,
            },
        )

        form = WaterLogForm(request.POST, instance=water_log)
        if form.is_valid():
            add_amount = form.cleaned_data.get("add_amount", 0)
            if add_amount:
                water_log.total_intake_ml += add_amount
            water_log.daily_goal_ml = form.cleaned_data["daily_goal_ml"]
            water_log.save()
            messages.success(request, f"Added {add_amount}ml of water! 💧")

        return redirect("desk")


# Diary Views
class DiaryListView(LoginRequiredMixin, ListView):
    """List all diary entries"""

    model = DiaryEntry
    template_name = "project/diary_list.html"
    context_object_name = "entries"
    login_url = "login"

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)


class DiaryDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a diary entry"""

    model = DiaryEntry
    template_name = "project/diary_detail.html"
    context_object_name = "entry"
    login_url = "login"

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)


class CreateDiaryEntryView(LoginRequiredMixin, CreateView):
    """Create a new diary entry"""

    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = "project/create_diary.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Diary entry created! ✍️")
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect back to the list of entries"""
        return reverse("diary_list")


class UpdateDiaryEntryView(LoginRequiredMixin, UpdateView):
    """Update an existing diary entry"""

    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = "project/update_diary.html"
    login_url = "login"

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)

    def get_success_url(self):
        """Redirect back to the diary entry"""
        return reverse("diary_detail", kwargs={"pk": self.object.pk})


class DeleteDiaryEntryView(LoginRequiredMixin, DeleteView):
    """Delete a diary entry"""

    model = DiaryEntry
    template_name = "project/delete_diary.html"
    success_url = reverse_lazy("diary_list")
    login_url = "login"

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)


# Photo Views
class PhotoListView(LoginRequiredMixin, ListView):
    """List all photos"""

    model = PhotoItem
    template_name = "project/photo_list.html"
    context_object_name = "photos"
    login_url = "login"

    def get_queryset(self):
        return PhotoItem.objects.filter(user=self.request.user)


class PhotoDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a photo"""

    model = PhotoItem
    template_name = "project/photo_detail.html"
    context_object_name = "photo"
    login_url = "login"

    def get_queryset(self):
        return PhotoItem.objects.filter(user=self.request.user)


class CreatePhotoView(LoginRequiredMixin, CreateView):
    """Upload a new photo"""

    model = PhotoItem
    form_class = PhotoItemForm
    template_name = "project/create_photo.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Photo added to your desk! 📷")
        return super().form_valid(form)

    def get_success_url(self):
        """Show photo on the desk"""
        return reverse("desk")


class DeletePhotoView(LoginRequiredMixin, DeleteView):
    """Delete a photo"""

    model = PhotoItem
    template_name = "project/delete_photo.html"
    success_url = reverse_lazy("photo_list")
    login_url = "login"

    def get_queryset(self):
        return PhotoItem.objects.filter(user=self.request.user)


# Sticky Note Views
class StickyNoteListView(LoginRequiredMixin, ListView):
    """List all sticky notes"""

    model = StickyNote
    template_name = "project/sticky_note_list.html"
    context_object_name = "notes"
    login_url = "login"

    def get_queryset(self):
        return StickyNote.objects.filter(user=self.request.user)


class StickyNoteDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a sticky note"""

    model = StickyNote
    template_name = "project/sticky_note_detail.html"
    context_object_name = "note"
    login_url = "login"

    def get_queryset(self):
        return StickyNote.objects.filter(user=self.request.user)


class CreateStickyNoteView(LoginRequiredMixin, CreateView):
    """Create a new sticky note"""

    model = StickyNote
    form_class = StickyNoteForm
    template_name = "project/create_sticky_note.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Sticky note created! 📝")
        return super().form_valid(form)

    def get_success_url(self):
        """Show sticky note on desk"""
        return reverse("desk")


class UpdateStickyNoteView(LoginRequiredMixin, UpdateView):
    """Update an existing sticky note"""

    model = StickyNote
    form_class = StickyNoteForm
    template_name = "project/update_sticky_note.html"
    login_url = "login"

    def get_queryset(self):
        return StickyNote.objects.filter(user=self.request.user)

    def get_success_url(self):
        """Redirect back to the list of sticky notes"""
        return reverse("sticky_note_list")


class DeleteStickyNoteView(LoginRequiredMixin, DeleteView):
    """Delete a sticky note"""

    model = StickyNote
    template_name = "project/delete_sticky_note.html"
    success_url = reverse_lazy("sticky_note_list")
    login_url = "login"

    def get_queryset(self):
        return StickyNote.objects.filter(user=self.request.user)


class ToggleStickyNoteView(LoginRequiredMixin, View):
    """Toggle completion status of a sticky note"""

    login_url = "login"

    def post(self, request, pk):
        note = get_object_or_404(StickyNote, pk=pk, user=request.user)
        note.is_completed = not note.is_completed
        note.save()

        status = "completed" if note.is_completed else "reopened"
        messages.success(
            request,
            (
                f'Note "{note.title}" {status}! ✓'
                if note.is_completed
                else f'Note "{note.title}" {status}!'
            ),
        )

        return redirect(request.META.get("HTTP_REFERER", "desk"))


# Desk Buddy Views
class DeskBuddyView(LoginRequiredMixin, ListView):
    """View all desk buddy messages"""

    model = DeskBuddy
    template_name = "project/desk_buddy.html"
    context_object_name = "messages"
    login_url = "login"

    def get_queryset(self):
        # Mark all as read when viewing
        DeskBuddy.objects.filter(user=self.request.user, is_read=False).update(
            is_read=True
        )
        return DeskBuddy.objects.filter(user=self.request.user)


class GetDeskBuddyMessageView(LoginRequiredMixin, View):
    """Get randomized message: water reminder, sticky note reminder, or API affirmation"""

    login_url = "login"

    def get(self, request):
        user = request.user
        message = None

        # Get user's current water status
        today_water = WaterLog.objects.filter(user=user, date=date.today()).first()
        water_needed = today_water and today_water.get_percentage_complete() < 100

        # Get uncompleted sticky notes
        incomplete_notes = StickyNote.objects.filter(user=user, is_completed=False)
        has_tasks = incomplete_notes.exists()

        # Build list of available message types
        available_types = []
        if water_needed:
            available_types.append("water")
        if has_tasks:
            available_types.append("task")
        available_types.append("affirmation")  # Always available

        # Randomly choose a message type
        import random

        message_type = random.choice(available_types)

        # Generate message based on type
        if message_type == "water" and water_needed:
            remaining = today_water.daily_goal_ml - today_water.total_intake_ml
            message = f"💧 Don't forget to hydrate! You need {remaining}ml more to reach your daily goal. Stay healthy!"

        elif message_type == "task" and has_tasks:
            # Pick a random incomplete task
            random_note = random.choice(incomplete_notes)
            message = f"📝 Reminder: Don't forget about '{random_note.title}'! Time to get it done!"

        else:  # affirmation from API
            try:
                # Call the affirmations API
                response = requests.get("https://www.affirmations.dev/", timeout=5)
                response.raise_for_status()
                data = response.json()
                message = data.get("affirmation", "You are doing great! Keep going! 🌟")
            except requests.RequestException:
                # Fallback affirmations if API fails
                fallback_affirmations = [
                    "You are capable of amazing things! Believe in yourself! ✨",
                    "Every small step forward is progress. Keep going! 🚀",
                    "Your hard work and dedication will pay off! 💪",
                    "You have the power to create positive change! 🌟",
                    "Take a moment to appreciate how far you've come! 🎉",
                ]
                message = random.choice(fallback_affirmations)

        # Save to database
        buddy_message = DeskBuddy.objects.create(user=user, affirmation=message)

        return JsonResponse({"message": message, "id": buddy_message.pk})
