# reviews/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Ticket, Review, Comment, UserFollows

User = get_user_model()


class TicketReviewTests(TestCase):
    def setUp(self):
        # Création d’un utilisateur de test et connexion
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client = Client()
        self.client.login(username='testuser', password='secret')

    def test_ticket_creation_and_list(self):
        # Création d’un ticket via la vue
        response = self.client.post(
            reverse('reviews:ticket_add'),
            {'title': 'Titre Test', 'description': 'Description Test'}
        )
        # Vérifie la redirection vers la liste
        self.assertRedirects(response, reverse('reviews:ticket_list'))
        # Vérifie qu’il y a bien un ticket en base
        tickets = Ticket.objects.filter(user=self.user)
        self.assertEqual(tickets.count(), 1)
        self.assertEqual(tickets.first().title, 'Titre Test')

    def test_ticket_edit_and_delete(self):
        # Préparation : un ticket existant
        ticket = Ticket.objects.create(
            user=self.user, title='Origine', description='Desc'
        )
        # Edition
        url_edit = reverse('reviews:ticket_edit', args=[ticket.pk])
        response = self.client.post(url_edit, {
            'title': 'Modifié', 'description': 'Desc modifiée'
        })
        self.assertRedirects(response, reverse('reviews:ticket_list'))
        ticket.refresh_from_db()
        self.assertEqual(ticket.title, 'Modifié')

        # Suppression
        url_delete = reverse('reviews:ticket_delete', args=[ticket.pk])
        response = self.client.post(url_delete)
        self.assertRedirects(response, reverse('reviews:ticket_list'))
        self.assertFalse(Ticket.objects.filter(pk=ticket.pk).exists())

    def test_review_creation_and_list(self):
        # Création d’un ticket pour y rattacher une review
        ticket = Ticket.objects.create(
            user=self.user, title='Pour critique', description='Desc'
        )
        url_review = reverse('reviews:review_create', args=[ticket.pk])
        response = self.client.post(url_review, {
            'rating': 5, 'headline': 'Super', 'body': 'Très bon'
        })
        self.assertRedirects(response, reverse('reviews:ticket_list'))
        reviews = Review.objects.filter(ticket=ticket)
        self.assertEqual(reviews.count(), 1)
        self.assertEqual(reviews.first().rating, 5)

    def test_review_edit_and_delete(self):
        ticket = Ticket.objects.create(
            user=self.user, title='Critiquer', description='Desc'
        )
        review = Review.objects.create(
            ticket=ticket, user=self.user,
            rating=3, headline='OK', body='Moyen'
        )
        # Edition
        url_edit = reverse('reviews:review_edit', args=[review.pk])
        response = self.client.post(url_edit, {
            'rating': 4, 'headline': 'Mieux', 'body': 'Amélioré'
        })
        self.assertRedirects(response, reverse('reviews:ticket_list'))
        review.refresh_from_db()
        self.assertEqual(review.rating, 4)
        # Suppression
        url_delete = reverse('reviews:review_delete', args=[review.pk])
        response = self.client.post(url_delete)
        self.assertRedirects(response, reverse('reviews:ticket_list'))
        self.assertFalse(Review.objects.filter(pk=review.pk).exists())


class CommentTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('u1', password='pass')
        self.ticket = Ticket.objects.create(title='T1', description='D1', user=self.u1)
        self.review = Review.objects.create(
            ticket=self.ticket, user=self.u1, rating=3, headline='H', body='B'
        )

    def test_comment_creation(self):
        self.client.login(username='u1', password='pass')
        url = reverse('reviews:comment_create', args=[self.review.pk])
        response = self.client.post(url, {'body': 'Super critique !'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(body='Super critique !').exists())


class ReviewDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u', password='pass')
        self.ticket = Ticket.objects.create(title='T1', description='D1', user=self.user)
        self.review = Review.objects.create(
            ticket=self.ticket, user=self.user, rating=4,
            headline='Titre', body='Contenu'
        )

    def test_detail_view_status_and_context(self):
        url = reverse('reviews:review_detail', args=[self.review.pk])
        # anonymes peuvent voir la page
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Titre')
        self.assertContains(response, 'Contenu')
        # pas encore de commentaire
        self.assertContains(response, 'Aucun commentaire')

    def test_comments_listed(self):
        Comment.objects.create(review=self.review, user=self.user, body='Nice!')
        url = reverse('reviews:review_detail', args=[self.review.pk])
        response = self.client.get(url)
        self.assertContains(response, 'Nice!')
        self.assertContains(response, '<time', html=False)


class FollowTests(TestCase):
    def setUp(self):
        # Deux utilisateurs et connexion d’Alice
        self.alice = User.objects.create_user('alice', password='pass')
        self.bob   = User.objects.create_user('bob',   password='pass')
        self.client.login(username='alice', password='pass')



    def test_follow_and_suggestions(self):
        # Avant : bob en suggestions
        resp = self.client.get(reverse('reviews:follow_list'))
        self.assertContains(resp, 'bob')
        # On suit bob
        resp = self.client.post(reverse('reviews:follow_add'),
                                {'username': 'bob'}, follow=True)
        self.assertContains(resp, 'Désabonner')      # bob apparaît dans abonnements
        self.assertNotContains(resp, 'Suivre')       # plus de bouton "Suivre" à côté de bob
        # On se désabonne
        uf_pk = UserFollows.objects.get(user=self.alice,
                                        followed_user=self.bob).pk
        resp = self.client.post(reverse('reviews:follow_delete', args=[uf_pk]),
                                follow=True)
        self.assertContains(resp, 'Suivre')          # bob revient en suggestions
