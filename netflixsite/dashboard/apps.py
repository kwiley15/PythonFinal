from django.apps import AppConfig #APpconfig base class to configure app settings 


class DashboardConfig(AppConfig): # configuration class for the dashboard django app
    default_auto_field = 'django.db.models.BigAutoField' 
    name = 'dashboard' #name of dashboard 

