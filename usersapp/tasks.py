from django.core.mail import send_mail
from celery import shared_task
from mysite.settings import EMAIL_HOST

# @shared_task
# def send_mail_password_reset(receiver_email,reset_url):
#     #sender mail

#     subject="Reset Password"
#     message = reset_url
#     reply_to_list=[receiver_email, ]       
#     email = EmailMessage(subject,message,'huzefamohammed10@gmail.com',reply_to_list)
#     email.send(fail_silently=True)
#     return "Task Completed"

# @shared_task
# def send_mail_activation_link(receiver_email,activation_link):

#     #send mail
#     subject="Activation Link"
#     # print('subject')
#     message = activation_link
#     reply_to_list=[receiver_email, ]
#     # print(receiver_email, activation_link)    
#     email = EmailMessage(subject,message,'huzefamohammed10@gmail.com',reply_to_list)
#     email.send(fail_silently=True)
#     # email_from = settings.EMAIL_HOST

#     # send_mail(subject, message, email_from, recipient_list)

#     return "Task Completed"

@shared_task
def send_mail_link(receiver_email,activation_link, subject, message):
    #send mail
    reply_list=[receiver_email, ]
    # mailjet
    email_from = EMAIL_HOST
    # smtp
    # email_from = settings.EMAIL_HOST_USER
    send_mail(
        subject = subject,
        message=message,
        from_email=email_from,
        recipient_list=reply_list,
        fail_silently=False,
        )

    return "Task Completed"
