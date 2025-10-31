# File: voter_analytics/admin.py
# Author: Louise Lee, llouise@bu.edu, 10/28/2025
# Description: What models we give admin access to

from django.contrib import admin
from .models import Voter

admin.site.register(Voter)
