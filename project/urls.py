# File: project/urls.py
# Author: Louise Lee, llouise@bu.edu, 11/24/2025
# Description: URL routing for digital desk app

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    # Main desk view
    path("", DeskView.as_view(), name="desk"),
    # Desk Buddy URLs
    path("buddy/message/", GetDeskBuddyMessageView.as_view(), name="get_buddy_message"),
    # Profile URLs
    path("profile/", ProfileDetailView.as_view(), name="profile_detail"),
    path("profile/update/", UpdateProfileView.as_view(), name="update_profile"),
    # Timer URLs
    path("timer/", TimerListView.as_view(), name="timer_list"),
    path("timer/<int:pk>/", TimerDetailView.as_view(), name="timer_detail"),
    path("timer/create/", CreateTimerView.as_view(), name="create_timer"),
    path("timer/<int:pk>/delete/", DeleteTimerView.as_view(), name="delete_timer"),
    path(
        "timer/<int:pk>/complete-cycle/",
        CompleteCycleView.as_view(),
        name="complete_cycle",
    ),
    path("timer/<int:pk>/add-cycles/", AddCyclesView.as_view(), name="add_cycles"),
    path(
        "timer/<int:pk>/finish-early/",
        FinishTimerEarlyView.as_view(),
        name="finish_timer_early",
    ),
    path("timer/<int:pk>/cancel/", CancelTimerView.as_view(), name="cancel_timer"),
    # Water Log URLs
    path("water/", WaterLogListView.as_view(), name="water_log_list"),
    path("water/create/", CreateWaterLogView.as_view(), name="create_water_log"),
    path("water/<int:pk>/", WaterLogDetailView.as_view(), name="water_log_detail"),
    path("water/update/", UpdateWaterLogView.as_view(), name="update_water_log"),
    path(
        "water/<int:pk>/update/",
        UpdateWaterLogDetailView.as_view(),
        name="update_water_log_detail",
    ),
    path(
        "water/<int:pk>/delete/", DeleteWaterLogView.as_view(), name="delete_water_log"
    ),
    # Diary URLs
    path("diary/", DiaryListView.as_view(), name="diary_list"),
    path("diary/<int:pk>/", DiaryDetailView.as_view(), name="diary_detail"),
    path("diary/create/", CreateDiaryEntryView.as_view(), name="create_diary"),
    path("diary/<int:pk>/update/", UpdateDiaryEntryView.as_view(), name="update_diary"),
    path("diary/<int:pk>/delete/", DeleteDiaryEntryView.as_view(), name="delete_diary"),
    # Photo URLs
    path("photos/", PhotoListView.as_view(), name="photo_list"),
    path("photos/<int:pk>/", PhotoDetailView.as_view(), name="photo_detail"),
    path("photos/create/", CreatePhotoView.as_view(), name="create_photo"),
    path("photos/<int:pk>/delete/", DeletePhotoView.as_view(), name="delete_photo"),
    # Sticky Note URLs
    path("notes/", StickyNoteListView.as_view(), name="sticky_note_list"),
    path("notes/<int:pk>/", StickyNoteDetailView.as_view(), name="sticky_note_detail"),
    path("notes/create/", CreateStickyNoteView.as_view(), name="create_sticky_note"),
    path(
        "notes/<int:pk>/update/",
        UpdateStickyNoteView.as_view(),
        name="update_sticky_note",
    ),
    path(
        "notes/<int:pk>/delete/",
        DeleteStickyNoteView.as_view(),
        name="delete_sticky_note",
    ),
    path(
        "notes/<int:pk>/toggle/",
        ToggleStickyNoteView.as_view(),
        name="toggle_sticky_note",
    ),
    # Authentication URLs
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="project/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="desk"), name="logout"),
    path("create_profile/", CreateProfileView.as_view(), name="create_profile"),
]
