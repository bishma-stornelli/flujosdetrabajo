from django.contrib.auth.models import User
from flujos.models import Flujo, Paso, Criterio, Alerta, Informe, TipoAlerta
from unidades.models import Unidad
from solicitudes.models import Solicitud, Registro

TipoAlerta(nombre="SMS").save()
TipoAlerta(nombre="Email").save()

u1 = User.objects.create_user(username='gersonDex', 
                              email='gerson@gmail.com', 
                              password='123'
                              )

u2 = User.objects.create_user(username='adminServicios', 
                              email='bianchini@gmail.com', 
                              password='123'
                              )

u3 = User.objects.create_user(username='ernestoDex', 
                              email='iamehn@gmail.com', 
                              password='123'
                              )
u4 = User.objects.create_user(username='bishma', 
                              email='tamerdark@gmail.com', 
                              password='123'
                              )
u5 = User.objects.create_user(username='andreth', 
                              email='andreth91@gmail.com', 
                              password='123'
                              )

u6 = User.objects.create_user(username='visitante1', 
                              email='a@gmail.com', 
                              password='123'
                              )

u7 = User.objects.create_user(username='visitante2', 
                              email='b@gmail.com', 
                              password='123'
                              )

u8 = User.objects.create_user(username='visitante3', 
                              email='c@gmail.com', 
                              password='123'
                              )
u1.save()
u2.save()
u3.save()
u4.save()
u5.save()
u6.save()
u7.save()
u8.save()
admin = User.objects.get(username="admin")
unidad1 = Unidad(nombre="DEX", descripcion="Decanato de Extension", responsable=admin)
unidad1.save()
unidad1.miembros.add(u1)
unidad1.miembros.add(u2)
unidad1.miembros.add(u3)
unidad1.miembros.add(u4)
unidad1.miembros.add(admin)


unidad2 = Unidad(nombre="DS", descripcion="Direccion de Servicios", responsable=u2)
unidad2.save()
unidad2.miembros.add(u5)
unidad2.miembros.add(u4)
unidad2.miembros.add(u1)


unidad3 = Unidad(nombre="CPYD", descripcion="Comision de Planificacion y Desarrollo", responsable=u3)
unidad3.save()
unidad3.miembros.add(u1)
unidad3.miembros.add(u5)
unidad3.miembros.add(u4)



unidad4 = Unidad(nombre="RECTORADO", descripcion="Rectorado", responsable=u4)
unidad4.save()
unidad4.miembros.add(u1)


unidad5 = Unidad(nombre="Secretaria", descripcion="Secretaria", responsable=u5)
unidad5.save()
unidad5.miembros.add(u1)


flujo1 = Flujo(nombre="Flujo Actividades Extension DEX",
 descripcion="Pasos para solicitar una actividad de extension financiada por el DEX ", unidad=unidad1)
flujo1.save()

flujo2 = Flujo(nombre="Flujo Solicitud de Servicios",
 descripcion="Pasos para solicitar la asistencia de planta fisica ", unidad=unidad2)
flujo2.save()



p1 = Paso(nombre="Inicial", descripcion="Completar la inscripcion en el sitio web del DEX", flujo=flujo1, tipo=Paso.TIPO_INICIAL)
p1.save()
p2 = Paso(nombre="PASO 2", descripcion="Paso dummy", flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p2.save()
p3 = Paso(nombre="PASO 3", descripcion="Paso dummy", flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p3.save()
p4 = Paso(nombre="PASO 4", descripcion="Paso dummy", flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p4.save()
p5 = Paso(nombre="PASO 5", descripcion="Paso dummy", flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p5.save()
p6 = Paso(nombre="PASO 6", descripcion="Paso dummy", flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p6.save()
p7 = Paso(nombre="PASO 7", descripcion="Paso dummy", flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p7.save()
p8 = Paso(nombre="Final", descripcion="Completar la entrega de documentosPaso final", flujo=flujo1, tipo=Paso.TIPO_FINAL)
p8.save()

c1 = Criterio(paso_origen=p1,paso_destino=p2,descripcion="Criterio de inscripcion",expresion="true")
c1.save()
c2 = Criterio(paso_origen=p2,paso_destino=p3,descripcion="Criterio dummy",expresion="true")
c2.save()
c3 = Criterio(paso_origen=p3,paso_destino=p4,descripcion="Criterio dummy",expresion="true")
c3.save()
c4 = Criterio(paso_origen=p4,paso_destino=p5,descripcion="Criterio dummy",expresion="true")
c4.save()
c5 = Criterio(paso_origen=p5,paso_destino=p6,descripcion="Criterio dummy",expresion="true")
c5.save()
c6 = Criterio(paso_origen=p6,paso_destino=p7,descripcion="Criterio dummy",expresion="true")
c6.save()
c7 = Criterio(paso_origen=p7,paso_destino=p8,descripcion="Criterio final",expresion="true")
c7.save()

a1 = Alerta(nombre="Alerta 1", paso=p1)
a1.save()

i1 = Informe(nombre="Alerta 1", paso=p1)
i1.save()

p1 = Paso(nombre="Inicial", descripcion="Completar la inscripcion en el sitio web del DS", flujo=flujo2, tipo=Paso.TIPO_INICIAL)
p1.save()
p2 = Paso(nombre="PASO 2", descripcion="Paso dummy", flujo=flujo2, tipo=Paso.TIPO_NORMAL)
p2.save()
p3 = Paso(nombre="PASO 3", descripcion="Paso dummy", flujo=flujo2, tipo=Paso.TIPO_NORMAL)
p3.save()
p4 = Paso(nombre="PASO 4", descripcion="Paso dummy", flujo=flujo2, tipo=Paso.TIPO_NORMAL)
p4.save()
p5 = Paso(nombre="PASO 5", descripcion="Paso dummy", flujo=flujo2, tipo=Paso.TIPO_NORMAL)
p5.save()
p6 = Paso(nombre="PASO 6", descripcion="Paso dummy", flujo=flujo2, tipo=Paso.TIPO_NORMAL)
p6.save()
p7 = Paso(nombre="PASO 7", descripcion="Paso dummy", flujo=flujo2, tipo=Paso.TIPO_NORMAL)
p7.save()
p8 = Paso(nombre="Final", descripcion="Reportar el beneficio a su inmueble", flujo=flujo1, tipo=Paso.TIPO_FINAL)
p8.save()

c1 = Criterio(paso_origen=p1,paso_destino=p2,descripcion="Criterio de inscripcion",expresion="true")
c1.save()
c2 = Criterio(paso_origen=p2,paso_destino=p3,descripcion="Criterio dummy",expresion="true")
c2.save()
c3 = Criterio(paso_origen=p3,paso_destino=p4,descripcion="Criterio dummy",expresion="true")
c3.save()
c4 = Criterio(paso_origen=p4,paso_destino=p5,descripcion="Criterio dummy",expresion="true")
c4.save()
c5 = Criterio(paso_origen=p5,paso_destino=p6,descripcion="Criterio dummy",expresion="true")
c5.save()
c6 = Criterio(paso_origen=p6,paso_destino=p7,descripcion="Criterio dummy",expresion="true")
c6.save()
c7 = Criterio(paso_origen=p7,paso_destino=p8,descripcion="Criterio final",expresion="true")
c7.save()


solicitud1 = Solicitud(flujo=flujo2,fecha_de_solicitud=datetime.datetime.now())