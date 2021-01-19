from rest_framework import routers

from .api.send_values_api import CorrelationsViewSet, LinksViewSet, ResearcherViewSet

router = routers.DefaultRouter()
router.register(r"correlations", CorrelationsViewSet)
router.register(r"researchers", ResearcherViewSet)
router.register(r"links", LinksViewSet)
urlpatterns = router.urls
