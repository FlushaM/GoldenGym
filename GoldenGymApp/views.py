from django.shortcuts import render, redirect, get_object_or_404
from GoldenGymApp.models import Cliente,Encargado,Novedad
from GoldenGymApp.forms import ClienteForm,EncargadoForm,NovedadForm
from django.urls import reverse
from django.http import HttpResponseRedirect

def gestion_clientes(request):
    # Si el método es POST, es porque se envió el formulario
    if request.method == 'POST':
        if 'cliente_id' in request.POST:
            # Editar cliente existente
            cliente = get_object_or_404(Cliente, id=request.POST['cliente_id'])
            form = ClienteForm(request.POST, instance=cliente)
        else:
            # Crear nuevo cliente
            form = ClienteForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('gestion_clientes')  # Redirige después de guardar para evitar re-envío del formulario

    else:
        form = ClienteForm()  # Formulario vacío para crear un nuevo cliente

    # Obtener la lista de todos los clientes
    clientes = Cliente.objects.all()
    return render(request, 'GoldenGymApp/gestion_cliente.html', {'form': form, 'clientes': clientes})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return HttpResponseRedirect(reverse('gestion_clientes'))


def gestion_encargados(request):
    if request.method == 'POST':
        if 'encargado_id' in request.POST:
            # Editar encargado existente
            encargado = get_object_or_404(Encargado, id=request.POST['encargado_id'])
            form = EncargadoForm(request.POST, instance=encargado)
        else:
            # Crear nuevo encargado
            form = EncargadoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('gestion_encargados')  # Redirige para evitar reenvíos de formulario

    else:
        form = EncargadoForm()  # Formulario vacío para crear un nuevo encargado

    # Obtener la lista de todos los encargados
    encargados = Encargado.objects.all()
    return render(request, 'GoldenGymApp/gestion_encargado.html', {'form': form, 'encargados': encargados})

# Vista para eliminar encargado
def eliminar_encargado(request, encargado_id):
    encargado = get_object_or_404(Encargado, id=encargado_id)
    encargado.delete()
    return HttpResponseRedirect(reverse('gestion_encargados'))


def validar_ingreso(request):
    mensaje = None

    if request.method == "POST":
        rut_ingresado = request.POST.get("rut")

        # Buscar al cliente en la base de datos por su RUT
        try:
            cliente = Cliente.objects.get(rut=rut_ingresado)
            # Verificar si tiene una suscripción activa (esto dependerá de tu lógica de negocio)
            if cliente.suscripcion_activa:  # Asegúrate de que tienes este campo en tu modelo
                mensaje = "Ingreso permitido. Bienvenido al gimnasio."
            else:
                mensaje = "Acceso denegado. No tiene una suscripción activa."
        except Cliente.DoesNotExist:
            mensaje = "RUT no registrado. Verifique su información."

    return render(request, "GoldenGymApp/validar_ingreso.html", {"mensaje": mensaje})


def novedades(request):
    # Obtener todas las novedades y ordenarlas por fecha de publicación
    novedades = Novedad.objects.all().order_by('-fecha_publicacion')

    # Reemplazar los saltos de línea por <br> en cada novedad
    for novedad in novedades:
        novedad.contenido_formateado = novedad.contenido.replace('\n', '<br>')

    return render(request, 'GoldenGymApp/novedades.html', {'novedades': novedades})