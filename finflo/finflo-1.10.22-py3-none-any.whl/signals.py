from django import dispatch
from django.db.models.signals import post_save , pre_save , post_delete
from .exception import DefaultsNotFoundError
from .middleware import get_current_user
from .models import (
    PartyType,
    States,
    TransitionManager,
    workevents,
    workflowitems 
)
from django.conf import settings
from .transition import FinFlotransition
from .compatability import check_version_compatibility



# MAIN SIGNAL RECEIVER FOR TRANSITION HANDLING - 4/8/2022 by anand

Base_link = 'https://pypi.org/project/finflo/'


# CORE LIST ITERATED FROM THE DEFAULT SETTINGS -- PRODUCTION : 27/10/2022
try:
    check_version_compatibility()
    b = [ite for ite in settings.FINFLO['PARTY_MODEL']] 
    a = [ite for ite in settings.FINFLO['WORK_MODEL']]
except:
    raise DefaultsNotFoundError ("unable to find WORK_MODEL and PARTY_MODEL in your settings.py file , \
        check the documentation for more details",Base_link)




# CUSTOM MULTIPLE RECEIVER SIGNALS 

def finflo_receiver(signal, senders ,  **kwargs):
    def decorator(receiver_func):
        for sender in senders:
            if isinstance(signal, (list, tuple)):
                for s in signal:
                    s.connect(receiver_func, sender=sender, **kwargs)
            else:
                signal.connect(receiver_func, sender=sender,**kwargs)

        return receiver_func

    return decorator




# MULTIPLE RECEIVER MODEL WITH MULTIPLE SENDERS

#### CREATER

## A
@finflo_receiver(post_save, senders = a)
def create(sender, instance, created , **kwargs):
    a = str(sender)
    remove_characters = ["class", "models.","'","<",">"," "]
    if created:
        for i in remove_characters:
            a = a.replace(i,"")
            states = States.objects.get(id = 1)
        obj = TransitionManager.objects.create(type = a.lower() , t_id = instance.id)
        gets_transition = FinFlotransition(t_id = obj.id , type =   a.lower() )
        obj2 = workflowitems.objects.create(transitionmanager = obj ,model_type = a.upper() , event_user = get_current_user() , initial_state = states.description ,interim_state = states.description, final_state = states.description)
        workevents.objects.create(workflowitems = obj2 , type = a.upper() , event_user = get_current_user() , record_datas = gets_transition.get_record_datas(), initial_state = states.description ,interim_state = states.description,  final_state = states.description)
    pass
        

## B
@finflo_receiver(post_save, senders = b)
def create(sender, instance, **kwargs):
        try:
            PartyType.objects.create(description = instance.name)
        except:
            pass



# POST DELETE 

## A
@finflo_receiver(post_delete, senders = a)
def delete(sender, instance, **kwargs):
        a = str(sender)
        remove_characters = ["class", "models.","'","<",">"," "]
        for i in remove_characters:
            a = a.replace(i,"")
        TransitionManager.objects.filter(type = a.capitalize() , t_id = instance.id).delete()
    

##  B
@finflo_receiver(post_delete, senders = b)
def delete(sender, instance, **kwargs):
        PartyType.objects.delete(description = instance.name)


