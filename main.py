from light_beam.core import LightBeamApp
from urls import urlpatterns
from frontapp.controllers import controllers


app = LightBeamApp(urlpatterns, controllers)