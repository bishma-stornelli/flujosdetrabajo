from django.contrib.auth.models import User
from flujos.models import Flujo, Paso, Criterio
from unidades.models import Unidad


u1 = User.objects.create_user(username='gersonDex', 
                              email='gerson@gmail.com', 
                              password='123',
                              first_name='Gerson',
                              last_name='Abreu'
                              )

u2 = User.objects.create_user(username='adminServicios', 
                              email='bianchini@gmail.com', 
                              password='123',
                              first_name='Omar',
                              last_name='Perez'
                              )

u3 = User.objects.create_user(username='ernestoDex', 
                              email='iamehn@gmail.com', 
                              password='123',
                              first_name='Ernesto',
                              last_name='Novich'
                              )
u4 = User.objects.create_user(username='bishma', 
                              email='tamerdark@gmail.com', 
                              password='123',
                              first_name='Bishma',
                              last_name='Stornelli'
                              )
u5 = User.objects.create_user(username='andreth', 
                              email='andreth91@gmail.com', 
                              password='123',
                              first_name='Andreth',
                              last_name='Salazar'
                              )

u6 = User.objects.create_user(username='visitante1', 
                              email='a@gmail.com', 
                              password='123',
                              first_name='Visitante',
                              last_name='DEX'
                              )

u7 = User.objects.create_user(username='visitante2', 
                              email='b@gmail.com', 
                              password='123',
                              first_name='Visitante',
                              last_name='DEG'
                              )

u8 = User.objects.create_user(username='visitante3', 
                              email='c@gmail.com', 
                              password='123',
                              first_name='Visitante',
                              last_name='Rectorado'
                              )
u1.save()
u2.save()
u3.save()
u4.save()
u5.save()
u6.save()
u7.save()
u8.save()

unidad1 = Unidad.objects.create(nombre="DEX", descripcion="Decanato de Extension", responsable=u1, miembros=[u1,u2,u3,u4])
unidad1.save()
unidad2 = Unidad.objects.create(nombre="DS", descripcion="Direccion de Servicios", responsable=u2, miembros=[u4,u5,u1])
unidad2.save()
unidad3 = Unidad.objects.create(nombre="CPYD", descripcion="Comision de Planificacion y Desarrollo", responsable=u3, miembros=[u1,u5,u4])
unidad3.save()
unidad4 = Unidad.objects.create(nombre="RECTORADO", descripcion="Rectorado", responsable=u4, miembros=(u1))
unidad4.save()
unidad5 = Unidad.objects.create(nombre="Secretaria", descripcion="Secretaria", responsable=u5, miembros=(u1))
unidad5.save()

flujo1 = Flujo.objects.create(nombre="Flujo Actividades Extension DEX",
 descripcion="Pasos para solicitar una actividad de extension financiada por el DEX ", unidad=unidad1)
flujo1.save()

flujo2 = Flujo.objects.create(nombre="Flujo Solicitud de Servicios",
 descripcion="Pasos para solicitar la asistencia de planta fisica ", unidad=unidad2)
flujo2.save()



p1 = Paso.objects.create(nombre="Inicial"
, descripcion="Completar la inscripcion en el sitio web del DEX", flujo=flujo1, tipo=Paso.TIPO_INICIAL)
p1.save()
p2 = Paso.objects.create(nombre="PASO 2", descripcion="Paso dummy", flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p2.save()
p3 = Paso.objects.create(nombre="PASO 3", descripcion="Paso dummy", flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p2.save()
p4 = Paso.objects.create(nombre="PASO 4", descripcion="Paso dummy", flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p4.save()
p5 = Paso.objects.create(nombre="PASO 5", descripcion="Paso dummy", flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p5.save()
p6 = Paso.objects.create(nombre="PASO 6", descripcion="Paso dummy", flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p6.save()
p7 = Paso.objects.create(nombre="PASO 7", descripcion="Paso dummy", flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p7.save()
p8 = Paso.objects.create(nombre="Final"
, descripcion="Completar la entrega de documentosPaso final", flujo=flujo1, tipo=Paso.TIPO_FINAL)
p8.save()

c1 = Criterio.objects.create(paso_origen=p1,paso_destino=p2,descripcion="Criterio de inscripcion",expresion="true")
c1.save()
c2 = Criterio.objects.create(paso_origen=p2,paso_destino=p3,descripcion="Criterio dummy",expresion="true")
c2.save()
c3 = Criterio.objects.create(paso_origen=p3,paso_destino=p4,descripcion="Criterio dummy",expresion="true")
c3.save()
c4 = Criterio.objects.create(paso_origen=p4,paso_destino=p5,descripcion="Criterio dummy",expresion="true")
c4.save()
c5 = Criterio.objects.create(paso_origen=p5,paso_destino=p6,descripcion="Criterio dummy",expresion="true")
c5.save()
c6 = Criterio.objects.create(paso_origen=p6,paso_destino=p7,descripcion="Criterio final",expresion="true")
c6.save()
c7 = Criterio.objects.create(paso_origen=p7,paso_destino=p8,descripcion="Criterio final",expresion="true")
c7.save()

p1 = Paso.objects.create(nombre="Inicial"
, descripcion="Completar la inscripcion en el sitio web del DS", flujo=flujo2, tipo=Paso.TIPO_INICIAL)
p1.save()
p2 = Paso.objects.create(nombre="PASO 2", descripcion="Paso dummy", flujo=flujo2, tipo=Paso.TIPO_NORMAL)
p2.save()
p3 = Paso.objects.create(nombre="PASO 3", descripcion="Paso dummy", flujo=flujo2, tipo=Paso.TIPO_NORMAL)
p2.save()
p4 = Paso.objects.create(nombre="PASO 4", descripcion="Paso dummy", flujo=flujo2, tipo=Paso.TIPO_NORMAL)
p4.save()
p5 = Paso.objects.create(nombre="PASO 5", descripcion="Paso dummy", flujo=flujo2, tipo=Paso.TIPO_NORMAL)
p5.save()
p6 = Paso.objects.create(nombre="PASO 6", descripcion="Paso dummy", flujo=flujo2, tipo=Paso.TIPO_NORMAL)
p6.save()
p7 = Paso.objects.create(nombre="PASO 7", descripcion="Paso dummy", flujo=flujo2, tipo=Paso.TIPO_NORMAL)
p7.save()
p8 = Paso.objects.create(nombre="Final"
, descripcion="Reportar el beneficio a su inmueble", flujo=flujo1, tipo=Paso.TIPO_FINAL)
p8.save()

c1 = Criterio.objects.create(paso_origen=p1,paso_destino=p2,descripcion="Criterio de inscripcion",expresion="true")
c1.save()
c2 = Criterio.objects.create(paso_origen=p2,paso_destino=p3,descripcion="Criterio dummy",expresion="true")
c2.save()
c3 = Criterio.objects.create(paso_origen=p3,paso_destino=p4,descripcion="Criterio dummy",expresion="true")
c3.save()
c4 = Criterio.objects.create(paso_origen=p4,paso_destino=p5,descripcion="Criterio dummy",expresion="true")
c4.save()
c5 = Criterio.objects.create(paso_origen=p5,paso_destino=p6,descripcion="Criterio dummy",expresion="true")
c5.save()
c6 = Criterio.objects.create(paso_origen=p6,paso_destino=p7,descripcion="Criterio final",expresion="true")
c6.save()
c7 = Criterio.objects.create(paso_origen=p7,paso_destino=p8,descripcion="Criterio final",expresion="true")
c7.save()
