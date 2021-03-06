from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.decorators import block_guest

@block_guest
def alerts(request):
    now = timezone.now()
    alerts = {}
    if not request.user.alerts_date:
        request.user.alerts_date = request.user.join_date

    for alert in request.user.alert_set.order_by('-id'):
        alert.new = alert.date > request.user.alerts_date
        diff = now - alert.date
        if diff.days <= 0:
            try:
                alerts['today'].append(alert)
            except KeyError:
                alerts['today'] = [alert]
        elif diff.days <= 1:
            try:
                alerts['yesterday'].append(alert)
            except KeyError:
                alerts['yesterday'] = [alert]
        elif diff.days <= 7:
            try:
                alerts['week'].append(alert)
            except KeyError:
                alerts['week'] = [alert]
        elif diff.days <= 30:
            try:
                alerts['month'].append(alert)
            except KeyError:
                alerts['month'] = [alert]
        else:
            try:
                alerts['older'].append(alert)
            except KeyError:
                alerts['older'] = [alert]

    new_alerts = request.user.alerts
    request.user.alerts = 0
    request.user.alerts_date = now
    request.user.save(force_update=True)
    return request.theme.render_to_response('alerts.html',
                                            {
                                             'new_alerts': new_alerts,
                                             'alerts': alerts,
                                             },
                                            context_instance=RequestContext(request))
