from django.urls import path

from .views import HomePageView, AboutPageView, TocoPageView, ResultsPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("toco/", TocoPageView.as_view(), name="toco"),
    path(
        "results/<int:years_of_experience>/<str:gmat_score>/",
        ResultsPageView.as_view(),
        name="results"
    ),
]
