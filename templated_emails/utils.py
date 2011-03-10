from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import Template, Context
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
import logging
from django.template.loader import get_template

def send_templated_email(recipients, template_path, context={},
                    from_email=settings.DEFAULT_FROM_EMAIL):
    current_site = Site.objects.get(id=settings.SITE_ID)
    context["current_site"] = current_site
    context["STATIC_URL"] = settings.STATIC_URL
    
    context = Context(context)
    subject = render_to_string("%s/short.txt"%template_path, context)\
                                .replace('\n', '').replace('\r', '')
    text = render_to_string("%s/email.txt"%template_path, context)
    
    body = None
    body_template = None
    html_path = "%s/email.html"%template_path
    try:
        body_template = get_template(html_path)
    except TemplateDoesNotExist:
        logging.info("Email sent without HTML, since %s not found"%html_path)
        
    msg = EmailMultiAlternatives(subject, text, from_email, recipients)
    
    if body_template:
        body = render_to_string(html_path, context)
        msg.attach_alternative(body, "text/html")

    msg.send()

