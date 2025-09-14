# File: quotes/views.py
# Author: Louise Lee, llouise@bu.edu, 09/07/2025
# Description: Defines view function, handles rendering of the different pages by using
# context data (e.g quotes, images, time)

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# List of quotes
QUOTES = [
    "A wise bear always keeps a marmalade sandwich in his hat in case of emergency.",
    "I'll never be like other people, but that's alright, because I'm a bear. A bear called Paddington.",
    "It's called a hard stare. My aunt taught me to do them when people had forgotten their manners.",
    "If we're kind and polite, the world will be right",
    "I'll never be like other people, but that's alright, because I'm a bear.",
]

# List of images
IMAGES = [
    "https://rwalley.com/wp-content/uploads/2016/11/1.jpg",
    "https://rwalley.com/wp-content/uploads/2019/09/RWA-PB-and-MrG3.jpg",
    "https://rwalley.com/wp-content/uploads/2019/09/RWA-PB-rain.jpg",
    "https://rwalley.com/wp-content/uploads/2019/09/RWA-PB2.jpg",
    "https://rwalley.com/wp-content/uploads/2016/11/2.jpg",
]

# Single image
IMAGE = "https://i.guim.co.uk/img/media/043451cedeb7aa3161e82b026d0173b655e98d48/0_66_3117_1870/master/3117.jpg?width=1010&quality=45&auto=format&fit=max&dpr=2&s=adc799bd938b03bf293073fef5ab8cd1"


# View functions for rendering each page
def home_page(request):
    """Display one quote and image"""

    template_name = "quotes/home.html"
    # Pick randomly from list and place into context dictionary, time
    context = {
        "quote": random.choice(QUOTES),
        "image": random.choice(IMAGES),
        "time": time.ctime(),
    }
    return render(request, template_name, context)


def show_all(request):
    """Display all quotes and images"""

    template_name = "quotes/show_all.html"
    # Pick randomly from list and place into context dictionary, time
    context = {
        "quotes": QUOTES,
        "images": IMAGES,
        "time": time.ctime(),
    }
    return render(request, template_name, context)


def about(request):
    """Respond to the URL 'about', delegate work to template."""

    template_name = "quotes/about.html"
    # Short text for biography, time
    context = {
        "bio": (
            "Paddington Bear is a fictional bear from Peru who is taken in by the Brown family at London's Paddington Station and brought to live with them.\n He is known for his love of marmalade, his blue duffle coat and hat, and his signature suitcase."
        ),
        "time": time.ctime(),
        "image": IMAGE,
    }
    return render(request, template_name, context)
