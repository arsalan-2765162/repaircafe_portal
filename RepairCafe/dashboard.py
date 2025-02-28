"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'RepairCafe.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'RepairCafe.dashboard.CustomAppIndexDashboard'
"""

try:
    # we use django.urls import as version detection as it will fail on django 1.11 and thus we are safe to use
    # gettext_lazy instead of ugettext_lazy instead
    from django.urls import reverse
    from django.utils.translation import gettext_lazy as _
except ImportError:
    from django.core.urlresolvers import reverse
    from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name
from RepairCafe.models import Ticket
from datetime import datetime
from django.utils import timezone
class SuccessRateCategoriesModule(modules.DashboardModule):
    title = 'Repair Success By Categories'

    def __init__(self, title=None, **kwargs):
        super().__init__(title, **kwargs)
        self.template = 'success_rate_categories.html'  # Path to your template
        
    def init_with_context(self,context):
        request=context['request']
        start_date_str=request.GET.get('graph_start_date')
        #print(start_date_str)
        end_date_str=request.GET.get('graph_end_date')
        start_date_provided=False
        end_date_provided=False

        if not start_date_str:
            start_date=datetime(1870, 1, 1, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
        else:
            start_date_provided=True
            start_date=start_date_str.replace("T", " ")

        if not end_date_str:
            end_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            end_date_provided=True
            end_date=end_date_str.replace("T", " ")

        successdict={}
        if start_date_provided and end_date_provided:
            message=f"showing repairs between {start_date} and {end_date}"
        elif start_date_provided:
            message=f"showing repairs after {start_date}"
        elif end_date_provided:
            message=f"showing repairs before {end_date}"
        else:
            message=""

        successdict['message']=message


        
        successdict['categories']={}
        for category in Ticket.ITEM_CATEGORY_CHOICES:
            successdict['categories'][category[1]]=(Ticket.objects.filter(itemCategory=category[0],repairStatus='COMPLETED',time_created__range=[start_date,end_date]).count(),Ticket.objects.filter(itemCategory=category[0],repairStatus='INCOMPLETE',time_created__range=[start_date,end_date]).count())

        self.children=successdict

    def is_empty(self):
        # Return False to ensure the module is always displayed
        return False
    
class   OtherStatsModule(modules.DashboardModule):
    title = 'Other statistics'

    def __init__(self, title=None,**kwargs):
        super().__init__(title,**kwargs)
        self.template='other_stats.html'

    def init_with_context(self,context):
        request=context['request']
        start_date_str=request.GET.get('other_stats_start_date')
        end_date_str=request.GET.get('other_stats_end_date')
        start_date_provided=False
        end_date_provided=False

        if not start_date_str:
            start_date=datetime(1870, 1, 1, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
        else:
            start_date_provided=True
            start_date=start_date_str.replace("T", " ")

        if not end_date_str:
            end_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            end_date_provided=True
            end_date=end_date_str.replace("T", " ")

        successdict={}
        if start_date_provided and end_date_provided:
            message=f"showing repairs between {start_date} and {end_date}"
        elif start_date_provided:
            message=f"showing repairs after {start_date}"
        elif end_date_provided:
            message=f"showing repairs before {end_date}"
        else:
            message=""
        
        checkedin = Ticket.objects.exclude(repairStatus = "WAITING").filter(time_created__range=[start_date,end_date]).count()
        checkedout = Ticket.objects.filter(isCheckedOut = True,time_created__range=[start_date,end_date]).count()
        successful = Ticket.objects.filter(repairStatus = "COMPLETED",time_created__range=[start_date,end_date]).count()#should tickets have a date? as this will be all completed tickets
        unsuccessful = Ticket.objects.filter(repairStatus = "INCOMPLETE",time_created__range=[start_date,end_date]).count()
        catpercentages = {}

        for category in Ticket.ITEM_CATEGORY_CHOICES:
            if Ticket.objects.filter(time_created__range=[start_date,end_date]).count()>0:
                catpercentages[category] = round(((Ticket.objects.filter(itemCategory = category[0],time_created__range=[start_date,end_date]).count())/ (Ticket.objects.filter(time_created__range=[start_date,end_date]).count()) * 100), 1)
            else:
                catpercentages[category]=0

    

        context_dict = {"checkedin":checkedin, "checkedout":checkedout, "successful":successful, "unsuccessful":unsuccessful, "catpercentages":catpercentages,"message":message}


        self.children=context_dict

    def is_empty(self):
        # Return False to ensure the module is always displayed
        return False


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for RepairCafe.
    """
    def init_with_context(self, context):
        self.columns=3
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Modify or delete records'),
            exclude=('django.contrib.*','repairCafe.Models.Queue'),
        ))
        
        

        self.children.append(OtherStatsModule())

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        

        self.children.append(SuccessRateCategoriesModule())

        #self.children.append(TotalSuccessRateModule())

        '''# append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))'''

        '''# append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ]
        ))'''


'''class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for RepairCafe.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)'''
