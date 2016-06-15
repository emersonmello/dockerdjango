from accounts.models import Profile
from basket.models import Basket

def retrieve_basket(request):
    if (request.session.has_key('carry_over_basket')
            and request.session['carry_over_basket']):
            if ( request.session.has_key('anon_basket_id')
                and request.session['anon_basket_id']):
                session = request.session['anon_basket_id']
            else:
                session = built_session(request)
            basket =  Basket.objects.get(session=session, active=True)
    else:
        session = built_session(request)
        basket = Basket.objects.create(session=session, active=True)
    return basket


def get_current_basket(request):
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
        session = built_session(request)
        try:
            basket = Basket.objects.get(user=profile, active=True,
                session=session)
        except Basket.DoesNotExist:
            basket = retrieve_basket(request)
            basket.user = profile
            basket.save()
    else:
        basket = retrieve_basket(request)
        if not request.session.has_key('carry_over_basket'):
            request.session['carry_over_basket'] = True
            session = built_session(request)
            request.session['anon_basket_id'] = session
    return basket


def built_session(request):
    user_agent = request.META['HTTP_USER_AGENT']
    ip_address = get_ip(request)
    session = '%s:%s' % (ip_address, user_agent)

    return session


def get_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        # HTTP_X_FORWARDED_FOR sometimes have a comma delimited list of IP addresses
        # Here we want the originating IP address
        # See http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/x-forwarded-headers.html
        # and https://en.wikipedia.org/wiki/X-Forwarded-For
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0].strip() or None
    else:
        ip_address = request.META.get('REMOTE_ADDR', None)
    return ip_address
