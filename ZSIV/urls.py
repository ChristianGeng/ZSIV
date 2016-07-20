from django.conf.urls import url
from . import views
from ZSIV.views import home, SummariesDetailView, DetailView
from .models import Summaries

from ZSIV.views import SummariesCreateView, SummariesUpdateView, SummariesDeleteView, SummariesDetailView

app_name = 'ZSIV'
urlpatterns = [
    # ex: /ZSIV/
    #url(r'^$', DetailView.as_view(),name='home'), # http://127.0.0.1:8000/ZSIV/
    
    # Summaries
    url(r'^Summaries/add/$', SummariesCreateView.as_view(), name='Summaries-add'),
    url(r'^Summaries/(?P<pk>[0-9]+)/$', SummariesUpdateView.as_view(), name='Summaries-update'),
    url(r'^Summaries/(?P<pk>[0-9]+)/delete/$', SummariesDeleteView.as_view(), name='Summaries-delete'),
    
    #url(r'^Summaries/(?P<pk>[0-9]+)/details/$',SummariesDetailView.as_view() ,name='Summaries-detail'),
    url(r'^Summaries/(?P<pk>[0-9]+)/detail/$',SummariesDetailView.as_view(), name="Summaries-detail"),
    
    # Mitarbeiter
    url(r'^Mitarbeiter.html$', views.indexViewMA.as_view(), name='indexMA'), #http://localhost:8000/ZSIV/Mitarbeiter.html
    url(r'^MitarbeiterSubscribe/(?P<mitarbeiter_id>[0-9]+)/$', views.MA_Subscribe_Journals, name='MitarbeiterSubscribe'),
    #url(r'^mitarbeiter/(?P<pk>[0-9]+)/$', views.subscribe, name='subscribe'),
    
    
    
    #url(r'^Journals.html$',views.JournalIndexView , name='indexJournal'),
    #url(r'^Journals.html$', views.index.as_view()),
    url(r'^Journals.html$', views.indexViewJournals.as_view(), name='indexJournal'),
    url(r'^JournalSubscribe/(?P<journal_id>[0-9]+)/$', views.Journal_Subscribe_MAs, name='JournalSubscribe'), #http://localhost:8000/ZSIV/JournalSubscribe/
    
]