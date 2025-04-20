from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import F, Sum
from django.shortcuts import render, redirect, get_object_or_404
from store.models import OrderItem, Order,Product

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id, is_superuser=False)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, "User updated successfully.")
        return redirect('manage_users')

    return render(request, "accounts/edit_user.html", {'user_obj': user})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id, is_superuser=False)
    user.delete()
    messages.warning(request, "User deleted.")
    return redirect('manage_users')


@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/manage_users.html', {'users': users})




@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_products = Product.objects.count()

    revenue = OrderItem.objects.aggregate(
        total=Sum(F('quantity') * F('product__price'))
    )['total'] or 0

    return render(request, "accounts/admin_dashboard.html", {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_revenue': revenue,
    })
@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        new_username = request.POST.get("username")
        new_email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Update username and email
        user.username = new_username
        user.email = new_email

        # Handle password update
        if password1 and password2:
            if password1 == password2:
                user.set_password(password1)
                update_session_auth_hash(request, user)  # prevent logout
            else:
                messages.error(request, "Passwords do not match.")
                return redirect('profile')

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request, "accounts/profile.html")

@login_required

def client_dashboard(request):
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return render(request, 'accounts/client_dashboard.html')
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("auth")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("auth")

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)

        # ✅ Redirect to client dashboard directly
        return redirect("client_dashboard")

    return redirect("auth")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")  # ou vers dashboard
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("auth")  # ← on retourne vers la page unique

    return redirect("auth")


def logout_view(request):
    logout(request)
    return redirect("auth")
def auth_page(request):
    return render(request, 'accounts/auth.html')