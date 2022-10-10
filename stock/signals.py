from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Transaction, Product


# Transaction modelde ürün girildiği zaman price_total i otomatik olarak hesaplaması için kullanıldı

# def ready(self):     apps.py eklenmeli, !UNUTULMAMALI
        # import stock.signals


@receiver(pre_save, sender=Transaction)
def calculate_total_price(sender, instance, **kwargs):
    if not instance.price_total:
        instance.price_total = instance.quantity*instance.price


#farklı modeller ile islem yapıldıgından dolayı signals kullanılması dogru yontem
@receiver(post_save, sender=Transaction)
def update_stock(sender, instance, **kwargs):
    product = Product.objects.get(id=instance.product_id)
    if instance.transaction == 1 :
        if not product.stock:
            product.stock = instance.quantity
        else:
            product.stock += instance.quantity 

    else:
        product.stock -= instance.quantity
        #burada quantity null gelme durumunu serializers da halledeceğiz, ayrıca  error msj verebilmemiz icin serializers da yapılacak

    product.save()                 
