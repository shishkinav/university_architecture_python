from views import MainPage, Contacts, AboutPage


urlpatterns = {
    '/': MainPage(),
    '/contacts': Contacts(),
    '/about': AboutPage(),
}