from django.conf.urls import url
from . import views
from ZSIV.views import SummariesDetailView, DetailView
from .models import Summaries
from django.views.generic import ListView

from ZSIV.views import SummariesCreateView, SummariesUpdateView, SummariesDeleteView
from ZSIV.views  import TestFormstSetView
from ZSIV.views  import Queuelistview
from ZSIV.views  import JournalCreateView
from ZSIV.models import Mitarbeiter
app_name = 'ZSIV'

urlpatterns = [

    # (1) Main Page
    # (2) Manage Subscriptions
    # (3) Manage Summaries
    # (4) Queue and send
    # (5) Versuche 
    
    
    # (1) Main Page, static so far
    url(r'^$', views.index, name='index'),
    

    # (2) Manage Subscriptions / jeweils ein Listview und ein View, der die Subscriptions managt
    url(r'^Mitarbeiter.html$', views.indexViewMA.as_view(), name='indexMA'), #http://localhost:8000/ZSIV/Mitarbeiter.html
    url(r'^MitarbeiterSubscribe/(?P<mitarbeiter_id>[0-9]+)/$', views.MA_Subscribe_Journals, name='MitarbeiterSubscribe'),
    url(r'^Journals.html$', views.indexViewJournals.as_view(), name='indexJournal'),
    url(r'^JournalSubscribe/(?P<journal_id>[0-9]+)/$', views.Journal_Subscribe_MAs, name='JournalSubscribe'), #http://localhost:8000/ZSIV/JournalSubscribe/

    
    
    
    # (3) Manage Summaries 
    
    # (3a) add, update, delete(nicht implementiert!)) + ein MultiDelete
    url(r'^Summaries/add/$', SummariesCreateView.as_view(), name='Summaries-add'), #http://localhost:8000/ZSIV/Summaries/add/
    url(r'^Summaries/update/(?P<pk>[0-9]+)/$', SummariesUpdateView.as_view(), name='Summaries-update'), 
    #url(r'^Summaries/delete/(?P<pk>[0-9]+)/$', SummariesDeleteView.as_view(), name='Summaries-delete'), # http://localhost:8000/ZSIV/Summaries/delete/93/
    url(r'^Summaries/delete/$', TestFormstSetView.as_view(), name='Summaries-delete-multi'),
    
    # (3b) Summary List Views - alle und nicht versandt
    url(r'^Summaries-all$',
        ListView.as_view(
            model=Summaries,
            queryset=Summaries.objects.order_by('-updated').select_related(),
            context_object_name='all_summaries',
            #paginate_by = '5',
            template_name='ZSIV/summaries_list.html', # not required, is the default  
            ),
        name='summaries-index'),
    url(r'^Summaries-unsent$',
        ListView.as_view(
            model=Summaries, 
            queryset=Summaries.objects.filter(SENT=False).select_related(),
            context_object_name='all_summaries',
            #paginate_by = '5',
            template_name='ZSIV/summaries_list.html', # not required, is the default  
            ),
        name='summaries-unsent'),

    
    
    
    # (4) Queue and send
    url(r'^queue$',
        Queuelistview.as_view(
                         model = Mitarbeiter,
                         template_name='ZSIV/queue_list.html',
                         ),
        name = 'queue'
        ),
    
    
    
    # (5) Versuche     
    # Ersetzen der Grunddaten (der admin-site)
    # Versuch, mehrere Journals hinzufuegen - defunct 
    url(r'^ttt/$', views.JournalCreateView.as_view(), name='add_journal_and_summaries'),
    
]