from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from basketapp.models import BasketItem


# @user_passes_test(lambda user: user.is_authenticated)
from geekshop.settings import LOGIN_URL


@login_required
def index(request):
    basket = request.user.basket.all()
    context = {
        'page_title': 'корзина',
        'basket': basket,
    }
    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, product_pk):
    if LOGIN_URL in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(
            reverse('main:product_page', args=[product_pk])
        )
    basket_item, _ = BasketItem.objects.get_or_create(
        user=request.user,
        product_id=product_pk
    )
    basket_item.qty += 1
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # возврат туда, откуда пришли


@login_required
def remove(request, basket_item_pk):
    item = get_object_or_404(BasketItem, pk=basket_item_pk)
    item.delete()
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(reverse('basket:index'))
