from views import MainPage, Contacts


urlpatterns = {
    '/': MainPage(),
    '/contacts': Contacts()
}