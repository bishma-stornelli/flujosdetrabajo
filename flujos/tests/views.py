import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase


class FlujosViewsTestCase(TestCase):
    fixtures = ['flujos_views_testdata.json']
    
#    def test_index(self):
#        resp = self.client.get(reverse('polls_index'))
#        self.assertEqual(resp.status_code, 200)
#        self.assertTrue('latest_poll_list' in resp.context)
#        self.assertEqual([poll.pk for poll in resp.context['latest_poll_list']], [1])
#        poll_1 = resp.context['latest_poll_list'][0]
#        self.assertEqual(poll_1.question, 'Are you learning about testing in Django?')
#        self.assertEqual(poll_1.choice_set.count(), 2)
#        choices = poll_1.choice_set.all()
#        self.assertEqual(choices[0].choice, 'Yes')
#        self.assertEqual(choices[0].votes, 1)
#        self.assertEqual(choices[1].choice, 'No')
#        self.assertEqual(choices[1].votes, 0)
#        
#    def test_bad_votes(self):
#        # Ensure a non-existant PK throws a Not Found.
#        resp = self.client.post(reverse('polls_detail', kwargs={'poll_id': 1000000}))
#        self.assertEqual(resp.status_code, 404)
#        
#        # Sanity check.
#        poll_1 = Poll.objects.get(pk=1)
#        self.assertEqual(poll_1.choice_set.get(pk=1).votes, 1)
#        
#        # Send no POST data.
#        resp = self.client.post(reverse('polls_detail', kwargs={'poll_id': 1}))
#        self.assertEqual(resp.status_code, 200)
#        self.assertEqual(resp.context['form']['choice'].errors, [u'This field is required.'])
#        
#        # Send junk POST data.
#        resp = self.client.post(reverse('polls_detail', kwargs={'poll_id': 1}), {'foo': 'bar'})
#        self.assertEqual(resp.status_code, 200)
#        self.assertEqual(resp.context['form']['choice'].errors, [u'This field is required.'])
#        
#        # Send a non-existant Choice PK.
#        resp = self.client.post(reverse('polls_detail', kwargs={'poll_id': 1}), {'choice': 300})
#        self.assertEqual(resp.status_code, 200)
#        self.assertEqual(resp.context['form']['choice'].errors, [u'Select a valid choice. That choice is not one of the available choices.'])
#        
    def test_valid_crear_informe(self):
        resp = self.cliente.post('/flujos/agregar_informe/1/', kwargs={
                                'paso': 1,
                                'nombre': 'Primer informe',
                                'miembro_es_receptor': False,
                                'solicitante_es_receptor': False,
                                'formato': 'Estoy probando que exista el campo ${Primer campo}'})
