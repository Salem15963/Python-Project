from django.shortcuts import render ,redirect
from .models import  Doctor , Clinic , Patient   ,Appointment   , Payment
from django.contrib import messages
import re
from datetime import datetime, date
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')




def root (request):
    return render(request,'welcome.html')


def signin(request):
    return render(request,'login.html')

def registration(request):
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        phone=request.POST['phone']
        national_id=request.POST['national_id']
        desc=request.POST['desc']
        role=request.POST['role']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
        new_user=Doctor.objects.create(first_name=first_name,last_name=last_name,email=email,password=pw_hash,phone=phone,national_id=national_id,desc=desc,role=role)
        request.session['first_name'] = new_user.first_name
        request.session['last_name'] = new_user.last_name
        request.session['id'] = new_user.id
        return redirect('/')

def login(request):
    logged_user= Doctor.objects.filter(email=request.POST['email'])
    if logged_user:
        logged_user=logged_user[0]
    request.session['first_name']=logged_user.first_name
    request.session['id']=logged_user.id
    request.session['last_name']=logged_user.last_name
    request.session['role']=logged_user.role
    return redirect('/account')

def home(request):
    context={
            'user':Doctor.objects.all(),
        }   
    return render(request,'home.html',context)

def logout(request):
    request.session.delete()
    return redirect('/')


def patients(request):
    context={
            'patients':Patient.objects.all(),
            'clinic':Clinic.objects.all(),
        }   
    return render(request,'all_patients.html',context)

def patient(request):
    return(request,'patient.html')

def admin_dash(request):
    return render(request,'registration.html')



    request.session['first_name']=logged_user.first_name
    request.session['id']=logged_user.id
    request.session['last_name']=logged_user.last_name
    request.session['role']=logged_user.role
    request.session['phone']=logged_user.phone
    request.session['clinic']=logged_user.clinic
    request.session['date_of_bith']=logged_user.date_of_bith

def account(request):

    return render(request, 'main_account.html')



def Clinic_validation(request):
    check = Clinic.objects.filter(name = request.POST['name'])
    error = False

    if len(request.POST['name'])< 3:
        messages.error(request,'The clinic name must contain more than two charecters', extra_tags = 'clinic_name' )
        error = True

    if not NAME_REGEX.match(request.POST['name']):
        messages.error(request,'The linic name must contain only alpha characters', extra_tags = 'clinic_name')
        error = True

    if len(request.POST['address'])< 9:
        messages.error(request,'The clinic address must be more than 8 cherecters', extra_tags = 'clinic_address')
        error = True

    if error == True:
        return redirect('/')

    elif error == False:
        Clinic.objects.create(name = request.POST['name'], address = request.POST['adddress'])

        messages.success(request, 'You have a new clinic !!', extra_tags = 'clinic_s')
        
        return redirect('/')
# ______________________________________________________
def patient_validate(request):
    # check = Patient.objects.get(national_id = request.POST['national_id'])
    check = True
    error = False


    if len(request.POST['first_name'])< 3:
        messages.error(request,'First Name must at laest contain two characters!', extra_tags = 'fn_error' )
        error = True

    if not NAME_REGEX.match(request.POST['first_name']):
        messages.error(request,'first name field must  contain Alpha characters', extra_tags = 'fn_error')
        error = True

    if not NAME_REGEX.match(request.POST['last_name']):
        messages.error(request,'Last name field must  contain Alpha characters', extra_tags = 'ln_error')
        error = True

    if len(request.POST['last_name'])< 3:
        messages.error(request,'Last Name must be at least contain two characters', extra_tags = 'ln_error')
        error = True
    if len(request.POST['national_id'])!=9:
        messages.error(request,'The national id must be 9 digites!!',extra_tags='national_id')
        error=True
    if (request.POST['gender'])!='female' or (request.POST['gender'])!='male':
         messages.error(request,'The gender must be only mail or femail',extra_tags='gender')
         error=True
    if len(request.POST['phone'])!=10:
         messages.error(request,'The phone must be only 10 digites',extra_tags='phone')
         error=True   
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request,'email format must matches the email patterns ', extra_tags = 'email_error')
        error = True
    if len(request.POST['desc'])<1:
         messages.error(request,'plese enter any description  ', extra_tags = 'desc')
         error=True
    if request.POST['birth_date'] > str(datetime.now()):
        messages.error(request,"Birth date must be in the past!",  extra_tags = 'birth_error')
        error=True
        
    
    if check:
        messages.error(request,'Pationt with this national_id has already been registered', extra_tags = 'national_id')
        error = True

    if error == True:

        return redirect('/account')

    elif error == False:

        Patient.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'],
                                national_id = request.POST['national_id'], email = request.POST['email'], phone = request.POST['phone'], desc = request.POST['desc'], date_of_birth = request.POST['date_of_birth']
                                ,clinic = Clinic.objects.get(name = request.POST['clinic']))

        messages.success(request, 'You have added anew pationt  succesfully ,Thank you and welcome to this our web', extra_tags = 'added')
        
        return redirect('/account')
# ______________________________________________________________________________
def appointment_validate(request):
    # check = Patient.objects.filter(national_id = request.POST['national_id'])
    error = False
    if len(request.POST['national_id']) != 9 :
        messages.error(request,'Please enter a valid national id', extra_tags = 'national_id' )
        error = True

    if len(request.POST['start_time'])< 1:
        messages.error(request,'Please enter a start date', extra_tags = 'start_time' )
        error = True

    if len(request.POST['end_time'])< 1:
        messages.error(request,'Please enter a end date', extra_tags = 'end_time' )
        error = True
    
    # if len(request.POST['title'])==0:
    #     messages.error(request,'Please Enter the title  for this appointment',extra_tags='appointment_title')
    #     error=True
    
    # if check:
    #     messages.error(request,'Pationt with this national_id has already been registered', extra_tags = 'national_id')
    #     error = True

    if error == True:
        return redirect('/account')

    elif error == False:
        patient = Patient.objects.get(national_id = request.POST['national_id'])
        Appointment.objects.create(start_time = request.POST['start_time'], end_time = request.POST['end_time'], patient_appoint = patient, doctor_appoint = Doctor.objects.get(id = request.session['id']))

        messages.success(request, 'You have added anew appointment  succesfully ,Thank you and welcome to this our web', extra_tags = 'added')
        
        return redirect('/account')
# _____________________________________________________________________________

def payment_validate(request):
    # check = Patient.objects.filter(national_id = request.POST['national_id'])
    error = False

    if len(request.POST['amount'])<1:
        messages.error(request,'Please enter a required amount of money', extra_tags = 'payment_amount' )
        error = True

    if len(request.POST['date'])< 1:
        messages.error(request,'Please enter a the  date', extra_tags = 'payment_date' )
        error = True
    
    if len(request.POST['method'])==0:
        messages.error(request,'Please Enter a correct methodes -enter -C- for credit or -M- for cash',extra_tags='payment_method')
        error=True
    
    if error == True:
        return redirect('/')

    elif error == False:

        Payment.objects.create()

        messages.success(request, 'You have added anew payment succesfully ,Thank you and welcome to this our web', extra_tags = 'added')
        
        return redirect('/')