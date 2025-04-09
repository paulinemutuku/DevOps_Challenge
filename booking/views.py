import logging
from datetime import date, datetime, timedelta  

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone

from .forms import BookingForm, UserProfileForm, UserRegisterForm
from .models import Booking, FitnessClass, UserProfile

logger = logging.getLogger(__name__)


def home(request):
    upcoming_classes = FitnessClass.objects.filter(
        date__gte=timezone.now().date()
    ).order_by("date", "start_time")[:3]

    return render(request, "booking/index.html", {"classes": upcoming_classes})


def about(request):
    """View function for the about us page."""
    return render(request, "booking/about.html")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}! You can now log in."
            )

            try:
                current_site = request.META["HTTP_HOST"]
                site_url = (
                    f"{'https://' if request.is_secure() else 'http://'}{current_site}"
                )

                html_message = render_to_string(
                    "booking/emails/welcome_email.html",
                    {"user": user, "site_url": site_url},
                )

                plain_message = f"Hi {user.first_name},\n\nThank you for registering with our Fitness Class Booking System!"

                send_mail(
                    "Welcome to FitMe!",
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    html_message=html_message,
                    fail_silently=True,
                )
            except Exception as e:
                logger.warning(f"Failed to send welcome email: {str(e)}")

            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "booking/register.html", {"form": form})


@login_required
def classes(request):
    query = request.GET.get("query", "")
    category = request.GET.get("category", "")

    all_classes = FitnessClass.objects.all().order_by("date", "start_time")

    if query:
        all_classes = all_classes.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(instructor__icontains=query)
        )

    if category:
        all_classes = all_classes.filter(category=category)

    user_bookings = Booking.objects.filter(user=request.user).values_list(
        "fitness_class_id", flat=True
    )

    for fitness_class in all_classes:
        fitness_class.is_booked = fitness_class.id in user_bookings
        fitness_class.is_available = not fitness_class.is_full

    try:
        categories = FitnessClass.CATEGORY_CHOICES
    except AttributeError:
        categories = []

    featured_classes = all_classes[:2]
    initial_classes = all_classes[2:8]
    remaining_classes = all_classes[8:]

    context = {
        "featured_classes": featured_classes,
        "initial_classes": initial_classes,
        "remaining_classes": remaining_classes,
        "all_classes": all_classes,
        "categories": categories,
        "selected_category": category,
        "query": query,
        "has_more_classes": len(remaining_classes) > 0,
    }

    return render(request, "booking/classes.html", context)


@login_required
def load_more_classes(request):
    offset = int(
        request.GET.get("offset", 8)
    )  
    limit = int(request.GET.get("limit", 6))  

    classes = FitnessClass.objects.all().order_by("date", "start_time")[
        offset : offset + limit
    ]

    user_bookings = Booking.objects.filter(user=request.user).values_list(
        "fitness_class_id", flat=True
    )

    class_html = []
    for i, fitness_class in enumerate(classes):
        fitness_class.is_booked = fitness_class.id in user_bookings
        fitness_class.is_available = not fitness_class.is_full

        class_html.append(
            {
                "id": fitness_class.id,
                "name": fitness_class.name,
                "description": fitness_class.description,
                "date": str(fitness_class.date),
                "start_time": str(fitness_class.start_time),
                "end_time": str(fitness_class.end_time),
                "instructor": fitness_class.instructor,
                "is_full": fitness_class.is_full,
                "is_booked": fitness_class.is_booked,
            }
        )

    has_more = FitnessClass.objects.all().count() > offset + limit

    return JsonResponse(
        {"classes": class_html, "has_more": has_more, "next_offset": offset + limit}
    )


@login_required
def book_class(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            if Booking.objects.filter(
                user=request.user, fitness_class=fitness_class
            ).exists():
                messages.warning(
                    request, f"You have already booked {fitness_class.name}!"
                )
                return redirect("classes")

            if fitness_class.is_full:
                messages.warning(
                    request, f"Sorry, {fitness_class.name} is already full!"
                )
                return redirect("classes")

            booking = form.save(commit=False)
            booking.user = request.user
            booking.fitness_class = fitness_class
            booking.save()

            try:
                current_site = request.META["HTTP_HOST"]
                site_url = (
                    f"{'https://' if request.is_secure() else 'http://'}{current_site}"
                )

                html_message = render_to_string(
                    "booking/emails/booking_confirmation.html",
                    {"user": request.user, "booking": booking, "site_url": site_url},
                )

                plain_message = f"Hi {request.user.first_name},\n\nYour booking for {fitness_class.name} on {fitness_class.date} at {fitness_class.start_time} has been confirmed!"

                send_mail(
                    f"Your FitMe Booking Confirmation: {fitness_class.name}",
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    html_message=html_message,
                    fail_silently=True,
                )
            except Exception as e:
                logger.warning(f"Failed to send booking confirmation email: {str(e)}")

            messages.success(
                request, f"You have successfully booked {fitness_class.name}!"
            )
            return redirect("booking_confirmation", booking_id=booking.id)
    else:
        form = BookingForm()

    return render(
        request,
        "booking/book_class.html",
        {"form": form, "fitness_class": fitness_class},
    )


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        class_name = booking.fitness_class.name

        fitness_class = booking.fitness_class

        booking.delete()

        try:
            current_site = request.META["HTTP_HOST"]
            site_url = (
                f"{'https://' if request.is_secure() else 'http://'}{current_site}"
            )

            html_message = render_to_string(
                "booking/emails/booking_cancellation.html",
                {
                    "user": request.user,
                    "booking": {"fitness_class": fitness_class},
                    "site_url": site_url,
                },
            )

            plain_message = f"Hi {request.user.first_name},\n\nYour booking for {class_name} has been cancelled."

            send_mail(
                "FitMe Booking Cancellation",
                plain_message,
                settings.EMAIL_HOST_USER,
                [request.user.email],
                html_message=html_message,
                fail_silently=True,
            )
        except Exception as e:
            logger.warning(f"Failed to send booking cancellation email: {str(e)}")

        messages.success(request, f"Your booking for {class_name} has been cancelled.")
        return redirect("classes")

    return render(request, "booking/cancel_booking.html", {"booking": booking})


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "booking/booking_confirmation.html", {"booking": booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by(
        "fitness_class__date", "fitness_class__start_time"
    )

    print(f"Found {bookings.count()} bookings for user {request.user.username}")

    today = timezone.now().date()

    upcoming_bookings = [b for b in bookings if b.fitness_class.date >= today]
    upcoming_count = len(upcoming_bookings)

    total_hours = 0
    for booking in bookings:
        if hasattr(booking.fitness_class, "start_time") and hasattr(
            booking.fitness_class, "end_time"
        ):
            start_time = booking.fitness_class.start_time
            end_time = booking.fitness_class.end_time
            if start_time and end_time:
                # Calculate duration in hours
                duration = (
                    datetime.combine(date.min, end_time)
                    - datetime.combine(date.min, start_time)
                ).seconds / 3600
                total_hours += duration

    # Find favorite class type
    class_types = {}
    for booking in bookings:
        class_type = (
            booking.fitness_class.category
            if hasattr(booking.fitness_class, "category")
            else "Unknown"
        )
        if class_type in class_types:
            class_types[class_type] += 1
        else:
            class_types[class_type] = 1

    favorite_class = "None"
    if class_types:
        favorite_class = max(class_types, key=class_types.get)

    # Prepare context data
    context = {
        "bookings": bookings,
        "upcomingClasses": upcoming_count,
        "totalHours": round(total_hours),
        "favoriteClass": favorite_class,
        "today": today,
        # Ensure we always pass these values to avoid template errors
        "has_bookings": bookings.exists(),
    }

    return render(request, "booking/my_bookings.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("profile")
    else:
        user_form = UserRegisterForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    context = {"user_form": user_form, "profile_form": profile_form}

    return render(request, "booking/profile.html", context)


def custom_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect("home")
