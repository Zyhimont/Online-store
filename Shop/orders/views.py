from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import *
from .forms import CheckoutContactForm


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    data = request.POST
    product_id = data.get("product_id")
    amount = data.get("am")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                     is_active=True, defaults={"quantity": amount})
        if not created:
            new_product.quantity += int(amount)
            new_product.save(force_update=True)

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_amount = products_in_basket.count()
    return_dict["products_total_amount"] = products_total_amount

    return_dict["products"] = list()
    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["product_name"] = item.product.product_name
        product_dict["item_price"] = item.item_price
        product_dict["quantity"] = item.quantity
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            print("Form is valid")
            data = request.POST
            name = data.get("name", "123456")
            phone = data["phone"]
            email = data.get("email")
            address = data.get("address")
            comments = data.get("comments")
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, customer_email=email,
                                         customer_address=address, comments=comments, status_id=1)
            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    product_in_basket.quantity = value
                    product_in_basket.order = order
                    product_in_basket.is_active = False
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product,
                                                  quantity=product_in_basket.quantity,
                                                  item_price=product_in_basket.item_price,
                                                  total_cost=product_in_basket.total_cost,
                                                  order=order)

        else:
            print("Form isn't valid")
    return render(request, 'orders/checkout.html', locals())
