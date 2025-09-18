# File: views/views.py
# Author: Louise Lee, llouise@bu.edu, 09/14/2025
# Description: Defines view function, handles rendering of the different pages by using
# context data (e.g lists/tables, images, time)
# pages: main (basic info), order (form), confirmation (process submitted order, display confirmation)

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# List of daily specials
SPECIALS = [
    "Signature sauce",
    "Rose sauce",
    "Mala sauce",
    "Teriyaki sauce",
]

# Standard prices
SPECIAL_PRICE = 2
WING_PRICE = 15


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
    # Variable to hold template - delegate work to display template
    template_name = "restaurant/order.html"

    # Pick special randomly from list and place into context dictionary, time
    context = {
        "special": random.choice(SPECIALS),
    }
    return render(request, template_name, context)


def confirmation(request):
    """Process form submission, generate confirmation of submitted order"""
    # Variable to hold template - delegate work to display template
    template_name = "restaurant/confirmation.html"
    print(request.POST)

    # Check if POST data was sent with HTTP POST msg:
    if request.POST:
        # Initiate cost and item list
        items = []
        cost = 0

        # Extract form fields into variables:
        # Special
        if "special" in request.POST:
            item = request.POST["special"]
            price = 2
            items.append(item)
            cost += price

        # Wings
        # Loop through the multiple checkbox options
        for w in request.POST.getlist("wings"):
            # If hot spicy wings selected, include spiciness option in list
            if w == "hot":
                spice = request.POST.get("hot_spice", "same")
                items.append(f"Hot spicy wings ({spice})")
                cost += WING_PRICE

            # Other wings, check selection then add the flavor to the item list
            # Add $15 if item selected
            elif w == "golden":
                items.append("Golden original wings")
                cost += WING_PRICE
            elif w == "cheesling":
                items.append("Cheesling wings")
                cost += WING_PRICE
            elif w == "honey":
                items.append("Honey garlic wings")
                cost += WING_PRICE
            elif w == "soy":
                items.append("Soy garlic wings")
                cost += WING_PRICE

        # Sides
        # Look up name and append item and cost if exist
        # Append item to list and increment cost
        for s in request.POST.getlist("sides"):
            if s == "radish":
                items.append("Pickled radish")
                cost += 1
            elif s == "rice":
                items.append("Steamed rice")
                cost += 2
            elif s == "coleslaw":
                items.append("Cole slaw")
                cost += 4
            elif s == "fries":
                items.append("French fries")
                cost += 7
            elif s == "sticks":
                items.append("Cheese sticks")
                cost += 8

        # Contact info
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        instructions = request.POST["instructions"]

        # Ready time: random value between 30-60mins
        minutes = random.randint(30, 60)
        future = time.time() + minutes * 60
        ready = time.ctime(future)

        # Create dictionary - context variables for use in template
        context = {
            "items": items,
            "cost": cost,
            "ready": ready,
            "minutes": minutes,
            "name": name,
            "phone": phone,
            "email": email,
            "instructions": instructions,
        }

    # Delegate response to template, provide context variables
    # Render confirmation page w these context variables
    return render(request, template_name=template_name, context=context)
