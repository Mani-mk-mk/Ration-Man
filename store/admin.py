from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(List)
admin.site.register(ListItem)
admin.site.register(PreviousOrder)
admin.site.register(PreviousOrderItem)
admin.site.register(Monthly)
admin.site.register(MonthlyItem)
admin.site.register(Party)
admin.site.register(PartyItem)

