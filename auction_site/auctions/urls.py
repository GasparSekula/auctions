from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import AuctionViewSet

router = DefaultRouter()
router.register(r'auctions', AuctionViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('auctions/', views.auction_list, name='auction_list'),
    path('auctions/<int:pk>/', views.auction_detail, name='auction_detail'),
    path('auctions/create/', views.auction_create, name='auction_create'),
    path('search/', views.search, name='search'),
    path('watchlist/', views.view_watchlist, name='view_watchlist'),
    path('add_to_watchlist/<int:pk>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:pk>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('user_auctions', views.user_auctions, name='user_auctions'),
    path('notifications/', views.notifications, name='notifications'),
    path('api/', include(router.urls)),
    path('export_auctions/<str:format>/', views.export_auctions, name='export_auctions'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
