from django.urls import path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    # path('', adminapp.index, name='index'),
    path('', adminapp.ShopUserList.as_view(), name='index'),

    path('admin/user/create/', adminapp.ShopUserAdminCreate.as_view(), name='shop_user_create'),

    # path('admin/user/delete/<int:user_pk>', adminapp.user_delete, name='user_delete'),
    path('admin/delete/<int:user_pk>', adminapp.ShopUserAdminDelete.as_view(), name='user_delete'),

    # path('admin/update/<int:user_pk>', adminapp.user_update, name='user_update'),
    path('admin/user/update/<int:user_pk>', adminapp.ShopUserAdminUpdate.as_view(), name='user_update'),

    # path('admin/categories/', adminapp.categories, name='categories'),
    path('admin/categories/', adminapp.ProductCategoryList.as_view(), name='categories'),

    path('admin/category/create/', adminapp.ProductCategoryCreate.as_view(), name='category_create'),

    path('admin/category/update/<int:pk>/', adminapp.ProductCategoryUpdate.as_view(), name='category_update'),

    path('admin/category/delete/<int:pk>/', adminapp.ProductCategoryDelete.as_view(), name='category_delete'),
]
