# http://getbootstrap.com/components/#breadcrumbs
from django.conf.urls import url
from django.views.generic import DeleteView, ListView

from ZSIV.models import Mitarbeiter, Summaries

from ZSIV.views import JournalCreateView, JournalDeleteView, JournalListview, JournalUpdateView, MessageTextView
from ZSIV.views import MitarbeiterCreateView, MitarbeiterDeleteView, MitarbeiterListview
from ZSIV.views import  SummariesUpdateView, TestFormstSetView, MitarbeiterUpdateView, Queuelistview, SummariesCreateView

from . import views

# from ZSIV.views import SummariesDeleteView # TODO: Implement!

# from ZSIV.views  import MyView
app_name = 'ZSIV'

# http://127.0.0.1:8000/ZSIV/queue
"""
    # (1) Main Page
    # (2) Manage Subscriptions
    # (3) Manage Summaries
    # (4) Queue and send,  email Text
    # (5) Versuche 
"""

# (1) Main Page, static so far
# url(r'^$', views.indexView, name='index'), # http://localhost:8000/ZSIV/

mainpage_ursl = [url(r'^$', views.MyView.as_view(), name='index')]

# (2) Manage Subscriptions / jeweils ein Listview und ein View, der die Subscriptions managt
# http://localhost:8000/ZSIV/Mitarbeiter.html
subscription_urls = [
    url(r'^Mitarbeiter.html$', views.indexViewMA.as_view(), name='indexMA'),
    url(r'^MitarbeiterSubscribe/(?P<mitarbeiter_id>[0-9]+)/$', views.MA_Subscribe_Journals,
        name='MitarbeiterSubscribe'),
    url(r'^Journals.html$', views.indexViewJournals.as_view(), name='indexJournal'),
    # http://localhost:8000/ZSIV/JournalSubscribe/
    url(r'^JournalSubscribe/(?P<journal_id>[0-9]+)/$', views.Journal_Subscribe_MAs, name='JournalSubscribe')
]

# (3) Manage Summaries
# (3a) add, update, delete(nicht implementiert!)) + ein MultiDelete
# http://localhost:8000/ZSIV/Summaries/add/
summary_urls = [
    url(r'^Summaries/add/$', SummariesCreateView.as_view(), name='Summaries-add'),
    url(r'^Summaries/update/(?P<pk>[0-9]+)/$', SummariesUpdateView.as_view(), name='Summaries-update'),
    url(r'^Summaries/delete/$', TestFormstSetView.as_view(), name='Summaries-delete-multi'),
    url(
        r'^Summaries-all$',
        ListView.as_view(
            model=Summaries,
            # queryset=Summaries.objects.order_by('-updated').select_related(),
            queryset=Summaries.objects.order_by('SENT').select_related(),
            context_object_name='all_summaries',
            paginate_by='15',
            template_name='ZSIV/summaries_list.html',  # not required, is the default
        ),
        name='summaries-index'),
    url(
        r'^Summaries-unsent$',
        ListView.as_view(
            model=Summaries,
            queryset=Summaries.objects.filter(SENT=False).select_related(),
            context_object_name='all_summaries',
            paginate_by='20',
            template_name='ZSIV/summaries_list.html',  # not required, is the default
        ),
        name='summaries-unsent'),
    url(
        r'^Summaries-sent-delete-experimental$',
        ListView.as_view(
            model=Summaries,
            queryset=Summaries.objects.filter(SENT=False).select_related(),
            context_object_name='all_summaries',
            template_name='ZSIV/summaries_delete-experimental.html',
        ),
        name='summaries-sent-delete-experimental')
]

# (4) Queue and send,  EmailText
email_urls = [
    url(r'^MessageText$', MessageTextView.as_view(), name='MessageText'), url(r'^queue$',
                                                                              Queuelistview.as_view(
                                                                                  model=Mitarbeiter,
                                                                                  template_name='ZSIV/queue_list.html',
                                                                              ),
                                                                              name='queue')
]

# (6) Manage Journals
# http://localhost:8000/ZSIV/Journal/add/
journal_urls = [
    url(r'^Journal/add/$', JournalCreateView.as_view(), name='Journal-add'),
    url(r'^Journals/all/$', JournalListview.as_view(), name='Journal-List'), url(r'^Journal/update/(?P<pk>[0-9]+)/$',
                                                                                 JournalUpdateView.as_view(),
                                                                                 name='Journal-update'),
    url(r'^Journal/delete/(?P<pk>[0-9]+)/$', JournalDeleteView.as_view(), name='Journal-delete')
]

# (7) Manage Mitarbeiter
mitarbeiter_urls = [
    url(r'^Mitarbeiter/add/$', MitarbeiterCreateView.as_view(),
        name='Mitarbeiter-add'), url(r'^Mitarbeiter/all/$', MitarbeiterListview.as_view(), name='Mitarbeiter-List'),
    url(r'^Mitarbeiter/update/(?P<pk>[0-9]+)/$', MitarbeiterUpdateView.as_view(),
        name='Mitarbeiter-update'), url(r'^Mitarbeiter/delete/(?P<pk>[0-9]+)/$',
                                        MitarbeiterDeleteView.as_view(),
                                        name='Mitarbeiter-delete')
]

# (XXX) Versuche
# Ersetzen der Grunddaten (der admin-site)
# Versuch, mehrere Journals hinzufuegen - defunct
experimental_urls = [url(r'^ttt/$', JournalCreateView.as_view(), name='add_journal_and_summaries')]

urlpatterns = []
urlpatterns += mainpage_ursl
urlpatterns += subscription_urls
urlpatterns += summary_urls
urlpatterns += email_urls
urlpatterns += journal_urls
urlpatterns += mitarbeiter_urls
urlpatterns += experimental_urls
