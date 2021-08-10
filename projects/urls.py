from rest_framework import routers

from projects.views import ProjectViewSet


app_name = 'projects'

router = routers.SimpleRouter()
router.register(r'', ProjectViewSet)
urlpatterns = router.urls
