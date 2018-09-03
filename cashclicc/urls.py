from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin

from cashclicc.core import views as core_views


urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^account/passwordreset', core_views.reset_password, name="reset_password"),
    url(r'^refresh_game/(?P<game_id>[0-9]+)/$', core_views.refresh_game, name="refresh_game"),
    url(r'^withdraw/', core_views.withdraw, name='withdraw'),
    url(r'^games/(?P<game_id>[0-9]+)', core_views.game_page, name='game_page'),
    url(r'^games/', core_views.games, name='games'),
    url(r'^contact/', core_views.contact, name='contact'),
    url(r'^tutorial/', core_views.tutorial, name='tutorial'),
    url(r'^about/', core_views.about, name='about'),
    url(r'^activate/(?P<user_id>[0-9]+)/$', core_views.activate, name='activate'),
    url(r'^login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': 'home'}, name='logout'),
    url(r'^signup/', core_views.signup, name='signup'),
    url(r'^signup/', core_views.signup, name='signup'),
    url(r'^account/', core_views.account, name='account'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^store/', core_views.store, name='store'),
    url(r'^donations/', core_views.donations, name='donations'),
]
