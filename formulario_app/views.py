from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import requests
from .models import Cita
from datetime import datetime

def registrar_cita(request):

    # --------- API ESTABLECIMIENTOS ---------
    try:
        url_est = "https://app6.dirislimacentro.gob.pe/SihceApi/establecimientos"
        response_est = requests.get(url_est, timeout=10)
        establecimientos = response_est.json()
    except Exception as e:
        establecimientos = []
        print("Error API establecimientos:", e)

    # --------- API UPS ---------
    try:
        url_ups = "https://app6.dirislimacentro.gob.pe/SihceApi/ups"
        response_ups = requests.get(url_ups, timeout=10)
        ups_lista = response_ups.json()
    except Exception as e:
        ups_lista = []
        print("Error API UPS:", e)

    # --------- GUARDAR Y ENVIAR ---------
    if request.method == 'POST':

        tipo_documento = request.POST.get('tipo_documento')
        numero_doc = request.POST.get('numero_doc')
        fecha_nacimiento_raw = request.POST.get('fecha_nacimiento')
        establecimiento = request.POST.get('establecimiento')
        ups = request.POST.get('ups')
        servicio = request.POST.get('servicio')

        #   Convertir fecha a dd-mm-yyyy
        try:
            fecha_obj = datetime.strptime(fecha_nacimiento_raw, "%Y-%m-%d")
            fecha_formateada = fecha_obj.strftime("%d-%m-%Y")
        except Exception:
            fecha_formateada = fecha_nacimiento_raw

        #   Guardar en tu BD
        Cita.objects.create(
            tipo_documento=tipo_documento,
            numero_doc=numero_doc,
            fecha_nacimiento=fecha_formateada,
            establecimiento=establecimiento,
            ups=ups,
            servicio=servicio
        )

        #   Enviar a API externa
        url_post = "https://app6.dirislimacentro.gob.pe/SihceApi/Scraper/registrar-cita-form"

        payload = {
            "servicio": servicio,
            "ups": ups,
            "establecimiento": establecimiento,
            "fechaNacimiento": fecha_formateada,   
            "numeroDocumento": numero_doc,
            "tipoDocumento": tipo_documento
        }

        try:
            response = requests.post(url_post, data=payload, timeout=None)

            # Si devuelve JSON
            try:
                respuesta_api = response.json()
            except:
                respuesta_api = response.text

            messages.success(request, f"Respuesta API: {respuesta_api}")

        except Exception as e:
            messages.error(request, f"Error al consumir API externa: {str(e)}")

        return redirect('registrar_cita')

    return render(request, 'formulario_app/formulario.html', {
        'establecimientos': establecimientos,
        'ups_lista': ups_lista
    })

def obtener_servicios(request):
    ups_valor = request.GET.get('ups')

    if not ups_valor:
        return JsonResponse({'error': 'UPS no enviado'}, status=400)

    try:
        # IMPORTANTE: el espacio se maneja automáticamente con encodeURIComponent en JS
        url = f"https://app6.dirislimacentro.gob.pe/SihceApi/servicios/{ups_valor}"
        
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return JsonResponse({'error': 'Error API externa'}, status=500)

        data = response.json()

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)