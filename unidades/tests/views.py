from django.core.urlresolvers import reverse
from django.test import TestCase
from unidades.models import Unidad
import datetime


class FlujosViewsTestCase(TestCase):
    fixtures = ['unidades_views_testdata.json']
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
    def test_valid_registrar_unidad(self):
        self.assertTrue(self.client.login(username="admin",password="admin"))
        resp = self.client.post('/unidades/registrar_unidad/', {
                                        'nombre': 'Unidad 1',
                                        'descripcion': 'Descripcion de la unidad 1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/unidades/listar_unidades/')
        
    def test_invalid_registrar_unidad(self):
        # Usuario no logueado intentando crear unidad
        resp = self.client.post('/unidades/registrar_unidad/', {
                                        'nombre': 'Unidad 1',
                                        'descripcion': 'Descripcion de la unidad 1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/usuarios/login/?next=/unidades/registrar_unidad/')
        # Log para las siguientes pruebas
        self.assertTrue(self.client.login(username="admin",password="admin"))
        # Dos unidades con mismo nombre
        resp = self.client.post('/unidades/registrar_unidad/', {
                                        'nombre': 'Unidad 1',
                                        'descripcion': 'Descripcion de la unidad 1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/unidades/listar_unidades/')
        resp = self.client.post('/unidades/registrar_unidad/', {
                                        'nombre': 'Unidad 1',
                                        'descripcion': 'Descripcion de la unidad 1'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form']['nombre'].errors, [u'Unidad with this Nombre already exists.'])
        # Nombre vacio
        resp = self.client.post('/unidades/registrar_unidad/', {
                                        'nombre': '',
                                        'descripcion': 'Descripcion de la unidad 1'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form']['nombre'].errors, [u'This field is required.'])
        
        # Descripcion vacio
        resp = self.client.post('/unidades/registrar_unidad/', {
                                        'nombre': 'Unidad 2',
                                        'descripcion': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form']['descripcion'].errors, [u'This field is required.'])
        # Ambos vacios
        resp = self.client.post('/unidades/registrar_unidad/', {
                                        'nombre': '',
                                        'descripcion': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form']['nombre'].errors, [u'This field is required.'])
        self.assertEqual(resp.context['form']['descripcion'].errors, [u'This field is required.'])
        # Usuario no administrador intentando crear unidad
        self.assertTrue(self.client.login(username="fake_admin", password="admin"))
        resp = self.client.post('/unidades/registrar_unidad/', {
                                        'nombre': 'Unidad 4',
                                        'descripcion': 'Descripcion de la unidad 4'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/unidades/listar_unidades/')
        self.assertQuerysetEqual(Unidad.objects.filter(nombre='Unidad 4'), [])
        #self.assertEqual([m for m in list(resp.context['messages'])], 'Solo el administrador')