from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)), # Admin config
    url(r'^$', 'shop.views.home', name='home'), # Home config
    # customer register
    url(r'^customers/register/$', 'shop.views.register_user'),
    url(r'^customers/register_success/$', 'shop.views.register_success'),     
    # customer login/logout
    url(r'^customers/login/$', 'shop.views.login'),
    url(r'^customers/auth/$', 'shop.views.auth_view'),
    url(r'^customers/logout/$', 'shop.views.logout'),
    url(r'^customers/login_success/$', 'shop.views.login_success'),
    url(r'^customers/login_invalid/$', 'shop.views.login_invalid'),
    # customer account
    url(r'^customers/account/$', 'shop.views.account_detail'),
    # store page
    url(r'^stores/books/$', 'shop.views.bookstore'),
    url(r'^stores/movies/$', 'shop.views.moviestore'),
    url(r'^stores/drinks/$', 'shop.views.drinkstore'),
    # session-based shopping cart
    url(r'^addToCart/$', 'shop.views.addToCart'),
    url(r'^view_cart/$', 'shop.views.view_cart'),
    # checkout
    url(r'^checkout/$', 'shop.views.checkout'),
    url(r'^order_process/$', 'shop.views.order_process'),
    url(r'^order_invalid/$', 'shop.views.order_invalid'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
