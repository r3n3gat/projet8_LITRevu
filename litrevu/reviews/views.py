from itertools import chain

from django.shortcuts               import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponseForbidden
from django.urls                    import reverse
from django.views.generic           import CreateView, DetailView
from django.db.models               import Q, F, Value
from django.db                      import IntegrityError
from django.contrib.auth            import get_user_model
from django.db.models.fields        import CharField

from .models  import Ticket, Review, Comment, UserFollows
from .forms   import TicketForm, ReviewForm, CommentForm, UserFollowForm

User = get_user_model()


@login_required
def feed(request):
    """
    Fil d’actualité : fusion tickets + critiques de l’utilisateur et de ses suivis,
    trié en antéchronologique.
    """
    # 1) IDs des utilisateurs suivis
    followed_ids = list(
        UserFollows.objects
                   .filter(user=request.user)
                   .values_list('followed_user_id', flat=True)
    )

    # 2) QuerySets annotés avec un champ `created` et `content_type`
    tickets = (
        Ticket.objects
              .filter(Q(user=request.user) | Q(user__in=followed_ids))
              .annotate(
                  created=F('created_at'),
                  content_type=Value('ticket', output_field=CharField()),
              )
              .select_related('user')
    )
    reviews = (
        Review.objects
              .filter(Q(user=request.user) | Q(user__in=followed_ids))
              .annotate(
                  created=F('time_created'),
                  content_type=Value('review', output_field=CharField()),
              )
              .select_related('ticket', 'user')
    )

    # 3) Fusionner et trier
    entries = sorted(
        chain(tickets, reviews),
        key=lambda obj: obj.created,
        reverse=True,
    )

    return render(request, 'reviews/feed.html', {
        'entries': entries,
    })


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    reviews = Review.objects.filter(user=request.user).order_by('-time_created')
    return render(request, 'reviews/ticket_list.html', {
        'tickets': tickets,
        'reviews': reviews,
    })


@login_required
def ticket_create(request):
    form = TicketForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        t = form.save(commit=False)
        t.user = request.user
        t.save()
        return redirect('reviews:ticket_list')
    return render(request, 'reviews/ticket_form.html', {'form': form})


@login_required
def ticket_edit(request, pk):
    t = get_object_or_404(Ticket, pk=pk)
    if t.user != request.user:
        return HttpResponseForbidden()
    form = TicketForm(request.POST or None,
                      request.FILES or None,
                      instance=t)
    if form.is_valid():
        form.save()
        return redirect('reviews:ticket_list')
    return render(request, 'reviews/ticket_form.html', {'form': form})


@login_required
def ticket_delete(request, pk):
    t = get_object_or_404(Ticket, pk=pk)
    if t.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        t.delete()
        return redirect('reviews:ticket_list')
    return render(request, 'reviews/ticket_confirm_delete.html', {'ticket': t})


@login_required
def review_create(request, ticket_pk):
    ticket = get_object_or_404(Ticket, pk=ticket_pk)
    # déjà une critique ? → redirige vers l’édition
    if ticket.reviews.exists():
        return redirect('reviews:review_edit', pk=ticket.reviews.first().pk)
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        r = form.save(commit=False)
        r.ticket = ticket
        r.user   = request.user
        r.save()
        return redirect('reviews:ticket_list')
    return render(request, 'reviews/review_answer_form.html', {
        'form':   form,
        'ticket': ticket,
    })


@login_required
def free_review_create(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            t = ticket_form.save(commit=False)
            t.user = request.user
            t.save()
            r = review_form.save(commit=False)
            r.ticket = t
            r.user   = request.user
            r.save()
            return redirect('reviews:ticket_list')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    return render(request, 'reviews/review_form.html', {
        'ticket_form': ticket_form,
        'form':        review_form,
        'ticket':      None,
    })


@login_required
def review_edit(request, pk):
    r = get_object_or_404(Review, pk=pk)
    if r.user != request.user:
        return HttpResponseForbidden()
    form = ReviewForm(request.POST or None, instance=r)
    if form.is_valid():
        form.save()
        return redirect('reviews:ticket_list')
    return render(request, 'reviews/review_form.html', {
        'form':   form,
        'ticket': r.ticket,
    })


@login_required
def review_delete(request, pk):
    r = get_object_or_404(Review, pk=pk)
    if r.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        r.delete()
        return redirect('reviews:ticket_list')
    return render(request, 'reviews/review_confirm_delete.html', {'review': r})


class ReviewDetailView(DetailView):
    model               = Review
    template_name       = 'reviews/review_detail.html'
    context_object_name = 'review'


class CommentCreateView(CreateView):
    model         = Comment
    form_class    = CommentForm
    template_name = 'reviews/comment_form.html'

    def form_valid(self, form):
        form.instance.user   = self.request.user
        form.instance.review = get_object_or_404(Review, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('reviews:review_detail', args=[self.kwargs['pk']])


@login_required
def follow_list(request):
    follows      = UserFollows.objects.filter(user=request.user)\
                       .select_related('followed_user')
    followers    = UserFollows.objects.filter(followed_user=request.user)\
                       .select_related('user')
    form         = UserFollowForm()
    followed_ids = list(follows.values_list('followed_user_id', flat=True))
    suggestions  = User.objects.exclude(pk__in=followed_ids + [request.user.pk])
    return render(request, 'reviews/follow_list.html', {
        'follows':     follows,
        'followers':   followers,
        'form':        form,
        'suggestions': suggestions,
    })


@login_required
def follow_add(request):
    if request.method != 'POST':
        return redirect('reviews:follow_list')

    form = UserFollowForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        if username == request.user.username:
            form.add_error('username', "Impossible de suivre cet utilisateur.")
        else:
            try:
                target = User.objects.get(username=username)
                UserFollows.objects.create(
                    user=request.user,
                    followed_user=target
                )
                return redirect('reviews:follow_list')
            except (User.DoesNotExist, IntegrityError):
                form.add_error('username', "Impossible de suivre cet utilisateur.")

    follows      = UserFollows.objects.filter(user=request.user)\
                       .select_related('followed_user')
    followers    = UserFollows.objects.filter(followed_user=request.user)\
                       .select_related('user')
    followed_ids = list(follows.values_list('followed_user_id', flat=True))
    suggestions  = User.objects.exclude(pk__in=followed_ids + [request.user.pk])
    return render(request, 'reviews/follow_list.html', {
        'follows':     follows,
        'followers':   followers,
        'form':        form,
        'suggestions': suggestions,
    })


@login_required
def follow_delete(request, pk):
    uf = get_object_or_404(UserFollows, pk=pk, user=request.user)
    if request.method == 'POST':
        uf.delete()
        return redirect('reviews:follow_list')
    return render(request, 'reviews/follow_confirm_delete.html', {'follow': uf})
