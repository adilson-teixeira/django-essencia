from django.db import models
from django.urls import reverse_lazy

from  mysrc.core.models import TimeStampedModel


class Customer(models.Model):
    first_name = models.CharField('nome', max_length=50)
    last_name = models.CharField('sobrenome', max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    class Meta: 
        ordering=('first_name',)
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name or ""}'.strip()

    def __str__(self):
        return self.full_name



class Expense(TimeStampedModel):
    description = models.CharField('descrição', max_length=100)
    payment_date = models.DateTimeField('data de pagamento', null=True, blank=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        verbose_name='pago a',
        related_name='expenses',
        null=True,
        blank=True
    )
    value = models.DecimalField('valor', max_digits=7, decimal_places=2)
    paid = models.BooleanField('pago', default=False)

    class Meta:
        ordering = ('-payment_date',)# o traço faz com que a ordem seja do mais recente
        verbose_name = 'despesa'
        verbose_name_plural = 'despesas'

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse_lazy('expense:expense_detail', kwargs={'pk':self.pk})
