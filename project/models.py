# File: project/models.py
# Author: Louise Lee, llouise@bu.edu, 11/24/2025
# Description: Models define the fields (columns) of database, specifying data types, values, rules
# Data models for digital desk productivity and wellness app

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone


class Profile(models.Model):
    """User profile with productivity statistics"""

    # Attach extra fields (display_name, preferences, stats) to each user
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="desk_profile"
    )

    # Optional name shown in the UI
    display_name = models.CharField(max_length=100, blank=True)

    # Bio of user
    bio = models.TextField(blank=True, help_text="A little about yourself")

    # When this profile was created (set automatically)
    created_at = models.DateTimeField(auto_now_add=True)

    # Default Pomodoro preferences
    default_focus_minutes = models.IntegerField(default=25)
    default_break_minutes = models.IntegerField(default=5)

    # Default daily water goal used for WaterLogs (in ml)
    daily_water_goal_ml = models.IntegerField(default=2000)

    class Meta:
        # Newest profiles first
        ordering = ["-created_at"]

    def __str__(self):
        # Indicate this is user's profile
        return f"{self.user.username}'s Profile"

    def get_absolute_url(self):
        # L ink to a Profile detail page
        return reverse("profile_detail", kwargs={"pk": self.pk})

    # -----------------------
    #
    # Weekly statistics helpers
    #
    # -----------------------

    def get_week_start(self):
        """Get the start of the current week (Monday) for the logged-in user."""
        today = timezone.now().date()
        # weekday: Monday = 0, Sunday = 6 → subtract offset to get Monday
        return today - timedelta(days=today.weekday())

    def get_weekly_focus_minutes(self):
        """Total focus minutes this week across completed timers."""
        week_start = self.get_week_start()
        # Filter: user, starting on/after week_start, and completed
        timers = TimerRecord.objects.filter(
            user=self.user, start_time__date__gte=week_start, status="completed"
        )
        # Each cycle contributes focus_duration_minutes
        total = sum(t.focus_duration_minutes * t.cycles_completed for t in timers)
        return total

    def get_weekly_tasks_completed(self):
        """Number of sticky notes completed this week."""
        week_start = self.get_week_start()
        # Count completed StickyNotes where updated_at is during this week
        return StickyNote.objects.filter(
            user=self.user, is_completed=True, updated_at__date__gte=week_start
        ).count()

    def get_weekly_diary_entries(self):
        """Number of diary entries written this week."""
        week_start = self.get_week_start()
        return DiaryEntry.objects.filter(user=self.user, date__gte=week_start).count()

    def get_weekly_water_average(self):
        """Average daily water intake (ml) this week."""
        week_start = self.get_week_start()
        logs = WaterLog.objects.filter(user=self.user, date__gte=week_start)
        if not logs.exists():
            # No logs so average is 0
            return 0
        # Sum water intake and divide by number of days with logs
        return sum(log.total_intake_ml for log in logs) / logs.count()

    def get_total_focus_time(self):
        """Total focus time (minutes) across all completed sessions."""
        timers = TimerRecord.objects.filter(user=self.user, status="completed")
        return sum(t.focus_duration_minutes * t.cycles_completed for t in timers)

    def get_total_tasks_completed(self):
        """Total number of StickyNotes marked as completed all time."""
        return StickyNote.objects.filter(user=self.user, is_completed=True).count()


class TimerRecord(models.Model):
    """Records Pomodoro-style focus sessions for a user"""

    # Possible states for a timer
    STATUS_CHOICES = [
        ("active", "Active"),  # user is currently working through cycles
        ("completed", "Completed"),  # all planned cycles finished or ended early
        ("cancelled", "Cancelled"),  # user cancelled the session
    ]

    # Link each timer to the user who owns it
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="timer_records"
    )

    # Optional description of the task (shown in UI)
    label = models.CharField(
        max_length=200, blank=True, help_text="What are you working on?"
    )

    # When this timer was created / started (set automatically once)
    start_time = models.DateTimeField(auto_now_add=True)

    # Length of one focus cycle in minutes
    focus_duration_minutes = models.IntegerField(
        default=25, help_text="Focus time per cycle"
    )

    # Length of one break in minutes
    break_duration_minutes = models.IntegerField(
        default=5, help_text="Break time per cycle"
    )

    # How many cycles the user planned to complete for this session
    planned_cycles = models.IntegerField(
        default=1, help_text="Number of cycles planned"
    )

    # How many cycles have actually been completed so far
    cycles_completed = models.IntegerField(
        default=0, help_text="Number of cycles completed"
    )

    # Current status of the timer (active/completed/cancelled)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    # When the timer was completed or cancelled (optional; set by helper methods)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Show most recently started timers first
        ordering = ["-start_time"]

    def __str__(self):
        # Show username, label (or generic name), and date in admin
        return f"{self.user.username} - {self.label or 'Focus Session'} ({self.start_time.strftime('%m/%d/%Y')})"

    def get_absolute_url(self):
        # Link to timer detail page
        return reverse("timer_detail", kwargs={"pk": self.pk})

    # -------------
    #
    # State helpers
    #
    # -------------

    def complete_cycle(self):
        """Mark one more cycle as completed; auto-complete timer if all cycles are done."""
        # Increment completed cycles
        self.cycles_completed += 1

        # If we've reached or exceeded planned cycles, mark timer as completed
        if self.cycles_completed >= self.planned_cycles:
            self.status = "completed"
            # Record when the timer actually finished
            self.completed_at = timezone.now()

        # Save changes to the database
        self.save()

    def finish_early(self):
        """User finishes the session early but still considers it 'completed'."""
        self.status = "completed"
        self.completed_at = timezone.now()
        self.save()

    def cancel(self):
        """Cancel the session before completion."""
        self.status = "cancelled"
        # We still record a timestamp for when the cancellation happened
        self.completed_at = timezone.now()
        self.save()

    def get_total_focus_minutes(self):
        """Calculate total completed focus time for this session (in minutes)."""
        # Only counts completed cycles, not planned ones
        return self.focus_duration_minutes * self.cycles_completed


class WaterLog(models.Model):
    """Tracks daily water intake for a user"""

    # Which user this water log belongs to
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="water_logs")

    # Date of this log automatically set to the date when the record is created
    date = models.DateField(auto_now_add=True)

    # Total water the user drank that day (ml)
    total_intake_ml = models.IntegerField(
        default=0, help_text="Total water consumed (ml)"
    )

    # Target water goal for that day (ml)
    daily_goal_ml = models.IntegerField(default=2000, help_text="Daily water goal (ml)")

    class Meta:
        # Show most recent days first
        ordering = ["-date"]
        # Ensure there is only one log per user per date
        unique_together = ["user", "date"]

    def __str__(self):
        # Show user, data and fraction of goal
        return f"{self.user.username} - {self.date}: {self.total_intake_ml}/{self.daily_goal_ml}ml"

    def get_absolute_url(self):
        # Link to detail view for a single WaterLog
        return reverse("water_log_detail", kwargs={"pk": self.pk})

    def get_percentage_complete(self):
        """Calculate percentage of daily goal completed (0–100)."""
        if self.daily_goal_ml == 0:
            # Avoid division by zero; treat as 0% if goal is zero
            return 0
        # Cap at 100% in case user drinks more than their goal
        return min(100, (self.total_intake_ml / self.daily_goal_ml) * 100)


class DiaryEntry(models.Model):
    """Contains journal entries for reflection"""

    # Which user this entry belongs to
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="diary_entries"
    )

    # Date for the entry (automatically set when created)
    date = models.DateField(auto_now_add=True)

    # Short title displayed in lists
    title = models.CharField(max_length=200, help_text="Short title for your entry")

    # Main journal content
    content = models.TextField(help_text="Write your thoughts here")

    # Timestamps for creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Show most recent entries first
        ordering = ["-date"]
        verbose_name_plural = "Diary Entries"

    def __str__(self):
        # Show user - title, date of entry
        return f"{self.user.username} - {self.title} ({self.date})"

    def get_absolute_url(self):
        # Link to diary entry detail view
        return reverse("diary_detail", kwargs={"pk": self.pk})


class PhotoItem(models.Model):
    """Represents a photo displayed on the digital desk"""

    # Who owns the photo
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photos")

    # Uploaded image file (stored under media/desk_photos/)
    image = models.ImageField(upload_to="desk_photos/")

    # Optional caption shown under/near the photo
    caption = models.CharField(max_length=200, blank=True, help_text="Optional caption")

    # When the photo was added
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Newest photos first
        ordering = ["-date_added"]

    def __str__(self):
        # User's photo and date
        return f"{self.user.username}'s photo ({self.date_added.strftime('%m/%d/%Y')})"

    def get_absolute_url(self):
        # Link to photo detail view
        return reverse("photo_detail", kwargs={"pk": self.pk})


class StickyNote(models.Model):
    """Quick notes that appear as sticky notes on the desk"""

    # Available color choices for the sticky notes in the UI
    COLOR_CHOICES = [
        ("yellow", "Yellow"),
        ("pink", "Pink"),
        ("blue", "Blue"),
        ("green", "Green"),
        ("purple", "Purple"),
    ]

    # Which user this sticky note belongs to
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sticky_notes"
    )

    # Short title used to summarize the task/note
    title = models.CharField(max_length=100, help_text="Short title")

    # Optional longer text content for the note
    content = models.TextField(null=True, blank=True, help_text="Optional note content")

    # Visual color theme for the note
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default="yellow")

    # Optional due/reminder date for the note
    due_date = models.DateField(
        null=True, blank=True, help_text="Optional reminder date"
    )

    # Whether the user has completed this note/task
    is_completed = models.BooleanField(default=False)

    # When the note was created and last updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Order by completion first (incomplete at top), then newest first
        ordering = ["is_completed", "-created_at"]

    def __str__(self):
        # Add a checkmark or circle to show completion status in admin
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.title} - {self.user.username}"

    def get_absolute_url(self):
        # Link to sticky note detail view
        return reverse("sticky_note_detail", kwargs={"pk": self.pk})


class DeskBuddy(models.Model):
    """Tracks when user receives affirmations from the API"""

    # Which user this affirmation belongs to
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="desk_buddy_messages"
    )

    # The text of the affirmation (e.g., from an external API)
    affirmation = models.TextField(help_text="The affirmation message")

    # When the affirmation was created/received
    created_at = models.DateTimeField(auto_now_add=True)

    # Whether the user has seen/dismissed this message
    is_read = models.BooleanField(default=False)

    class Meta:
        # Show newest messages first
        ordering = ["-created_at"]
        verbose_name_plural = "Desk Buddy Messages"

    def __str__(self):
        # Example: "Affirmation for testuser1 at 11/24/2025 21:30"
        return f"Affirmation for {self.user.username} at {self.created_at.strftime('%m/%d/%Y %H:%M')}"

    def get_absolute_url(self):
        # Link to a detail view for a single DeskBuddy message
        return reverse("desk_buddy_detail", kwargs={"pk": self.pk})
