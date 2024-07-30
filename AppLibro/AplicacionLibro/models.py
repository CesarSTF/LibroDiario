from django.db import models
from django.core.exceptions import ValidationError


class LibroDiario(models.Model):
    fecha = models.DateField()
    descripcion = models.CharField(max_length=100)
    saldoInicialCaja = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    saldoInicialBanco = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    saldoFinalCaja = models.DecimalField(max_digits=18, decimal_places=2, default=0, editable=False)
    saldoFinalBanco = models.DecimalField(max_digits=18, decimal_places=2, default=0, editable=False)
    ivaIngresoTotal = models.DecimalField(max_digits=18, decimal_places=2, default=0, editable=False)
    ivaEgresoTotal = models.DecimalField(max_digits=18, decimal_places=2, default=0, editable=False)

    def calcular_saldo_final(self):
        entradas = self.entradadiario_set.all()
        total_ingreso_caja = sum(entrada.ingresoCaja for entrada in entradas)
        total_egreso_caja = sum(entrada.egresoCaja for entrada in entradas)
        total_ingreso_banco = sum(entrada.ingresoBanco for entrada in entradas)
        total_egreso_banco = sum(entrada.egresoBanco for entrada in entradas)

        self.saldoFinalCaja = self.saldoInicialCaja + total_ingreso_caja - total_egreso_caja
        self.saldoFinalBanco = self.saldoInicialBanco + total_ingreso_banco - total_egreso_banco

        # Calcular IVA total
        self.ivaIngresoTotal = sum(entrada.ivaIngreso for entrada in entradas)
        self.ivaEgresoTotal = sum(entrada.ivaEgreso for entrada in entradas)

    def save(self, *args, **kwargs):
        if self.pk:
            self.calcular_saldo_final()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.descripcion

from django.db import models
from django.core.exceptions import ValidationError

class EntradaDiario(models.Model):
    descripcion = models.CharField(max_length=255)
    ingresoCaja = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    egresoCaja = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ingresoBanco = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    egresoBanco = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # IVA en porcentaje
    ivaIngreso = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    ivaEgreso = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    libroDiario = models.ForeignKey('LibroDiario', on_delete=models.CASCADE)
    fecha = models.DateField()

    @property
    def monto(self):
        """Calcula el monto total de ingresos y egresos."""
        return self.ingresoCaja + self.egresoCaja + self.ingresoBanco + self.egresoBanco

    @property
    def iva_total(self):
        """Calcula el total de IVA basado en el monto."""
        return (self.monto * self.iva) / 100

    @property
    def numeroComprobante(self):
        """Devuelve el número de comprobante basado en el ID."""
        return self.id

    def clean(self):
        """Validaciones para asegurar que los valores no sean negativos y el IVA sea válido."""
        if self.ingresoCaja < 0:
            raise ValidationError('El ingreso en caja no puede ser negativo.')
        if self.egresoCaja < 0:
            raise ValidationError('El egreso en caja no puede ser negativo.')
        if self.ingresoBanco < 0:
            raise ValidationError('El ingreso en banco no puede ser negativo.')
        if self.egresoBanco < 0:
            raise ValidationError('El egreso en banco no puede ser negativo.')
        if self.iva < 0 or self.iva > 100:
            raise ValidationError('El IVA debe estar entre 0 y 100.')

    def save(self, *args, **kwargs):
        """Calcula IVA de ingreso y egreso antes de guardar el modelo."""
        self.clean()
        self.ivaIngreso = (self.ingresoCaja + self.ingresoBanco) * self.iva / 100
        self.ivaEgreso = (self.egresoCaja + self.egresoBanco) * self.iva / 100
        super().save(*args, **kwargs)
