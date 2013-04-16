"""Views for the Zinnia Aquablog"""
from django.conf import settings
from django.template import loader
from django.template import Context
from django.http import HttpResponseServerError
from django.contrib.auth import authenticate, login
from aquablog.forms import UserCreationForm, ProfileForm
from aquablog.models import UserProfile
from django.contrib.auth.tokens import default_token_generator
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.utils.http import urlquote, base36_to_int
from django.contrib.sites.models import Site
from os.path import join as pjoin
from PIL import Image as PImage
from django.contrib.auth.decorators import login_required

from aquablog.forms import DocumentForm
from aquablog.models import Document

#the decorator
'''
def custom_login_required(f):
        def wrap(request, *args, **kwargs):
                #this check the session if userid key exist, if not it will redirect to login page
                if not request.user.is_authenticated():
                        return HttpResponseRedirect(settings.LOGIN_URL)
                return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap
'''

def server_error(request, template_name='500.html'):
    """
    500 error handler.
    Templates: `500.html`
    Context:
    STATIC_URL
      Path of static media (e.g. "media.example.org")
    """
    t = loader.get_template(template_name)
    return HttpResponseServerError(
        t.render(Context({'STATIC_URL': settings.STATIC_URL})))

def signup(request, template_name='registration/signup.html', 
           email_template_name='registration/signup_email.html',
           signup_form=UserCreationForm,
           token_generator=default_token_generator,
           post_signup_redirect=None):
    if post_signup_redirect is None:
        post_signup_redirect = reverse('aquablog.views.signup_done')
    if request.method == "POST":
        form = signup_form(request.POST)
        if form.is_valid():
            opts = {}
            opts['use_https'] = request.is_secure()
            opts['token_generator'] = token_generator
            opts['email_template_name'] = email_template_name
            if not Site._meta.installed:
                opts['domain_override'] = RequestSite(request).domain
            form.save(**opts)
            return HttpResponseRedirect(post_signup_redirect)
    else:
        form = signup_form()
    return render_to_response(template_name, {'form': form,}, 
                              context_instance=RequestContext(request))

def signup_done(request, template_name='registration/signup_done.html'):
    return render_to_response(template_name, 
                              context_instance=RequestContext(request))

def signup_confirm(request, uidb36=None, token=None,
                   token_generator=default_token_generator,
                   post_signup_redirect=None):
    assert uidb36 is not None and token is not None #checked par url
    if post_signup_redirect is None:
        post_signup_redirect = reverse('aquablog.views.signup_complete')
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, id=uid_int)
    context_instance = RequestContext(request)

    if token_generator.check_token(user, token):
        context_instance['validlink'] = True
        user.is_active = True
        user.save()
    else:
        context_instance['validlink'] = False
    return HttpResponseRedirect(post_signup_redirect)

def signup_complete(request, template_name='registration/signup_complete.html'):
    return render_to_response(template_name, 
                              context_instance=RequestContext(request, 
                                                              {'login_url': settings.LOGIN_URL}))

@login_required
def profile(request, pk):
    """Edit user profile."""
    try:
        if int(pk) != request.user.id:
           return HttpResponseRedirect(settings.LOGIN_URL)
        profile = UserProfile.objects.get(user=pk)
    except :
        profile = UserProfile(user=request.user)
        profile.save() 

    img = None
    pf = None

    if request.method == "POST":
        pf = ProfileForm(user=request.user, data=request.POST)
        #pf = ProfileForm(request.POST, request.FILES)
        if pf.is_valid():
            local_avatar = None
            try:
                local_avatar = request.FILES['avatar']
            except KeyError:
                pass
            #print request.POST['categories']
            cats = request.POST.getlist('categories')
            #pf.bla
            # resize and save image under same filename
            if local_avatar :
                profile.avatar = local_avatar
                imfn = pjoin(settings.MEDIA_ROOT, profile.avatar.name)
                im = PImage.open(imfn)
                im.thumbnail((85,85), PImage.ANTIALIAS)
                im.save(imfn, "JPEG")
            profile.categories.clear()
            for c in cats:
                profile.categories.add(c)
            profile.save()

    else:
        pf = ProfileForm(user=request.user)
        #pf = ProfileForm()

    if profile.avatar:
        img = pjoin(settings.MEDIA_URL, profile.avatar.name)
    return render_to_response("profile.html", {'pf':pf, 'img': img}, context_instance=RequestContext(request))