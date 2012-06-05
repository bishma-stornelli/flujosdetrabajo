from django.contrib.auth.models import User
from flujos.models import Flujo, Paso, Criterio
from unidades.models import Unidad


u1 = User.objects.create(username='u1', password='u1')
u1.save()
u2 = User.objects.create(username='u2', password='u2')
unidad1 = Unidad.objects.create(nombre="unidad1", descripcion="descripcion1", responsable=u1, miembros=(u1))
u2.save()
flujo1 = Flujo.objects.create(nombre="flujo1", descripcion="flujo1",unidad=unidad1)
flujo1.save()
p1 = Paso.objects.create(nombre="p1", descripcion="p1",flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p1.save()
p2 = Paso.objects.create(nombre="p2", descripcion="p2",flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p3 = Paso.objects.create(nombre="p3", descripcion="p3",flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p4 = Paso.objects.create(nombre="p4", descripcion="p4",flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p5 = Paso.objects.create(nombre="p5", descripcion="p5",flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p6 = Paso.objects.create(nombre="p6", descripcion="p6",flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p7 = Paso.objects.create(nombre="p7", descripcion="p7",flujo=flujo1, tipo=Paso.TIPO_NORMAL)
p8 = Paso.objects.create(nombre="p8", descripcion="p8",flujo=flujo1, tipo=Paso.TIPO_FINAL)
p9 = Paso.objects.create(nombre="p9", descripcion="p9",flujo=flujo1, tipo=Paso.TIPO_DIVISION)
p10 = Paso.objects.create(nombre="p10", descripcion="p10",flujo=flujo1, tipo=Paso.TIPO_UNION)
c1 = Criterio.objects.create(paso_origen=p1,paso_destino=p2,descripcion="vacia",expresion="true")
c2 = Criterio.objects.create(paso_origen=p1,paso_destino=p3,descripcion="vacia",expresion="true")
c3 = Criterio.objects.create(paso_origen=p2,paso_destino=p3,descripcion="vacia",expresion="true")
c4 = Criterio.objects.create(paso_origen=p3,paso_destino=p9,descripcion="vacia",expresion="true")
c5 = Criterio.objects.create(paso_origen=p9,paso_destino=p4,descripcion="vacia",expresion="true")
c6 = Criterio.objects.create(paso_origen=p9,paso_destino=p5,descripcion="vacia",expresion="true")
c7 = Criterio.objects.create(paso_origen=p4,paso_destino=p10,descripcion="vacia",expresion="true")
c8 = Criterio.objects.create(paso_origen=p5,paso_destino=p10,descripcion="vacia",expresion="true")
c9 = Criterio.objects.create(paso_origen=p10,paso_destino=p6,descripcion="vacia",expresion="true")
c10= Criterio.objects.create(paso_origen=p6,paso_destino=p8,descripcion="vacia",expresion="true")
c11= Criterio.objects.create(paso_origen=p2,paso_destino=p7,descripcion="vacia",expresion="true")
c12= Criterio.objects.create(paso_origen=p7,paso_destino=p8,descripcion="vacia",expresion="true")
