from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import TestCase
from flujos.models import Paso, Flujo, Criterio
import datetime


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
    def test_crear_todo_flujo(self):
        resp = self.aux_crear_flujo("admin", "admin", 2, "El nombre", "La descripcion")
        self.assertEqual(resp.status_code, 302, "Luego de un post valido a crear_flujo deberia redireccionar")
        self.assertEqual(resp['Location'], 'http://testserver/flujos/consultar_flujo/1/')
        resp = self.client.get(resp['Location'])
        self.assertContains(resp, "El nombre")
        self.assertContains(resp, "La descripcion")
        
        # Intentar crear varios pasos
        self.aux_crear_paso(1,"1", "1",1,Paso.TIPO_INICIAL)
        self.aux_crear_paso(1,"2", "2",2,Paso.TIPO_NORMAL)
        self.aux_crear_paso(1,"3", "3",3,Paso.TIPO_NORMAL)
        self.aux_crear_paso(1,"4", "4",4,Paso.TIPO_DIVISION)
        self.aux_crear_paso(1,"5", "5",5,Paso.TIPO_NORMAL)
        self.aux_crear_paso(1,"6", "6",6,Paso.TIPO_NORMAL)
        self.aux_crear_paso(1,"7", "7",7,Paso.TIPO_UNION)
        self.aux_crear_paso(1,"8", "8",8,Paso.TIPO_FINAL)
        
        
        self.aux_crear_camino(1, paso_origen=1, paso_destino=2)
        self.aux_crear_camino(1, paso_origen=1, paso_destino=3)
        self.aux_crear_camino(1, paso_origen=2, paso_destino=8)
        self.aux_crear_camino(1, paso_origen=3, paso_destino=4)
        self.aux_crear_camino(1, paso_origen=4, paso_destino=5)
        self.aux_crear_camino(1, paso_origen=4, paso_destino=6)
        self.aux_crear_camino(1, paso_origen=5, paso_destino=7)
        self.aux_crear_camino(1, paso_origen=6, paso_destino=7)
        self.aux_crear_camino(1, paso_origen=8, paso_destino=8)

        self.assertEqual(self.aux_crear_camino(2, paso_origen=1, paso_destino=3, commit= False).status_code, 404, "Crear un camino en un flujo que no existe deberia regresar 404")
        
        r = self.aux_crear_camino(1, 0, 3, commit=False)
        self.assertEqual(r.status_code, 200, "Crear un camino entre pasos que no existe deberia renderizar el mismo template")
        self.assertEqual(r.context['form']['paso_origen'].errors, [u'Select a valid choice. That choice is not one of the available choices.'])
        
    def aux_crear_camino(self, flujo_id, paso_origen, paso_destino, descripcion='Cualquier cosa', expresion='True', commit=True):
        response = self.client.post('/flujos/agregar_camino/%s/' % flujo_id,
                                    { 'paso_origen': paso_origen, 
                                     'paso_destino': paso_destino,
                                     'descripcion': descripcion,
                                     'expresion': expresion })
        if commit:
            self.assertEqual(response.status_code, 302, "Crear un camino deberia redireccionar a la pagina del flujo")
            self.assertEqual(response['Location'], 'http://testserver/flujos/consultar_flujo/%s/' % flujo_id, 
                                                "Agregar camino deberia redirecciona a la consulta del flujo")
        return response
        
    def aux_crear_paso(self, flujo_id, nombre, descripcion, id_de_paso_esperado, tipo=Paso.TIPO_NORMAL):
        response = self.client.post('/flujos/agregar_paso/%s/' % flujo_id,
                                    { 'flujo': flujo_id, 
                                     'nombre': nombre,
                                     'tipo': tipo,
                                     'descripcion': descripcion })
        self.assertEqual(response.status_code, 302, "Crear un paso deberia redireccionar a la pagina de consultarlo")
        self.assertEqual(response['Location'], 'http://testserver/flujos/consultar_paso/%s/' % id_de_paso_esperado, 
                         "El id asignado al paso recien creado es incorrecto")
        
    
    def aux_crear_flujo(self, username, password, unidad_id, nombre='Flujo cualquiera', descripcion='Algo'):
        self.assertTrue(self.client.login(username=username,password=password), "El usuario %s no se encuentra registrado." % username)
        return self.client.post('/flujos/crear_flujo/', {
                                        'nombre': nombre,
                                        'descripcion': descripcion,
                                        'unidad': unidad_id })
        
    def test_crear_flujo_en_otra_unidad(self):
        resp = self.aux_crear_flujo("admin", "admin", 1)
        self.assertEqual(resp.status_code, 403, "El status de la pagina debe ser 403 indicando que no se tiene acceso")
        
    def test_crear_flujo_con_parametros_invalidos(self):
        # Nombre vacio
        resp = self.aux_crear_flujo("admin", "admin", 2, '')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form']['nombre'].errors, [u'This field is required.'])
        
        resp = self.aux_crear_flujo("admin", "admin", 2, descripcion='')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form']['descripcion'].errors, [u'This field is required.'])
        
#    def test_invalid_registrar_unidad(self):
#        # Usuario no logueado intentando crear unidad
#        resp = self.client.post('/unidades/registrar_unidad/', {
#                                        'nombre': 'Unidad 1',
#                                        'descripcion': 'Descripcion de la unidad 1'})
#        self.assertEqual(resp.status_code, 302)
#        self.assertEqual(resp['Location'], 'http://testserver/usuarios/login/?next=/unidades/registrar_unidad/')
#        # Log para las siguientes pruebas
#        self.assertTrue(self.client.login(username="admin",password="admin"))
#        # Dos unidades con mismo nombre
#        resp = self.client.post('/unidades/registrar_unidad/', {
#                                        'nombre': 'Unidad 1',
#                                        'descripcion': 'Descripcion de la unidad 1'})
#        self.assertEqual(resp.status_code, 302)
#        self.assertEqual(resp['Location'], 'http://testserver/unidades/listar_unidades/')
#        resp = self.client.post('/unidades/registrar_unidad/', {
#                                        'nombre': 'Unidad 1',
#                                        'descripcion': 'Descripcion de la unidad 1'})
#        self.assertEqual(resp.status_code, 200)
#        self.assertEqual(resp.context['form']['nombre'].errors, [u'Unidad with this Nombre already exists.'])
#        # Nombre vacio
#        resp = self.client.post('/unidades/registrar_unidad/', {
#                                        'nombre': '',
#                                        'descripcion': 'Descripcion de la unidad 1'})
#        self.assertEqual(resp.status_code, 200)
#        self.assertEqual(resp.context['form']['nombre'].errors, [u'This field is required.'])
#        
#        # Descripcion vacio
#        resp = self.client.post('/unidades/registrar_unidad/', {
#                                        'nombre': 'Unidad 2',
#                                        'descripcion': ''})
#        self.assertEqual(resp.status_code, 200)
#        self.assertEqual(resp.context['form']['descripcion'].errors, [u'This field is required.'])
#        # Ambos vacios
#        resp = self.client.post('/unidades/registrar_unidad/', {
#                                        'nombre': '',
#                                        'descripcion': ''})
#        self.assertEqual(resp.status_code, 200)
#        self.assertEqual(resp.context['form']['nombre'].errors, [u'This field is required.'])
#        self.assertEqual(resp.context['form']['descripcion'].errors, [u'This field is required.'])
#        # Usuario no administrador intentando crear unidad
#        self.assertTrue(self.client.login(username="fake_admin", password="admin"))
#        resp = self.client.post('/unidades/registrar_unidad/', {
#                                        'nombre': 'Unidad 4',
#                                        'descripcion': 'Descripcion de la unidad 4'})
#        self.assertEqual(resp.status_code, 302)
#        self.assertEqual(resp['Location'], 'http://testserver/unidades/listar_unidades/')
#        self.assertQuerysetEqual(Unidad.objects.filter(nombre='Unidad 4'), [])
        #self.assertEqual([m for m in list(resp.context['messages'])], 'Solo el administrador')
