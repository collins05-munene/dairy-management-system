from django.db import models
from django.core.validators import RegexValidator
from django.db.models import Sum
from django.core.validators import MinValueValidator

# Create your models here.
name_regex = RegexValidator(
    regex = r'^[a-zA-Z]$',
    message = "Name can only be in letters"
)

class BrandCategory(models.Model):
    name = models.CharField(validators=[name_regex], max_length=30)

    def __str__(self):
        return self.name

class NetWeight(models.Model):
    net_weight = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.net_weight} KG(s)"
    
class FeedCategory(models.Model):
    name = models.CharField(validators=[name_regex], max_length=30)

    def __str__(self):
        return self.name
    

class FeedStock(models.Model):
    feed_category = models.ForeignKey(FeedCategory, on_delete=models.CASCADE, null=False)

    brand_category = models.ForeignKey(BrandCategory, on_delete=models.CASCADE, null=False)

    net_weight = models.ForeignKey(NetWeight, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('brand_category', 'feed_category', 'net_weight')

    @property
    def bags_in_stock(self):
        total_in = self.transactions.filter(transaction_type='IN').aggregate(total=Sum('quantity'))['total'] or 0

        total_out = self.transactions.filter(transaction_type='OUT').aggregate(total=Sum('quantity'))['total'] or 0

        return total_in - total_out
    

class FeedTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out')
    )

    feed_stock = models.ForeignKey(
        FeedStock,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.quantity}"
