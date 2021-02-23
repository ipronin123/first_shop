from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from adminapp.forms import AdminShopUserCreateUpdateForm, ProductCategoryCreateForm
from mainapp.models import ProductCategory


class SuperUserOnlyMixin:
    """"миксин который будет пробрасываться в классы, чтобы в админку можно было зайти только суперпользователям"""
    """"далее его надо будет пробросить ПЕРВЫМ аргуметом в классах"""

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title_key = 'page_title'
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.page_title_key] = self.page_title
        return context


# @user_passes_test(lambda user: user.is_superuser)
# def index(request):
#     all_users = get_user_model().objects.all()
#     context = {
#         'page_title': 'админка/пользователи',
#         'all_users': all_users,
#     }
#     return render(request, 'adminapp/index.html', context)


class ShopUserList(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = get_user_model()
    page_title = 'админка/пользователи/'


@user_passes_test(lambda user: user.is_superuser)
def user_delete(request, user_pk):
    """"пользователя делаем не активным, тк удалять пользователей плохая практика"""
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        return HttpResponseRedirect(reverse('my_admin:index'))

    context = {
        'page_title': 'админка/пользователи/удаление',
        'user_to_delete': user,
    }
    return render(request, 'adminapp/user_delete.html', context)


class ShopUserAdminDelete(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('my_admin:index')
    pk_url_kwarg = 'user_pk'
    page_title = 'пользователи/удаление'


# @user_passes_test(lambda user: user.is_superuser)
# def user_update(request, user_pk):
#     user = get_object_or_404(get_user_model(), pk=user_pk)
#     if request.method == 'POST':
#         user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('my_admin:index'))
#     else:
#         user_form = AdminShopUserUpdateForm(instance=user)
#
#     context = {
#         'page_title': 'админка/пользователи/редактирование',
#         'form': user_form,
#     }
#     return render(request, 'adminapp/shopuser_form.html', context)


class ShopUserAdminCreate(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = get_user_model()
    form_class = AdminShopUserCreateUpdateForm
    success_url = reverse_lazy('my_admin:index')
    page_title = 'пользователи/создание'


class ShopUserAdminUpdate(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    """"редактор юзеров"""
    model = get_user_model()
    form_class = AdminShopUserCreateUpdateForm
    # lazy срабатывает когда понадобится, если не указать, то грузится вместе с модулем
    success_url = reverse_lazy('my_admin:index')
    # уазать именнованный pk иначе сломается
    pk_url_kwarg = 'user_pk'
    page_title = 'пользователи/редактирование'


# @user_passes_test(lambda user: user.is_superuser)
# def categories(request):
#     context = {
#         'page_title': 'админка/категории',
#         'category_list': ProductCategory.objects.all()
#     }
#     return render(request, 'adminapp/productcategory_list.html', context)


class ProductCategoryList(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ProductCategory  # джанго ждем в шаблоне object_list т.к это listView
    page_title = 'админка/категории'


class ProductCategoryCreate(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ProductCategory
    # fields = '__all__'
    form_class = ProductCategoryCreateForm
    # lazy срабатывает когда понадобится, если не указать, то грузится вместе с модулем
    success_url = reverse_lazy('my_admin:categories')
    page_title = 'категории/создание'


class ProductCategoryUpdate(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    # fields = '__all__'
    # передаем форму, в которой уже заданы поля
    form_class = ProductCategoryCreateForm
    # lazy срабатывает когда понадобится, если не указать, то грузится вместе с модулем
    success_url = reverse_lazy('my_admin:categories')
    page_title = 'категории/редактирование'


class ProductCategoryDelete(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')
    page_title = 'категории/удаление'
