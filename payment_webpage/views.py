from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from payment_repo.pay import payments
import os
from config_it import MONGODB_CRED_DB,MONGODB_COLL
from config_it.config_keys import config_value


# Create your views here. 


def homepage(request):
    global qr_code_file_name,m_wallet_name,url
    if request.method=='POST':
        payment_mode=request.POST.get('payment')
        amount=int(request.POST.get('amount'))
        m_wallet=request.POST.get('m_wallet')
        chain=request.POST.get('chain')


        # c=config_value()
        # keys=c.value_retrieve(MONGODB_CRED_DB,MONGODB_COLL,{'name':chain})
        # url=keys['api']
        # print(url)
        
    
        p_=payments()
        link=p_.merchant_inputs(amount,m_wallet,payment_mode)
        qr_code_file,qr_time=p_.generate_qr_code(link)
        qr_code_file_name=qr_code_file

        interval_dict={
            'eth':10000, #10 sec
            'trx':0
        }  

        interval=interval_dict[chain]
        if chain=='eth':
            c=config_value()
            keys=c.value_retrieve(MONGODB_CRED_DB,MONGODB_COLL,{'name':chain})
            url=keys['api']
            print(url)
            context={
                'qr_code_img':'./static/'+qr_code_file,
                'time':qr_time,
                'm_wallet':m_wallet,
                'url':url,
                'chain':chain,
                'interval':interval
            }
            return render(request,'qr_code.html',context)
        
        elif chain=='trx':
            context={
                'qr_code_img':'./static/'+qr_code_file,
                'time':qr_time,
                'm_wallet':m_wallet,
                'chain':chain,
                'interval':interval
            }
            return render(request,'qr_code_trx.html',context)
            
    else:
        return render(request,'homepage.html')
        


    #return render(request,'homepage.html')

def qr_code(request):
    return render(request,'qr_code.html')

def qr_code_trx(request):
    return render(request,'qr_code_trx.html')



from django.http import JsonResponse

def start_autopayment(request):

    if request.method == 'POST':
        m_wallet = request.POST.get('m_wallet')
        url = request.POST.get('url')
        p_ = payments()

        
        temp = p_.auto_payment(m_wallet,url)
        if temp != []:
            status = 'success'
        
        else:
            status = 'pending'

            
        return JsonResponse({'status': status})  # Return a JsonResponse with the status

    return JsonResponse({'status': 'error'})  # Return a default status if the request method is not POST


def start_autopayment_trx(request):
    global temp

    if request.method == 'POST':
        m_wallet = request.POST.get('m_wallet')
        
        p_ = payments()
        temp = p_.auto_payment_trx(m_wallet)
        if temp != []:
            
            status = 'success'
        
        else:
            status = 'pending'

             
        return JsonResponse({'status': status})  # Return a JsonResponse with the status

    return JsonResponse({'status': 'error'}) 


def error_page(request):
    return render(request,'error_page.html')  

def success_page(request):
    os.remove('./static/'+qr_code_file_name) 
    return render(request,'success_page.html',{'temp':temp})  