from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (Home, Checkout, ProductDetail, 
                add_to_cart, remove_from_cart, 
                OrderSummary, remove_single_item_from_cart,
                PayPalPayment, payment_done, payment_canceled, 
                Search, AddCoupon, StripePayment, RefundRequest,
                UserProfileView, AddLenses, RemoveLenses)
                
app_name = "core"
handler404 = 'core.views.page_not_found_view'

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("order-summary/", OrderSummary.as_view(), name="order-summary"),
    path("checkout/", Checkout.as_view(), name="checkout"),
    path("product/<slug>", ProductDetail.as_view(), name="product-detail"),
    path("add-to-cart/<slug>", add_to_cart, name="add_to_cart"),
    path("add-coupon/", AddCoupon.as_view(), name="add_coupon"),
    path("add-lenses/<slug>", AddLenses.as_view(), name="add_lenses"),
    path("remove-lenses/<slug>", RemoveLenses.as_view(), name="remove_lenses"),
    path("remove-from-cart/<slug>", remove_from_cart, name="remove_from_cart"),
    path("remove-single-item-from-cart/<slug>", remove_single_item_from_cart, name="remove_single_item_from_cart"),
    path('paypal-payment/', PayPalPayment.as_view(), name='paypal_payment'),
    path('stripe-payment/', StripePayment.as_view(), name='stripe_payment'),
    path('payment-done/', payment_done, name='payment_done'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
    path('search/',Search.as_view(), name='search'),
    path("refund-request/", RefundRequest.as_view(), name="refund_request"),
    path("user/", UserProfileView.as_view(), name="user_profile"),


    # REST API URL
    path('api/', include('core.api.urls', namespace="api")),
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)