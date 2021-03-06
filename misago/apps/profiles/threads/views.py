from misago.apps.profiles.decorators import profile_view
from misago.apps.profiles.template import RequestContext
from misago.models import Forum
from misago.utils.pagination import make_pagination

@profile_view('user_threads')
def threads(request, user, page=0):
    queryset = user.thread_set.filter(forum_id__in=Forum.objects.readable_forums(request.acl)).filter(deleted=False).filter(moderated=False).select_related('start_post', 'forum').order_by('-id')
    count = queryset.count()
    pagination = make_pagination(page, count, 12)
    
    return request.theme.render_to_response('profiles/threads.html',
                                            context_instance=RequestContext(request, {
                                             'profile': user,
                                             'tab': 'threads',
                                             'items_total': count,
                                             'items': queryset[pagination['start']:pagination['stop']],
                                             'pagination': pagination,
                                             }));
