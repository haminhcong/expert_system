from django.contrib import admin
from models import StoreItem, ItemProperty, PropertyValue, RuleModel, LeftFactModel, RightFactModel

admin.site.register(StoreItem)
admin.site.register(ItemProperty)
admin.site.register(PropertyValue)
admin.site.register(RuleModel)
admin.site.register(LeftFactModel)
admin.site.register(RightFactModel)

# Register your models here.
