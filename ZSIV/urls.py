from django.conf.urls import url
from . import views
from ZSIV.views import SummariesDetailView, DetailView
from .models import Summaries
from django.views.generic import TemplateView,  ListView

from ZSIV.views import SummariesCreateView, SummariesUpdateView, SummariesDeleteView, SummariesDetailView
from ZSIV.views  import TestFormstSetView
from ZSIV.models import Summaries
app_name = 'ZSIV'






urlpatterns = [
    # ex: /ZSIV/
    #url(r'^$', DetailView.as_view(),name='home'), # http://127.0.0.1:8000/ZSIV/
    
    
    
    url(r'^$', views.index, name='index'),
    
    # Summariey Views
    url(r'^Summaries-all$',
        ListView.as_view(
            model=Summaries,
            queryset=Summaries.objects.order_by('-updated').select_related(),
            context_object_name='all_summaries',
            #paginate_by = '5',
            template_name='ZSIV/summaries_list.html', # not required, is the default  
            ),
        name='summaries-index'),
               
    
    url(r'^Summaries/delete/$', TestFormstSetView.as_view(), name='Summaries-delete-multi'),
    # Summaries Trias - Add and Update work 
    url(r'^Summaries/add/$', SummariesCreateView.as_view(), name='Summaries-add'), #http://localhost:8000/ZSIV/Summaries/add/
    url(r'^Summaries/update/(?P<pk>[0-9]+)/$', SummariesUpdateView.as_view(), name='Summaries-update'),
    url(r'^Summaries/delete/(?P<pk>[0-9]+)/$', SummariesDeleteView.as_view(), name='Summaries-delete'), # http://localhost:8000/ZSIV/Summaries/delete/93/
    
    #url(r'^Summaries/(?P<pk>[0-9]+)/delete/$', SummariesDeleteView.as_view(), name='Summaries-delete'),
    #url(r'^Summaries/(?P<summary_id>[0-9]+)/detail/$',SummariesDetailView.as_view(), name="Summaries-detail"),
    
    # Subscriptions 
    url(r'^Mitarbeiter.html$', views.indexViewMA.as_view(), name='indexMA'), #http://localhost:8000/ZSIV/Mitarbeiter.html
    url(r'^MitarbeiterSubscribe/(?P<mitarbeiter_id>[0-9]+)/$', views.MA_Subscribe_Journals, name='MitarbeiterSubscribe'),
    url(r'^Journals.html$', views.indexViewJournals.as_view(), name='indexJournal'),
    url(r'^JournalSubscribe/(?P<journal_id>[0-9]+)/$', views.Journal_Subscribe_MAs, name='JournalSubscribe'), #http://localhost:8000/ZSIV/JournalSubscribe/
    
]