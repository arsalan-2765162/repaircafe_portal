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
class SuccessRateCategoriesModule(modules.DashboardModule):
    title = 'Repair Success By Categories'

    def __init__(self, title=None, **kwargs):
        super().__init__(title, **kwargs)
        self.template = 'success_rate_categories.html'  # Path to your template
        
    def init_with_context(self,context):
        successdict={}
        successdict['categories']={}
        for category in Ticket.ITEM_CATEGORY_CHOICES:
            successdict['categories'][category[1]]=(Ticket.objects.filter(itemCategory=category[0],repairStatus='COMPLETED').count(),Ticket.objects.filter(itemCategory=category[0],repairStatus='INCOMPLETE').count())

        self.children=successdict

    def is_empty(self):
        # Return False to ensure the module is always displayed
        return False
    
class   OtherStatsModule(modules.DashboardModule):
    title = 'Total Repair Success Rate'

    def __init__(self, title=None,**kwargs):
        super().__init__(title,**kwargs)
        self.template='other_stats.html'

    def init_with_context(self,context):
        
        checkedin = Ticket.objects.exclude(repairStatus = "WAITING").count()
        checkedout = Ticket.objects.filter(isCheckedOut = True).count()
        successful = Ticket.objects.filter(repairStatus = "COMPLETED").count()#should tickets have a date? as this will be all completed tickets
        unsuccessful = Ticket.objects.filter(repairStatus = "INCOMPLETE").count()
        catpercentages = {}

        for category in Ticket.ITEM_CATEGORY_CHOICES:
            catpercentages[category] = round(((Ticket.objects.filter(itemCategory = category[0]).count())/ (Ticket.objects.count()) * 100), 1)

    

        context_dict = {"checkedin":checkedin, "checkedout":checkedout, "successful":successful, "unsuccessful":unsuccessful, "catpercentages":catpercentages}


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
        
        self.children.append(SuccessRateCategoriesModule())

        self.children.append(OtherStatsModule())

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

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
