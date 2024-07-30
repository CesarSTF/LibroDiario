from django.db import models

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

class EntradaDiario(models.Model):
    libroDiario = models.ForeignKey(LibroDiario, on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=100)
    numeroComprobante = models.CharField(max_length=10, editable=False)
    ingresoCaja = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    egresoCaja = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    ingresoBanco = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    egresoBanco = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    ivaIngreso = models.DecimalField(max_digits=18, decimal_places=2, default=0, editable=False)
    ivaEgreso = models.DecimalField(max_digits=18, decimal_places=2, default=0, editable=False)

    def save(self, *args, **kwargs):
        # Calcular IVA de ingreso y egreso
        self.ivaIngreso = (self.ingresoCaja + self.ingresoBanco) * self.iva / 100
        self.ivaEgreso = (self.egresoCaja + self.egresoBanco) * self.iva / 100

        if not self.numeroComprobante:
            last_entry = EntradaDiario.objects.filter(libroDiario=self.libroDiario).order_by('id').last()
            if last_entry:
                last_num = int(last_entry.numeroComprobante)
                self.numeroComprobante = f"{last_num + 1:02d}"
            else:
                self.numeroComprobante = "01"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.descripcion
