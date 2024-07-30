from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date

from .forms import LibroDiarioForm, EntradaDiarioForm
from .models import LibroDiario, EntradaDiario


def libro_diario(request):
    if request.method == 'POST':
        form = LibroDiarioForm(request.POST)
        if form.is_valid():
            libro = form.save()
            return redirect('entrada_diario', libro_diario_id=libro.id)
    else:
        form = LibroDiarioForm()
        # Obtenemos todos los libros diarios
        libros_diarios = LibroDiario.objects.all().prefetch_related('entradadiario_set')

        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        if fecha_inicio and fecha_fin:
            fecha_inicio = parse_date(fecha_inicio)
            fecha_fin = parse_date(fecha_fin)
            libros_diarios = libros_diarios.filter(
                entradadiario__fecha__range=[fecha_inicio, fecha_fin]
            ).distinct()

        context = {
            'form': form,
            'libros_diarios': [],
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
        }

        for libro in libros_diarios:
            entradas = libro.entradadiario_set.all()
            total_ingreso_caja = sum(entrada.ingresoCaja for entrada in entradas)
            total_egreso_caja = sum(entrada.egresoCaja for entrada in entradas)
            total_ingreso_banco = sum(entrada.ingresoBanco for entrada in entradas)
            total_egreso_banco = sum(entrada.egresoBanco for entrada in entradas)
            total_iva_ingreso = sum(entrada.ivaIngreso for entrada in entradas)
            total_iva_egreso = sum(entrada.ivaEgreso for entrada in entradas)

            saldo_final_caja = libro.saldoInicialCaja + total_ingreso_caja - total_egreso_caja
            saldo_final_banco = libro.saldoInicialBanco + total_ingreso_banco - total_egreso_banco
            ganancia_neta = saldo_final_caja + saldo_final_banco

            libro_totales = {
                'libro': libro,
                'totales': {
                    'ingreso_caja': total_ingreso_caja,
                    'egreso_caja': total_egreso_caja,
                    'ingreso_banco': total_ingreso_banco,
                    'egreso_banco': total_egreso_banco,
                    'iva_ingreso': total_iva_ingreso,
                    'iva_egreso': total_iva_egreso,
                    'saldo_final_caja': saldo_final_caja,
                    'saldo_final_banco': saldo_final_banco,
                    'ganancia_neta': ganancia_neta,
                }
            }
            context['libros_diarios'].append(libro_totales)

        return render(request, 'LibroDiario.html', context)
def entrada_diario(request, libro_diario_id):
    libro_diario = get_object_or_404(LibroDiario, id=libro_diario_id)
    if request.method == 'POST':
        form = EntradaDiarioForm(request.POST)
        if form.is_valid():
            entrada_diario = form.save(commit=False)
            entrada_diario.libroDiario = libro_diario
            entrada_diario.save()
            libro_diario.calcular_saldo_final()
            libro_diario.save()
            return redirect('libro_diario')
    else:
        form = EntradaDiarioForm()
    return render(request, 'EntradaDiario.html', {'form': form, 'libro_diario': libro_diario})

def modificar_entrada(request, entrada_id):
    entrada = get_object_or_404(EntradaDiario, id=entrada_id)
    if request.method == 'POST':
        form = EntradaDiarioForm(request.POST, instance=entrada)
        if form.is_valid():
            form.save()
            entrada.libroDiario.calcular_saldo_final()
            entrada.libroDiario.save()
            return redirect('libro_diario')
    else:
        form = EntradaDiarioForm(instance=entrada)
    return render(request, 'EntradaDiario.html', {'form': form, 'libro_diario': entrada.libroDiario})

def eliminar_entrada(request, entrada_id):
    entrada = get_object_or_404(EntradaDiario, id=entrada_id)
    libro_diario = entrada.libroDiario
    entrada.delete()
    libro_diario.calcular_saldo_final()
    libro_diario.save()
    return redirect('libro_diario')