from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Portfolio, Blog, Contact
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    portfolio_lists = Portfolio.objects.all()[:3]
    blog_lists = Blog.objects.all().order_by('-created_at')[:3]
    context = {
        'portfolio_lists': portfolio_lists,
        'blog_lists': blog_lists,
    }

    return render(request, 'portfolio/home.html', context)


def about(request):
    return render(request, 'portfolio/about.html')


def portfolio(request):
    portfolio_lists = Portfolio.objects.all()
    context = {
        'portfolio_lists': portfolio_lists,
    }
    return render(request, 'portfolio/portfolio.html', context)


def blogs_page(request):
    blog_lists = Blog.objects.all().order_by('-created_at')
    context = {
        'blog_lists': blog_lists,
    }
    return render(request, 'portfolio/blogs_page.html', context)


def detailed_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    context = {
        'blog': blog,
    }
    return render(request, 'portfolio/detailed_blog.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Create a new Contact object with the provided data
        Contact.objects.create(name=name, email=email, message=message)

        # Add a success message to the current request
        messages.success(request, 'Your message has been sent successfully')

        # Redirect the user to the 'contact' page
        return redirect('contact')

    # Render the 'contact.html' template if the request method is not 'POST'
    return render(request, 'portfolio/contact.html')


def signup(request):
    if request.method == 'POST':
        full_name = request.POST['name'].split()
        first_name = full_name[0]
        if len(full_name) == 1:
            last_name = ''
        if len(full_name) == 2:
            last_name = full_name[1]
        if len(full_name) > 2:
            last_name = full_name[1:]
            last_name = ' '.join(last_name)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                # Add an information message to the current request
                messages.info(request, 'Username already exists')

                # Redirect the user to the 'home' page
                return redirect('home')
            elif User.objects.filter(email=email).exists():
                # Add an information message to the current request
                messages.info(request, 'Email already exists')

                # Redirect the user to the 'home' page
                return redirect('home')
            else:
                # Create a new User object with the provided data
                user = User.objects.create_user(
                    username=username, password=password, email=email)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                # Add a success message to the current request
                messages.success(request, 'User created successfully')

                # Redirect the user to the 'home' page
                return redirect('home')

        else:
            # Add an information message to the current request
            messages.info(request, 'Password not matching')
            return redirect('home')

    # Return an HTTP response with the message "Page not found" if the request method is not 'POST'
    return render(request, 'portfolio/404_error.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user with the given username and password
        user = authenticate(username=username, password=password)

        # If the user is authenticated, log them in and redirect to the home page
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('home')
        # If the user is not authenticated, display an error message and redirect to the home page
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('home')

    # If the request method is not 'POST', render the 404 error page
    return render(request, 'portfolio/404_error.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('home')
