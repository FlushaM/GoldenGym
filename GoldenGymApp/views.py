from django.shortcuts import render, redirect, get_object_or_404
from GoldenGymApp.models import Cliente,Encargado,Novedad
from GoldenGymApp.forms import ClienteForm,EncargadoForm,NovedadForm,ReporteForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse

def gestion_clientes(request):
    if request.method == 'POST':
        if 'cliente_id' in request.POST:
            cliente = get_object_or_404(Cliente, id=request.POST['cliente_id'])
            form = ClienteForm(request.POST, instance=cliente)
        else:
            form = ClienteForm(request.POST)

        # Verifica si el formulario es válido
        if form.is_valid():
            form.save()
            return redirect('gestion_clientes')  # Redirige después de guardar
        else:
            print(form.errors)  # Imprime los errores del formulario para depuración
    else:
        form = ClienteForm()

    clientes = Cliente.objects.all()
    return render(request, 'GoldenGymApp/gestion_cliente.html', {'form': form, 'clientes': clientes})


def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('gestion_clientes')  # Redirige a la lista de clientes después de guardar
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'GoldenGymApp/gestion_cliente.html', {'form': form, 'cliente': cliente})


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


from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Reporte
from .forms import ReporteForm

# Vista para mostrar los reportes de un cliente
def reportes_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    reportes = cliente.reportes.all()  # Obtener todos los reportes de este cliente

    return render(request, 'GoldenGymApp/reportes_cliente.html', {
        'cliente': cliente,
        'reportes': reportes
    })

# Vista para crear un nuevo reporte para un cliente


def crear_reporte(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.cliente = cliente  # Asociamos el reporte al cliente
            reporte.save()
            # Si la solicitud es AJAX, devolver una respuesta JSON
            if request.is_ajax():
                return JsonResponse({'success': True})
            # Si no es AJAX, redirigir como de costumbre
            return redirect('reportes_cliente', cliente_id=cliente.id)
        else:
            # Si el formulario no es válido, devolver error
            if request.is_ajax():
                return JsonResponse({'success': False})
    
    else:
        form = ReporteForm()

    return render(request, 'GoldenGymApp/crear_reporte.html', {
        'form': form,
        'cliente': cliente
    })


def editar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    if request.method == 'POST':
        form = ReporteForm(request.POST, instance=reporte)
        if form.is_valid():
            form.save()
            return redirect('reportes_cliente', cliente_id=reporte.cliente.id)
    else:
        form = ReporteForm(instance=reporte)

    return render(request, 'GoldenGymApp/editar_reporte.html', {'form': form, 'reporte': reporte})



def eliminar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    cliente_id = reporte.cliente.id  # Guardar el ID del cliente para redirigir después
    print(f"Se está eliminando el reporte del cliente con ID: {cliente_id}")
    reporte.delete()
    return redirect('reportes_cliente', cliente_id=cliente_id)