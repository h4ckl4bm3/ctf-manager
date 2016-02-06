from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class ProfileViewIntegrationTest(TestCase):

    def setUp(self):
        super(ProfileViewIntegrationTest, self).setUp()
        self.user = User.objects.create_user('test123', 'email@e.com', 'pass')
        self.client.login(username='test123',
                          password='pass')

    def test_profile_view_uses_template(self):
        response = self.client.get(reverse('view_profile', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_view_passes_correct_user_to_template(self):
        user = User.objects.create_user('viewMe')
        response = self.client.get(reverse('view_profile', args=[user.pk]))

        self.assertContains(response, user.username)
        self.assertEqual(user, response.context['p_user'])

