# File: formdata/templates/formdata/views.py
# Name: Louise
# Description:
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def show_form(request):
    """Show form to the user"""

    # Variable to hold template - delegate work to display template
    template_name = "formdata/form.html"
    return render(request, template_name)


def submit(request):
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

    # delegate response to template, provide context variables
    return render(request, template_name=template_name, context=context)
