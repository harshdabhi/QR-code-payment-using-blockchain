from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from payment_repo.pay import payments
import os


# Create your views here. 


def homepage(request):
    global qr_code_file_name,m_wallet_name
    if request.method=='POST':
        payment_mode=request.POST.get('payment')
        amount=int(request.POST.get('amount'))
        m_wallet=request.POST.get('m_wallet')
 
        p_=payments()
        link=p_.merchant_inputs(amount,m_wallet,payment_mode)
        qr_code_file,qr_time=p_.generate_qr_code(link)
        qr_code_file_name=qr_code_file




 

        
        context={
            'qr_code_img':'./static/'+qr_code_file,
            'time':qr_time,
            'm_wallet':m_wallet,
        }
        return render(request,'qr_code.html',context)
    else:
        return render(request,'homepage.html')
        


    #return render(request,'homepage.html')

def qr_code(request):
    return render(request,'qr_code.html')



from django.http import JsonResponse

def start_autopayment(request):
    if request.method == 'POST':
        m_wallet = request.POST.get('m_wallet')
        p_ = payments()

        
        temp = p_.auto_payment(m_wallet)
        if temp != []:
            status = 'success'
        
        else:
            status = 'pending'

            
        return JsonResponse({'status': status})  # Return a JsonResponse with the status

    return JsonResponse({'status': 'error'})  # Return a default status if the request method is not POST


def error_page(request):
    return render(request,'error_page.html')  

def success_page(request):
    os.remove('./static/'+qr_code_file_name)
    return render(request,'success_page.html')  