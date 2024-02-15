from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from properties.models import Property, Unit, Tenant, TenantAgreement
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
@login_required(login_url='/login')
def home(request):
    return render(request, "main/admin_home.html", {})
    
def property(request):
    if request.method == 'POST':
        obj = Property()
        obj.name = request.POST.get('propertyName')
        obj.address = request.POST.get('address')
        obj.location = request.POST.get('location')
        obj.features = request.POST.get('features')

        obj.save()
        return redirect('/property')
    datas = Property.objects.all()
    return render(request,"main/property.html",{"datas":datas})

def delete_property(request):
    prop_id = request.GET.get('Prop_id')
    Property.objects.get(id=prop_id).delete()
    return redirect('/property')

def update_property(request):
    prop_id = request.GET.get('Prop_id')
    data = Property.objects.get(id=prop_id)
    if request.method == 'POST':
        data.name = request.POST.get('propertyName')
        data.address = request.POST.get('address')
        data.location = request.POST.get('location')
        data.features = request.POST.get('features')

        data.save(update_fields=['name','address','location','features'])
        return redirect('/property')
    return render(request,"main/property_update.html",{'data':data})
    
def unit(request):
    prop_id = request.GET.get('Prop_id')
    data = Property.objects.get(id=prop_id)
    if request.method == 'POST':
        obj = Unit()
        obj.property = data
        obj.rent_cost = request.POST.get('cost')
        obj.type = request.POST.get('type')
        obj.save()
        return redirect('/unit?Prop_id='+str(prop_id))
    units = Unit.objects.filter(property=data.id)
    return render(request, "main/unit.html", {'property': data, 'units':units})

def delete_unit(request):
    unit_id = request.GET.get('Unit_id')
    prop_id = request.GET.get('Prop_id')
    property = Property.objects.get(id=prop_id)
    
    Unit.objects.get(id=unit_id).delete()
    return redirect('/unit?Prop_id='+str(property.id))

def update_unit(request):
    prop_id = request.GET.get('Prop_id')
    unit_id = request.GET.get('Unit_id')
    data = Unit.objects.get(id=unit_id)
    if request.method == 'POST':
        data.rent_cost = request.POST.get('rent_cost')
        data.type = request.POST.get('type')
        
        data.save(update_fields=['rent_cost','type'])
        return redirect('/unit?Prop_id='+str(prop_id))
    return render(request,"main/unit_update.html",{'data':data, 'choice':['1BHK', '2BHK', '3BHK', '4BHK']})

def tenant(request):
    search_query = request.GET.get('search')
    datas = Tenant.objects.all()

    if search_query:
        datas = datas.filter(
            Q(name__icontains=search_query) |
            Q(tenantagreement__property__name__icontains=search_query) |
            Q(tenantagreement__unit__type__icontains=search_query) |
            Q(tenantagreement__unit__rent_cost__icontains=search_query)
        )

        tenant_data = []
        for tenant in datas:
            tenant_info = {
                'tenant': tenant,
                'agreements': TenantAgreement.objects.filter(tenant=tenant)
            }
            tenant_data.append(tenant_info)

        return render(request, "main/tenant.html", {"datas": tenant_data})
    if request.method == 'POST':
        obj = Tenant()
        obj.name = request.POST.get('name')
        obj.address = request.POST.get('address')
        obj.document_proofs = request.POST.get('document_proofs')

        obj.save()
        return redirect('/tenant')
    datas = Tenant.objects.all()
    tenant_data = []
    for tenant in datas:
        tenant_info = {
            'tenant': tenant,
            'agreements': TenantAgreement.objects.filter(tenant=tenant)  # Fetch units assigned to the tenant
        }
        tenant_data.append(tenant_info)
    return render(request,"main/tenant.html",{"datas":tenant_data,})

def delete_tenant(request):
    tenant_id = request.GET.get('Tenant_id')
    Tenant.objects.get(id=tenant_id).delete()
    return redirect('/tenant?Tenant_id='+str(tenant_id))

def update_tenant(request):
    tenant_id = request.GET.get('Tenant_id')
    obj = Tenant.objects.get(id=tenant_id)
    if request.method == 'POST':
        obj.name = request.POST.get('name')
        obj.address = request.POST.get('address')
        obj.document_proofs = request.POST.get('document_proofs')
        
        obj.save(update_fields=['name','address','document_proofs'])
        return redirect('/tenant?Tenant_id='+str(tenant_id))
    return render(request,"main/tenant_update.html",{'data':obj})

def tenant_profile(request):
    tenant_id = request.GET.get('Tenant_id')
    Tenant_data = Tenant.objects.get(id=tenant_id)
    Agreement_data = TenantAgreement.objects.filter(tenant=Tenant_data)
    return render(request,'main/tenant_profile.html',{'tenant':Tenant_data,'rental_info':Agreement_data})

def agreement(request):
    tenant_id = request.GET.get('Tenant_id')
    properties = Property.objects.all()
    if request.method == 'POST':
        agreement = TenantAgreement()
        agreement.tenant = Tenant.objects.get(id=tenant_id)
        agreement.property = Property.objects.get(id=request.POST.get('property'))
        agreement.unit = Unit.objects.get(id=request.POST.get('unit'))
        agreement.agreement_end_date = request.POST.get('agreement_end_date')
        agreement.monthly_rent_date = request.POST.get('monthly_rent_date')
        agreement.save()
        return redirect('/agreement?Tenant_id='+str(tenant_id))
    datas = TenantAgreement.objects.filter(tenant=Tenant.objects.get(id=tenant_id))
    return render(request,'main/agreement.html', {'tenant_id': tenant_id, 'properties':properties,'datas':datas})

def get_units(request, property_id):
    units = Unit.objects.filter(property_id=property_id)
    unit_data = [{'id': unit.id, 'type': unit.type} for unit in units]
    return JsonResponse(unit_data, safe=False)

def delete_agreement(request):
    agreement_id = request.GET.get('Agreement_id')
    tenant_id = request.GET.get('Tenant_id')
    TenantAgreement.objects.get(id=agreement_id).delete()
    return redirect('/agreement?Tenant_id='+str(tenant_id))

