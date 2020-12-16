from django.shortcuts import render
from .models import Product, Contact, Order, Orderupdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from paytm import checksum

MERCHANT_KEY='dtq%JUmdUr95YFeZ'
# Create your views here.
from django.http import HttpResponse

def index(request):
    #products = Product.objects.all()
    #print(products)
    
    
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n//4 + ceil((n/4)-(n//4))

        allprods.append([prod, range(1, nslides), nslides])
    #params={'no_of_slides':nslides, 'range': range(1,nslides), 'product': products}
    #allprods = [[products, range(1, nslides), nslides], 
    #[products, range(1, nslides), nslides]]
    params = {'allprods':allprods}
    return render(request, 'shop/index2.html', params)

def searchMatch(query, item):
    if query in item.description.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.Subcategory.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nslides = n//4 + ceil((n/4)-(n//4))
        if len(prod) != 0:
            allprods.append([prod, range(1, nslides), nslides])
    #params={'no_of_slides':nslides, 'range': range(1,nslides), 'product': products}
    #allprods = [[products, range(1, nslides), nslides], 
    #[products, range(1, nslides), nslides]]
    params = {'allprods':allprods, 'msg': ""}
    if len(allprods) == 0:
        params = {'msg': "Please enter a relevant query"}
    return render(request, 'shop/search.html', params)
    

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank = False
    if request.method=="POST":
        print(request)
        name = request.POST.get('name', '')
        
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        
    return render(request, 'shop/contact.html', {'thank': thank})

def tracker(request):
    if request.method=="POST":
        orderid = request.POST.get('orderid', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderid, email=email)
            if len(order)>0:
                update = Orderupdate.objects.filter(order_id=orderid)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "update":updates, "itemsJson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
   

    return render(request, 'shop/tracker.html')



def products(request, myid):
    #fetch the product using id
    product = Product.objects.filter(id=myid)
    
    return render(request, 'shop/products.html', {'product':product[0]})

def checkout(request):
    if request.method=="POST":
        
        items_json = request.POST.get('itemsjson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        order = Order(items_json=items_json, name=name, email=email, phone=phone, address=address, city=city, state=state, zip_code=zip_code, amount=amount)
        order.save()
        update = Orderupdate(order_id=order.order_id, update_desc="The order have been placed")
        update.save()
        thank = True
        id = order.order_id
        #return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
        #request paytm to transfer the amount from user
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
    return render(request, 'shop/checkout.html')


    
