from django.core.urlresolvers import reverse, resolve
from django.utils.html import escape

from CTFmanager.forms import ChallengeForm, DUPLICATE_ERROR
from CTFmanager.models import Event, Challenge
from CTFmanager.tests.views.base import ViewTestCase
from CTFmanager.views import new_challenge


class EventPageAddChallengeTest(ViewTestCase):
    def test_requires_login(self):
        self.client.logout()
        _event = self.create_event('challenge_test', True)
        response = self.client.get(reverse('newChallenge', args=[_event.name]))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('newChallenge', args=[_event.name]))

    def post_incorrect_form(self):
        _event = self.create_event('test', True)
        url = reverse('newChallenge', args=[_event.name])
        return self.client.post(url, data={'name': '', 'points': '200'})

    def create_new_challenge_response(self):
        _event = self.create_event('test', True)
        response = self.client.get(reverse('newChallenge', args=[_event.name]))
        return response

    def test_add_challenge_resolves_to_correct_page(self):
        _event = self.create_event('test', True)
        response = resolve(reverse('newChallenge', args=[_event.name]))
        self.assertEqual(response.func, new_challenge)

    def test_add_challenge_uses_correct_template(self):
        response = self.create_new_challenge_response()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/add_challenge.html')

    def test_add_challenge_page_renders_challenge_form(self):
        response = self.create_new_challenge_response()
        self.assertIsInstance(response.context['form'], ChallengeForm)

    def test_for_valid_input_shows_challenge_on_event_detail_page(self):
        _event = self.create_event('testEvent', True)
        url = reverse('newChallenge', args=[_event.name])
        self.client.post(url, data={'name': 'testChallenge', 'points': '200'})
        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, 'testChallenge')

    def test_for_invalid_input_renders_to_new_challenge_page(self):
        _event = self.create_event('test', True)
        url = reverse('newChallenge', args=[_event.name])
        response = self.client.post(url, data={'name': '', 'points': '200'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/add_challenge.html')

    def test_for_invalid_input_redirect_uses_challenge_form(self):
        response = self.post_incorrect_form()
        self.assertIsInstance(response.context['form'], ChallengeForm)

    def test_for_invalid_input_doesnt_save(self):
        self.post_incorrect_form()
        event = Event.objects.first()
        self.assertEqual(0, len(event.challenge_set.all()))

    def test_duplicate_challenge_displays_error_text(self):
        _event = self.create_event('testEvent')
        chal = Challenge.objects.create(name='testDuplicate', points=1, event=_event)
        url = reverse('newChallenge', args=[_event.name])
        response = self.client.post(url, data={'name': chal.name, 'points': chal.points})
        self.assertContains(response, escape(DUPLICATE_ERROR))