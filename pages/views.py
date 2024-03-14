import pickle

from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Toco Tachibana"
        context["numbers"] = [1, 2, 3, 4, 5]
        context["error_message"] = None
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request):
        years_of_experience = request.POST.get("years")
        try:
            gmat_score = float(request.POST.get("gmat"))
        except TypeError as e:
            contexts = self.get_context_data()
            contexts["error_message"] = f"Error: {e}"
            return render(request, self.template_name, contexts)

        return redirect(
            "results",
            years_of_experience=years_of_experience,
            gmat_score=gmat_score,
        )


class ResultsPageView(TemplateView):
    template_name = "results.html"

    def get_context_data(self, **kwargs):
        with open("model_pkl", "rb") as f:
            model = pickle.load(f)
        admission_decision = model.predict([[
            kwargs["years_of_experience"],
            float(kwargs["gmat_score"]),
        ]])

        context = super().get_context_data(**kwargs)
        context["years_of_experience"] = kwargs["years_of_experience"]
        context["gmat_score"] = kwargs["gmat_score"]
        context["admission_decision"] = (
            "Accepted" if admission_decision[0] == 1 else "Rejected"
        )
        return context


class AboutPageView(TemplateView):
    template_name = "about.html"


class TocoPageView(TemplateView):
    template_name = "toco.html"
