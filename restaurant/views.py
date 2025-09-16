# File: views/views.py
# Author: Louise Lee, llouise@bu.edu, 09/14/2025
# Description: Defines view function, handles rendering of the different pages by using
# context data (e.g lists/tables, images, time)

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random


# View functions for rendering each page
def main_page(request):
    """Display basic details of restaurant"""
    # Variable to hold template - delegate work to display template
    template_name = "restaurant/main.html"

    # Pick randomly from list and place into context dictionary, time
    context = {
        "outside": "https://lh3.googleusercontent.com/p/AF1QipMgxQYQTgNytKWvuLqU5WdAxm37FKgTIVe2ls1p=s1360-w1360-h1020-rw",
        "inside": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4noG0M6rCJYtmtlQQ2697DkCoy17EtHbGQLOD3MxZzRUJsaB0w3vpaa7lFuGS2FcoKU6nVfQPp0Xn9Dzi7Ccx7eJA08_dTHa5f8vSUlt4hL6v1E-D3dBwvQwyzbbgSR3W8ZhF50E8A=s1360-w1360-h1020-rw",
        "feast": "https://cdn.asp.events/CLIENT_Comexpos_0322E963_F4B5_73A7_0954F2A7F5928375/sites/IFE-2025/media/libraries/exhibitors/1bcfc150-678c-11ed-b1330a410bd8e1d9-cover-image.png/fit-in/1500x9999/filters:no_upscale()",
        "chicken": "https://lh3.googleusercontent.com/p/AF1QipPz2ZQbDQFcCsjEPWXmiHF84XNrlAX1kTktBhYc=s1360-w1360-h1020-rw",
    }
    return render(request, template_name, context)


def order(request):
    """Form to order food"""
    template_name = "formdata/form.html"

    return render(request, template_name)


def confirmation(request):
    """Process form submission, generate result"""

    template_name = "formdata/confirmation.html"
    print(request.POST)

    # check it POST data was sent with HTTP POST msg:
    if request.POST:
        # extract form fields into variables:
        name = request.POST["name"]
        favorite_color = request.POST["favorite_color"]

        # Create dictionary - context variables for use in template
        context = {
            "name": name,
            "favorite_color": favorite_color,
        }

    # Delegate response to template, provide context variables
    return render(request, template_name=template_name, context=context)
