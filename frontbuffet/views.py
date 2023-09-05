from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import FoodOffer


def index(request):
    latest_question_list = FoodOffer.objects.all()
    template = loader.get_template("frontbuffet/index.html")
    context = {
        "all_offers_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, offer_id):
    try:
        offer = FoodOffer.objects.get(pk=offer_id)
    except FoodOffer.DoesNotExist:
        raise Http404("Offer does not exist")
    return render(request, "frontbuffet/detail.html", {"offer": offer})
