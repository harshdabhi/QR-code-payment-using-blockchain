from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from payment_repo.pay import payments
import os
from config_it import MONGODB_CRED_DB,MONGODB_COLL,MONGODB_CRED_CUST,MONGODB_CUST_LOG
from config_it.config_keys import config_value
from django.http import JsonResponse


# Create your views here. 
# def login_required(view_func):
#     def wrapper(request, *args, **kwargs):
#         # Check if the user is authenticated
#         if not request.session.get('authenticated'):
#             return render(request,'pages_login.html',{'message':'Invalid user'}) 

#         return view_func(request, *args, **kwargs)
#     return wrapper


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


def start_autopayment(request):
    global temp

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
            print(temp)
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

def pages_login(request):
    
   
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        c_=config_value()
        keys=c_.value_retrieve(MONGODB_CRED_CUST,MONGODB_CUST_LOG,{'username':username})
        
        
        try:
            password_check=keys['password'] 
            if password_check==password: 
                request.session['authenticated'] = True
                 
                return render(request,'homepage.html')
            
        except Exception as e:
            
            return render(request, 'pages_login.html',{'message':'Invalid user'})
        
    
    return render(request, 'pages_login.html') 



def pages_register(request):
    c_=config_value()
    keys=c_.value_retrieve(MONGODB_CRED_CUST,'registration',{'name':'status'})
    if keys['enabled']=='no':
        return redirect('/pages-error-404')
    
    else:


        try:

            if request.method == 'POST':
                name = request.POST.get('name')
                email = request.POST.get('email')
                username = request.POST.get('username')
                password = request.POST.get('password')

                dict_inputs={
                    'name':name,
                    'email':email,
                    'username':username,
                    'password':password
                }
    
                

                d=config_value()

                d.value_input(MONGODB_CRED_CUST,MONGODB_CUST_LOG,dict_inputs)
                return redirect('/pages_login')
            
            else:
                return render(request,'pages_register.html')
                
        except Exception as e:
            print(e)
    

def pages_error(request):
    return render(request,'pages-error-404.html')
