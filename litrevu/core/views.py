# litrevu/core/views.py

from django.shortcuts       import render, redirect
from django.contrib.auth    import login
from django.urls            import reverse

from accounts.forms         import CustomAuthenticationForm

def home(request):
    """
    Page d'accueil :
      - Affiche toujours le formulaire de connexion.
      - En POST, redirige vers le flux après login.
    """
    next_url = reverse('reviews:feed')
    form = CustomAuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect(next_url)

    return render(request, 'core/home.html', {
        'form': form,
        'next': next_url,
    })
