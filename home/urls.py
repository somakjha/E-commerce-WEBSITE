from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('',views.landing_page,name='landing'),
    path('landing_page', views.landing_page, name='landing'),
    path('landing_page_with_context', views.landing_page_with_context, name='landing_page_with_context'),
    path('home',views.home_page,name='home'),
    path("register", views.landing_page_register, name="reg"),
    path("texts", views.texts_page, name="texts"),
    path("interests", views.interests_page, name="interests"),
    path("confirmations", views.confirmations_page, name="confirmations"),
    path("buy", views.buy_page, name="buy"),
    path("sell", views.sell_page, name="sell"),
    path("rent", views.rent_page, name="rent"),
    path("lease", views.lease_page, name="lease"),
    path("render_service", views.render_service_page, name="render_service"),
    path("require_service", views.require_service_page, name="require_service"),
    path("account_details", views.account_details_page, name="account_details"),
    path("all_transactions", views.all_transactions_page, name="all_transactions"),
    path("forgot_password", views.forgot_password, name="forgot_password"),
    path("logout", views.logout, name="logout"),
    path("login", views.login, name="login"),
    path("contributors", views.contributors, name="contributors"),
    path("ad_page", views.ad_page, name="ad_page")

]