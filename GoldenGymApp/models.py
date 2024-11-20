
from django.db import models

class Cliente(models.Model):
    PLANES_MEMBRESIA = [
        ('SEMANAL', 'Semanal - $15,000'),
        ('MENSUAL', 'Mensual - $28,000'),
        ('TRIMESTRAL', 'Trimestral - $75,000'),
        ('SEMESTRAL', 'Semestral - $135,000'),
    ]

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField(unique=True)
    membresia = models.CharField(max_length=10, choices=PLANES_MEMBRESIA)
    suscripcion_activa = models.BooleanField(default=False)  # Suscripción activa

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.membresia}"


class Encargado(models.Model):
    # Nombre del encargado
    nombre = models.CharField(max_length=100)

    # Apellido del encargado
    apellido = models.CharField(max_length=100)

    # RUT (Rol Único Tributario) del encargado
    rut = models.CharField(max_length=12, unique=True)

    # Correo electrónico del encargado
    correo = models.EmailField(max_length=100, unique=True)

    # Nombre de usuario para login
    usuario = models.CharField(max_length=50, unique=True)

    # Contraseña para login (se recomienda usar el sistema de autenticación de Django)
    contraseña = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.usuario})"
    


class Novedad(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='img/', blank=True, null=True)  # Usar ImageField
    ruta_video = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.titulo
