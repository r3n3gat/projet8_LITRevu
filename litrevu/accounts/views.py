from django.shortcuts           import render, redirect
from django.contrib.auth        import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views  import LoginView as AuthLoginView
from django.urls                import reverse

from .forms import SignUpForm, ProfileForm, CustomAuthenticationForm

def signup(request):
    """
    Inscription d’un nouvel utilisateur et auto‐login.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

class login_view(AuthLoginView):
    """
    LoginView personnalisé pour utiliser notre CustomAuthenticationForm.
    """
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse('reviews:feed')

@login_required
def logout_confirm(request):
    """
    GET → affiche confirmation.
    POST → déconnecte et redirige vers login.
    """
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
    return render(request, 'accounts/logout_confirm.html')

@login_required
def profile(request):
    """
    Affiche la fiche utilisateur, avec ses tickets et ses critiques.
    """
    tickets = request.user.tickets.order_by('-created_at')
    reviews = request.user.reviews.order_by('-time_created')
    return render(request, 'accounts/profile.html', {
        'tickets': tickets,
        'reviews': reviews,
    })

@login_required
def profile_edit(request):
    """
    Édition du profil.
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile_form.html', {'form': form})
