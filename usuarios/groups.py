from django.contrib.auth.models import Group

miembro = Group(name='Miembro de Unidad')
miembro.save()

responsable = Group(name='Responsable de Unidad')
responsable.save()

solicitante = Group(name='Solicitante')
solicitante.save()


