from django.views.generic import DetailView, TemplateView
from django.template import Context
from django.template.loader import get_template
from settings import STATIC_URL
from btsearch.bts.models import BaseStation, Cell, Network
from btsearch.uke.models import UkeLocation, UkePermission

class IndexView(TemplateView):
    template_name = 'map/index.html'

class ControlPanelView(TemplateView):
    template_name = 'map/control_panel.html'

    def get_context_data(self, **kwargs):
        context = super(ControlPanelView, self).get_context_data(**kwargs)
        context['networks'] = Network.objects.all()
        context['standards'] = Cell.STANDARDS
        context['bands'] = Cell.BANDS
        return context

class StatusPanelView(TemplateView):
    template_name = 'map/status_panel.html'

class BaseStationExtendedInfoView(DetailView):
    model = BaseStation
    context_object_name = 'base_station'
    template_name = 'map/base_station_extended_info.html'

class UkeLocationExtendedInfoView(DetailView):
    model = UkeLocation
    context_object_name = 'uke_location'
    template_name = 'map/uke_location_extended_info.html'

    def get_context_data(self, **kwargs):
        network = Network.objects.get(code=self.kwargs['network_code'])
        context = super(UkeLocationExtendedInfoView, self).get_context_data(**kwargs)
        context['permissions'] = UkePermission.objects.filter(uke_location=self.object, network=network)
        context['network'] = network
        return context

class LocationView():
    template_name = 'map/location_info.html'
    location = None
    raw_filters = {}

    def __init__(self, location, raw_filters):
        self.location = location
        self.raw_filters = raw_filters

    def get_location_items(self):
        filters = self.get_processed_filters()
        return self.location.get_base_stations(**filters)

    def get_processed_filters(self):
        filters = {}
        if 'standard' in self.raw_filters:
            filters['standard'] = self.raw_filters['standard'][0].split(',')
        if 'band' in self.raw_filters:
            filters['band'] = self.raw_filters['band'][0].split(',')
        return filters

    def render_location_info(self):
        template = get_template(self.template_name)
        context = {'location': self.location,
                   'items': self.get_location_items(),
                   'STATIC_URL': STATIC_URL}
        return template.render(Context(context))

class UkeLocationView(LocationView):
    template_name = 'map/uke_location_info.html'

    def get_location_items(self):
        permissions_by_network = {}
        networks = []
        filters = self.get_processed_filters()
        for permission in self.location.get_permissions(**filters):
            network = permission.network
            if network not in networks:
                networks.append(network)

            if not permissions_by_network.has_key(network.code):
                permissions_by_network[network.code] = []
            permissions_by_network[network.code].append(permission)

        items = []
        for network in networks:
            items.append({'network': network,
                          'supported': self.location.get_supported_standards_and_bands_by_network(network),
                          'permissions': permissions_by_network[network.code]})
        return items