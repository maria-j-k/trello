from rest_framework import routers

from projects.views import IssueViewSet, ProjectViewSet


app_name = 'projects'

router = routers.SimpleRouter()
router.register(r'', ProjectViewSet)
router.register(r'(?P<project_pk>[^/.]+)/issues', IssueViewSet)
urlpatterns = router.urls
