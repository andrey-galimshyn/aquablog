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

from aquablog.forms import DocumentForm
from aquablog.models import Document

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

#@login_required
def profile(request, pk):
    """Edit user profile."""
    try:
        profile = UserProfile.objects.get(user=pk)
    except :
        profile = UserProfile(user=request.user)
        profile.save() 

    img = None
    pf = None

    if request.method == "POST":
        pf = ProfileForm(request.POST, request.FILES)
        if pf.is_valid():
            profile.avatar = request.FILES['avatar']
            profile.save()
            # resize and save image under same filename
            if not profile.avatar.name :
                profile.avatar.name = '/images/avatar.jpg'
            imfn = pjoin(settings.MEDIA_ROOT, profile.avatar.name)
            im = PImage.open(imfn)
            im.thumbnail((85,85), PImage.ANTIALIAS)
            im.save(imfn, "JPEG")
    else:
        pf = ProfileForm()

    if profile.avatar:
        img = pjoin(settings.MEDIA_URL, profile.avatar.name)
    return render_to_response("profile.html", {'pf':pf, 'img': img}, context_instance=RequestContext(request))



def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('aquablog.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
