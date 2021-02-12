from django.contrib import admin

from .models import OrderItem, Order, Item, Address, Payment, Coupon, UserProfile, EyeLenses


def make_refund_accepted(modelAdmin, request, queryset):
    queryset.update(refund_request=False, refund_granted = True)

make_refund_accepted.short_description = 'Update Refund Granted to accepted'

class OrderAdmin(admin.ModelAdmin):
    ordering = ['ordered', 'order_date']
    list_display = [
                    'user',
                    'ordered',
                    'order_date',
                    'delivered',
                    'received',
                    'refund_request',
                    'refund_granted',
                    'shipping_address',
                    'coupon',
                    'payment',
                    'ref_code',
                    'delivered',
                    'received',
                    'failed_confirm',
                    'in_process_delivery',   
    ]
    list_display_links = [
                    'user',
                    'shipping_address',
                    'delivered',
                    'in_process_delivery',   
                    'coupon',
                    'payment',
                    'failed_confirm',
                    'received',  
                    
    ]

    search_fields = [
        'user__username',
        'ref_code',
    ]
    list_filter = [
                    'ordered',
                    'order_date',
                    'delivered',
                    'received',
                    'refund_request',
                    'refund_granted',
                    'failed_confirm',
                    'in_process_delivery',   

    ]

    actions = [make_refund_accepted]

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip_code',
        'address_type',
        'default',
    ]

    search_fields = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip_code',
        'address_type',
        'default',
    ]

    list_filter = ['default', 'address_type', 'country']


    
admin.site.register(Item)

admin.site.register(OrderItem)

admin.site.register(Order,OrderAdmin)

admin.site.register(Address, AddressAdmin)

admin.site.register(Payment)

admin.site.register(Coupon)

admin.site.register(UserProfile)

admin.site.register(EyeLenses)
