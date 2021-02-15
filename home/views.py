from django.shortcuts import render,HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
##########################Pyrebase####################################
import pyrebase
config = {
    "apiKey": "AIzaSyAXwgisDN7kx6BMZCIwYjj8KNDgmJuz1Mg",
    "authDomain": "exampledjango-4af38.firebaseapp.com",
    "databaseURL": "https://exampledjango-4af38.firebaseio.com",
    "storageBucket": "exampledjango-4af38.appspot.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database() ##database reference
authe = firebase.auth()   ##authentication reference
#######################################################################
# Create your views here.
def texts_page(request):
    if request.session.is_empty() == False: 
        try : 
            msgs1 = db.child("messages").child(request.session["uid"]).shallow().get()  
        except:
            pass
        onlineUsers = db.child("onlineUsers").shallow().get()
        # print(msgs1)
        if msgs1.val() is None : 
            context = {
                "names" : None,
                "user_name" : request.session["fName"]
            }
            return render(request,"texts_page.html", context)
        # print(onlineUsers.val())
        # print('3' in onlineUsers.val())
        # msgs2 = db.child("messages").child("2").child("1").get()
        # print(type(msgs))
        # print(msgs1.val())
        messages1 = list(msgs1.val())
        names = []
        for userid in messages1:
            eachName = db.child("userId").child(userid).get()

            if userid in onlineUsers.val():
                names.append([eachName.val()["fName"], userid, "online"])
            else:
                print(eachName.val())
                names.append([eachName.val()["fName"], userid, "offline"])



        context = {}
        # context["messages"] = messages?
        context["names"] = names
        context["uid"] = request.session["uid"]
        context["user_name"] = request.session["fName"]
        # print(type(tempMsg))
        # print(messages)
        return render(request,"texts_page.html", context)
    else:
        return landing_page_with_context(request, {'first_login' : True})

def interests_page(request):
    if request.session.is_empty() == False:
        interest_shown_response = db.child("interests_shown").child(request.session["uid"]).get() 
        interest_received_response = db.child("interests_received").child(request.session["uid"]).get() 
        #interest_shown_keys_response=db.child("interests_shown").child(request.session["uid"]).shallow().get()
        #interest_received_keys_response=db.child("interests_received").child(request.session["uid"]).shallow().get() 
        
        interest_shown=interest_shown_response.val()
        interest_received=interest_received_response.val()

        #print(interest_shown)
        #print(interest_received)

        if interest_shown:
            for i in interest_shown.keys():
                if interest_shown[i][3]==0:
                    product_details=db.child("sell").child(interest_shown[i][2]).child(interest_shown[i][1]).get()
                    interest_shown[i][3]="Seller :"
                else:
                    product_details=db.child("lease").child(interest_shown[i][2]).child(interest_shown[i][1]).get()
                    interest_shown[i][3]="Lessor :"
                interest_shown[i].append(i)
                print(product_details.val())
                interest_shown[i]=interest_shown[i]+product_details.val()
            interest_shown=list(interest_shown.values())
        else:
            interest_shown=None
        
        if interest_received:
            for i in interest_received.keys():
                if interest_received[i][3]==0:
                    product_details=db.child("sell").child(request.session["uid"]).child(interest_received[i][1]).get()
                    interest_received[i][3]="Seller :"
                else:
                    product_details=db.child("lease").child(request.session["uid"]).child(interest_received[i][1]).get()
                    interest_received[i][3]="Lessor :"
                product_details=product_details.val()
                interest_received[i].append(i)
                shower_name=db.child("userId").child(interest_received[i][2]).get()
                shower_full_name=shower_name.val()["fName"]+" "+shower_name.val()["lName"]
                product_details.append(shower_full_name)
                interest_received[i]=interest_received[i]+product_details
            interest_received=list(interest_received.values())
        else:
            interest_received=None
            
        context={}
        context["interest_shown"]=interest_shown
        context["interest_received"]=interest_received
        context["uid"]=request.session["uid"]
        context["user_name"]=request.session["fName"]
        print(context)
        return render(request,'interests_page.html',context)
    else:
        return landing_page_with_context(request, {'first_login' : True})

def confirmations_page(request):
    if request.session.is_empty() == False:
        confirmations_shipped_response = db.child("confirmations_shipped").child(request.session["uid"]).get() 
        confirmations_received_response = db.child("confirmations_received").child(request.session["uid"]).get() 
        
        confirmations_shipped=confirmations_shipped_response.val()
        confirmations_received=confirmations_received_response.val()

        print(confirmations_shipped)
        print(confirmations_received)

        if confirmations_shipped:
            for i in confirmations_shipped.keys():
                if confirmations_shipped[i][3]==0:
                    product_details=db.child("sell").child(request.session["uid"]).child(confirmations_shipped[i][1]).get()
                    confirmations_shipped[i][3]="Seller :"
                else:
                    product_details=db.child("lease").child(request.session["uid"]).child(confirmations_shipped[i][1]).get()
                    confirmations_shipped[i][3]="Lessor :"
                product_details=product_details.val()
                print("asdsa2",confirmations_shipped[i][2])
                print("asdsa1", confirmations_shipped[i][1])
                print(product_details)
                confirmations_shipped[i].append(i)
                buyer_name=db.child("userId").child(confirmations_shipped[i][2]).get()
                buyer_full_name=buyer_name.val()["fName"]+" "+buyer_name.val()["lName"]
                product_details.append(buyer_full_name)
                confirmations_shipped[i]=confirmations_shipped[i]+product_details
            confirmations_shipped=list(confirmations_shipped.values())
        else:
            confirmations_shipped=None
        print(confirmations_shipped)

        if confirmations_received:
            for i in confirmations_received.keys():
                if confirmations_received[i][3]==0:
                    product_details=db.child("sell").child(confirmations_received[i][2]).child(confirmations_received[i][1]).get()
                    confirmations_received[i][3]="Seller :"
                else:
                    product_details=db.child("lease").child(confirmations_received[i][2]).child(confirmations_received[i][1]).get()
                    confirmations_received[i][3]="Lessor :"
                confirmations_received[i].append(i)
                confirmations_received[i]=confirmations_received[i]+product_details.val()
            confirmations_received=list(confirmations_received.values())
        else:
            confirmations_received=None
        print(confirmations_received)
        context={}
        context["confirmations_shipped"]=confirmations_shipped
        context["confirmations_received"]=confirmations_received
        context["uid"]=request.session["uid"]
        context["user_name"]=request.session["fName"]
        print(context)
        return render(request,'confirmations_page.html',context)
    else:
        return landing_page_with_context(request, {'first_login' : True})

def buy_page(request):
    if request.session.is_empty() == False:
        if request.method == 'GET' and request.GET.get('text')!=None:
            search_text=request.GET.get('text').lower()
            print (search_text)
            list_of_items=db.child("titles").order_by_key().equal_to(search_text).get().val()
            if list_of_items:
                list_of_items=list_of_items[search_text]
                item_list=list(list_of_items.values())
                keys_list=list(list_of_items.keys())
                print(item_list)
                print(keys_list)
            else:
                item_list=None
            
            list_to_show=[]
            j=0
            if item_list:
                for i in item_list:
                    intermediate_list=db.child("sell").child(i[0]).child(i[1]).get().val()
                    intermediate_list.append(i[0])
                    intermediate_list.append(i[1])
                    intermediate_list.append(keys_list[j])
                    j+=1
                    list_to_show.append(intermediate_list)
            else:
                list_to_show=None;
            print(list_to_show)
            context={}
            context["list_to_show"]=list_to_show
            context["searched_item"]=request.GET.get('text')
            context["user_name"]=request.session["fName"]
            context["uid"]=request.session["uid"]
            context["show_happy"]=0
            return render(request,'buy_page.html',context)
        else:
            context={}
            context["user_name"]=request.session["fName"]
            context["show_happy"]=1
            return render(request,'buy_page.html',context)
    else:
        return landing_page_with_context(request, {'first_login' : True})

def sell_page(request):
    if request.session.is_empty() == False :
        items_response=db.child("sell").child(request.session["uid"]).get()
        items_response_keys = db.child("sell").child(request.session["uid"]).shallow().get()
        items_keys = items_response_keys.val()
        items=items_response.val()
        if items:
            final_list = []
            # items_list=list(items.values())
            for i in items.keys():
                if items[i][5] == 0:
                    items[i].append(i)
                    final_list.append(items[i])
            # print(type(final_list))
        else:
            final_list=None
            
        full_name=request.session["fName"]+" "+request.session["lName"]
        context={}
        context["items"]=final_list
        context["user_name"]=request.session["fName"]
        context["uid"]=request.session["uid"]
        context["full_name"]=full_name
        return render(request,'sell_page.html',context)
    else:
        return landing_page_with_context(request, {'first_login' : True})

def rent_page(request):
    if request.session.is_empty() == False :
        if request.method == 'GET' and request.GET.get('text')!=None:
            search_text=request.GET.get('text').lower()
            print (search_text)
            list_of_items=db.child("lease_titles").order_by_key().equal_to(search_text).get().val()
            if list_of_items:
                list_of_items=list_of_items[search_text]
                item_list=list(list_of_items.values())
                keys_list=list(list_of_items.keys())
                # print(item_list)
                # print(keys_list)
            else:
                item_list=None
            
            list_to_show=[]
            j=0
            if item_list:
                for i in item_list:
                    intermediate_list=db.child("lease").child(i[0]).child(i[1]).get().val()
                    intermediate_list.append(i[0])
                    intermediate_list.append(i[1])
                    intermediate_list.append(keys_list[j])
                    j+=1
                    list_to_show.append(intermediate_list)
            else:
                list_to_show=None;
            print(list_to_show)
            context={}
            context["show_happy"]=0
            context["list_to_show"]=list_to_show
            context["searched_item"]=request.GET.get('text')
            context["user_name"]=request.session["fName"]
            context["uid"]=request.session["uid"]
            return render(request,'rent_page.html',context)
        else:
            context={}
            context["show_happy"]=1
            context["user_name"]=request.session["fName"]
            return render(request,'rent_page.html',context)
    else:
        return landing_page_with_context(request, {'first_login' : True})

def lease_page(request):
    if request.session.is_empty() == False :
        items_response=db.child("lease").child(request.session["uid"]).get()
        items_response_keys = db.child("lease").child(request.session["uid"]).shallow().get()
        items = items_response.val()
        items_keys = items_response_keys.val() 
        if items:
            final_list = []
            # items_list=list(items.values())
            for i in items.keys():
                if items[i][5] == 0:
                    items[i].append(i)
                    final_list.append(items[i])
        else:
            final_list=None
        full_name=request.session["fName"]+" "+request.session["lName"]
        context={}
        context["items"]=final_list
        context["user_name"]=request.session["fName"]
        context["uid"]=request.session["uid"]
        context["full_name"]=full_name
        return render(request,'lease_page.html',context)
    else:
        return landing_page_with_context(request, {'first_login' : True})

def render_service_page(request):
    if request.session.is_empty() == False :
        return render(request,'render_service_page.html')
    else:
        return landing_page_with_context(request, {'first_login' : True})

def require_service_page(request):
    if request.session.is_empty() == False :
        return render(request,'require_service_page.html')
    else:
        return landing_page_with_context(request, {'first_login' : True})

def account_details_page(request):
    if request.session.is_empty() == False :
        context = {
            "fullName" : request.session["fName"] + " "+request.session["lName"],
            "eMail" : request.session["email"],
            "user_name":request.session["fName"]
        }
        return render(request,'account_details_page.html', context)
    else:
        return landing_page_with_context(request, {'first_login' : True})

def all_transactions_page(request):
    if request.session.is_empty() == False :
        transaction_details_response = db.child("all_transactions").child(request.session["uid"]).get()
        transaction_details = transaction_details_response.val()
        print(transaction_details)
        context = {}
        iem_details = []
        if transaction_details:
            for i in transaction_details.keys():
                if(transaction_details[i][3] == 1 or transaction_details[i][3] == 2):
                    if(transaction_details[i][3] == 2):
                        item_details = db.child("sell").child(request.session["uid"]).child(transaction_details[i][1]).get().val()
                    elif(transaction_details[i][3] == 1):
                        item_details = db.child("sell").child(transaction_details[i][2]).child(transaction_details[i][1]).get().val()
                    # print(item_details)
                    transaction_details[i].append(item_details[0])
                    transaction_details[i].append(item_details[1])
                    transaction_details[i].append(item_details[3])
                    transaction_details[i].append(item_details[4])
                elif(transaction_details[i][3] == 3 or transaction_details[i][3] == 4):
                    if(transaction_details[i][3] == 3):
                        item_details = db.child("lease").child(transaction_details[i][2]).child(transaction_details[i][1]).get().val()
                    elif(transaction_details[i][3] == 4):
                        item_details = db.child("lease").child(request.session["uid"]).child(transaction_details[i][1]).get().val()
                    transaction_details[i].append(item_details[0])
                    transaction_details[i].append(item_details[1])
                    transaction_details[i].append(item_details[3])
                    transaction_details[i].append(item_details[4])
                to_from_name=db.child("userId").child(transaction_details[i][2]).get()
                fullName=to_from_name.val()["fName"]+" "+to_from_name.val()["lName"]
                transaction_details[i][2] = fullName
            transaction_details_list = list(transaction_details.values())
        else:
            transaction_details_list = None

        print(transaction_details_list)
        context["transaction_details_list"] = transaction_details_list
        context["user_name"]=request.session["fName"]
        # print(transaction_details_list)
        return render(request,'all_transactions_page.html', context)
    else:
        return landing_page_with_context(request, {'first_login' : True})

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def landing_page_with_context(request, context):
        return render(request, 'landing_page.html', context)

def landing_page_register(request):
    return render(request, "landing_page_register.html")


def landing_page(request):
    if request.session.is_empty()==False:
        images=db.child("images").get()
        images=images.val()
        images=list(images.values())
        images=images[::-1]
        if len(images)>9:
            images=images[:9]
        print(images)
        context={}
        context["user_name"]=request.session["fName"]
        context["images"]=images
        return home_page_with_context(request,context)
    if request.method == 'POST':  ## registering a user
        fName = request.POST.get("fName")
        lName = request.POST.get("lName")
        email = request.POST.get("email")
        password = request.POST.get("password")
        conPass = request.POST.get("conPass")

        users = db.child("users").get()
        
        try:
            # print("absydvsa")
            user = authe.create_user_with_email_and_password(email, password)
            # print(user)
            
            authe.send_email_verification(user['idToken'])

            # print(users)
            count = len(users.val()) + 1

            data = {
                "userId": count
            }
            tempEmail = ""  ## generating mail for firebase DB
            for i in email :
                if i == '@':
                    break
                if i == '.':
                    tempEmail += '@'
                    continue
                tempEmail += i

            # print(tempEmail)

            db.child("users").child(tempEmail).set(data)
            data = {
                "fName": fName,
                "lName": lName,
            }
            db.child("userId").child(count).set(data)
            context = {
                "not_verified_email" : False,
                'bad_login' : False,
                "POST_request" : True,
                "forgot_password" : False,
                "incorrect_email" : False,
                "Email_already_registered" : False,
                "logged_out" : False,
                "first_login" : False
            }
            return render(request, 'landing_page.html', context)

        except:
            context = {
                "not_verified_email" : False,
                'bad_login' : False,
                "POST_request" : False,
                "forgot_password" : False,
                "incorrect_email" : False,
                "Email_already_registered" : True,
                "logged_out" : False,
                "first_login" : False
            }
            return landing_page_with_context(request, context)
    
    context = {
            "not_verified_email" : False,
            'bad_login' : False,
            "POST_request" : False,
            "forgot_password" : False,
            "incorrect_email" : False,
            "Email_already_registered" : False,
            "logged_out" : False,
            "first_login" : False
        }
    return render(request,'landing_page.html', context)

def home_page(request):    
    if request.session.is_empty() == False:
        images=db.child("images").get()
        images=images.val()
        images=list(images.values())
        images=images[::-1]
        if len(images)>9:
            images=images[:9]
        print(images)
        context={}
        context["user_name"]=request.session["fName"]
        context["images"]=images
        return render(request,'home_page.html',context)
    else:
        return landing_page_with_context(request, {'first_login' : True})

def home_page_with_context(request, context):
    if request.session.is_empty() == False:
        images=db.child("images").get()
        images=images.val()
        images=list(images.values())
        images=images[::-1]
        if len(images)>9:
            images=images[:9]
        print(images)
        context={}
        context["user_name"]=request.session["fName"]
        context["images"]=images
        return render(request, 'home_page.html', context)
    else:
        return landing_page_with_context(request, {'first_login' : True})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get("forgot_pass_email")
        try : 
            authe.send_password_reset_email(email)
            context = {
                        "not_verified_email" : False,
                        'bad_login' : False,
                        "POST_request" : False,
                        "forgot_password" : True,
                        "incorrect_email" : False,
                        "Email_already_registered" : False,
                        "logged_out" : False,
                        "first_login" : False
                    }
            return landing_page_with_context(request, context)
        except:
            context = {
                        "not_verified_email" : False,
                        'bad_login' : False,
                        "POST_request" : False,
                        "forgot_password" : False,
                        "incorrect_email" : True,
                        "Email_already_registered" : False,
                        "logged_out" : False,
                        "first_login" : False
                    }
            return landing_page_with_context(request, context)

def logout(request):
    db.child("onlineUsers").child(request.session["uid"]).remove()
    request.session.flush()

    context = {
        "not_verified_email" : False,
        'bad_login' : False,
        "POST_request" : False,
        "forgot_password" : False,
        "incorrect_email" : False,
        "Email_already_registered" : False,
        "logged_out" : True,
        "first_login" : False
    }
    return landing_page_with_context(request, context)

def login(request):
    if request.method == 'POST':  ## signing in user
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = authe.sign_in_with_email_and_password(email, password)
            userInfo = authe.get_account_info(user['idToken'])

            # print(userInfo["users"][0]["emailVerified"])

            if userInfo["users"][0]["emailVerified"] == False : 
                context = {
                    "not_verified_email" : True,
                    "bad_login" : False,
                    "POST_request": False,
                    "forgot_password" : False,
                    "incorrect_email" : False,
                    "Email_already_registered" : False,
                    "logged_out" : False,
                    "first_login" : False
                }
                return landing_page_with_context(request, context)
                
            if userInfo["users"][0]["emailVerified"] == True:
                # print(user)
                tempEmail = ""
                for i in email :
                    if i == '@':
                        break
                    if i == '.':
                        tempEmail += '@'
                        continue
                    tempEmail += i
                userDB = db.child("users").child(tempEmail).get()
                # print(userD)
                
                
                ################# SESSION SETTINGS ############
                request.session["uid"] = userDB.val()["userId"]
                userIdDB = db.child("userId").child(request.session["uid"]).get()
                user["displayName"] = userIdDB.val()["fName"]
                request.session["email"] = email
                request.session["fName"] = userIdDB.val()["fName"]
                request.session["lName"] = userIdDB.val()["lName"]
                # request.session["tempEmail"] = tempEmail
                ################################################
                
                data = {
                    "active" : True,
                    "userid" : request.session["uid"]
                }
                db.child("onlineUsers").child(request.session["uid"]).set(data)

                context = {
                    'user_name': user["displayName"],
                    "uid" : request.session["uid"],
                    "fName" : request.session["fName"],
                    "lName" : request.session["lName"],
                }
                return home_page_with_context(request, context)
                
        except: ## Wrong Credentials
            context = {
                "not_verified_email" : False,
                'bad_login' : True,
                "POST_request" : False,
                "forgot_password" : False,
                "incorrect_email" : False,
                "Email_already_registered" : False,
                "logged_out" : False,
                "first_login" : False
            }
            return landing_page_with_context(request, context)

def contributors(request):
    if request.session.is_empty() == False:
        return render(request,"contributors.html")
    else:
        return landing_page_with_context(request, {'first_login' : True})
def ad_page(request):
    if request.session.is_empty() == False:
        context={}
        context["user_name"] = request.session["fName"]
        return render(request,"ad_page.html", context)   
    else:
        return landing_page_with_context(request, {'first_login' : True})


