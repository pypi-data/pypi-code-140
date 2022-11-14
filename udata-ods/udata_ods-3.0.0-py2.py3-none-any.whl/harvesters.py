import mimetypes
import os

from dateutil.parser import parse as parse_date

from udata.core.dataset.models import HarvestDatasetMetadata, HarvestResourceMetadata
from udata.frontend.markdown import parse_html
from udata.i18n import gettext as _
from udata.harvest.backends.base import BaseBackend, HarvestFilter, HarvestFeature
from udata.harvest.exceptions import HarvestSkipException
from udata.models import License, Resource
from udata.utils import get_by


def guess_format(mimetype, url=None):
    '''
    Guess a file format given a MIME type and/or an url
    '''
    # TODO: factorize in udata
    ext = mimetypes.guess_extension(mimetype)
    if not ext and url:
        parts = os.path.splitext(url)
        ext = parts[1] if parts[1] else None
    return ext[1:] if ext and ext.startswith('.') else ext


def guess_mimetype(mimetype, url=None):
    '''
    Guess a MIME type given a string or and URL
    '''
    # TODO: factorize in udata
    if mimetype in mimetypes.types_map.values():
        return mimetype
    elif url:
        mime, encoding = mimetypes.guess_type(url)
        return mime


class OdsBackend(BaseBackend):
    display_name = 'OpenDataSoft'
    verify_ssl = False
    filters = (
        HarvestFilter(_('Tag'), 'tags', str, _('A tag name')),
        HarvestFilter(_('Publisher'), 'publisher', str, _('A publisher name')),
    )
    features = (
        HarvestFeature('inspire', _('Harvest Inspire datasets'),
                       _('Whether this harvester should import datasets coming from Inspire')),
    )

    # Map filters key to ODS facets
    FILTERS = {
        'tags': 'keyword',
        'publisher': 'publisher',
    }

    # above this records count limit, shapefile export will be disabled
    # since it would be a partial export
    SHAPEFILE_RECORDS_LIMIT = 50000

    LICENSES = {
        'Open Database License (ODbL)': 'odc-odbl',
        'Licence Ouverte (Etalab)': 'fr-lo',
        'Licence ouverte / Open Licence': 'fr-lo',
        'CC BY-SA': 'cc-by-sa',
        'Public Domain': 'other-pd'
    }

    FORMATS = {
        'csv': ('CSV', 'csv', 'text/csv'),
        'geojson': ('GeoJSON', 'geojson', 'application/vnd.geo+json'),
        'json': ('JSON', 'json', 'application/json'),
        'shp': ('Shapefile', 'shp', None),
    }

    @property
    def source_url(self):
        return self.source.url.rstrip('/')

    @property
    def api_search_url(self):
        return '{0}/api/datasets/1.0/search/'.format(self.source_url)

    def api_dataset_url(self, dataset_id):
        return '{0}/api/datasets/1.0/{1}/'.format(self.source_url, dataset_id)

    def explore_url(self, dataset_id):
        return '{0}/explore/dataset/{1}/'.format(self.source_url, dataset_id)

    def extra_file_url(self, dataset_id, file_id, plural_type):
        return '{0}/api/datasets/1.0/{1}/{2}/{3}'.format(
            self.source_url, dataset_id, plural_type, file_id
        )

    def download_url(self, dataset_id, format):
        return ('{0}download?format={1}&timezone=Europe/Berlin'
                '&use_labels_for_header=false'
                ).format(self.explore_url(dataset_id), format)

    def export_url(self, dataset_id):
        return '{0}?tab=export'.format(self.explore_url(dataset_id))

    def initialize(self):
        count = 0
        nhits = None

        def should_fetch():
            if nhits is None:
                return True
            max_value = min(nhits, self.max_items) if self.max_items else nhits
            return count < max_value

        while should_fetch():
            params = {
                'start': count,
                'rows': 50,
                'interopmetas': 'true',
            }
            for f in self.get_filters():
                ods_key = self.FILTERS.get(f['key'], f['key'])
                op = 'exclude' if f.get('type') == 'exclude' else 'refine'
                key = '.'.join((op, ods_key))
                param = params.get(key, set())
                param.add(f['value'])
                params[key] = param
            response = self.get(self.api_search_url, params=params)
            response.raise_for_status()
            data = response.json()
            nhits = data['nhits']
            for dataset in data['datasets']:
                count += 1
                self.add_item(dataset['datasetid'])

    def process(self, item):
        dataset_id = item.remote_id
        response = self.get(self.api_dataset_url(dataset_id),
                            params={'interopmetas': 'true'})
        response.raise_for_status()
        ods_dataset = response.json()
        ods_metadata = ods_dataset['metas']
        ods_interopmetas = ods_dataset.get('interop_metas', {})

        if not any((ods_dataset.get(attr) for attr
                    in ('has_records', 'attachments', 'alternative_exports'))):
            msg = 'Dataset {datasetid} has no record'.format(**ods_dataset)
            raise HarvestSkipException(msg)

        if 'inspire' in ods_interopmetas and not self.has_feature('inspire'):
            msg = 'Dataset {datasetid} has INSPIRE metadata'
            raise HarvestSkipException(msg.format(**ods_dataset))

        dataset = self.get_dataset(item.remote_id)
        if not dataset.harvest:
            dataset.harvest = HarvestDatasetMetadata()

        dataset.title = ods_metadata['title']
        dataset.frequency = 'unknown'
        description = ods_metadata.get('description', '').strip()
        dataset.description = parse_html(description)
        dataset.private = False
        dataset.harvest.modified_at = ods_metadata['modified']

        tags = set()
        if 'keyword' in ods_metadata:
            if isinstance(ods_metadata['keyword'], list):
                tags |= set(ods_metadata['keyword'])
            else:
                tags.add(ods_metadata['keyword'])

        if 'theme' in ods_metadata:
            if isinstance(ods_metadata['theme'], list):
                for theme in ods_metadata['theme']:
                    tags.update([t.strip().lower() for t in theme.split(',')])
            else:
                themes = ods_metadata['theme'].split(',')
                tags.update([t.strip().lower() for t in themes])

        dataset.tags = list(tags)

        # Detect license
        default_license = dataset.license or License.default()
        license_id = ods_metadata.get('license')
        dataset.license = License.guess(license_id,
                                        self.LICENSES.get(license_id),
                                        default=default_license)

        self.process_resources(dataset, ods_dataset, ('csv', 'json'))

        if 'geo' in ods_dataset['features']:
            exports = ['geojson']
            if ods_metadata['records_count'] <= self.SHAPEFILE_RECORDS_LIMIT:
                exports.append('shp')
            self.process_resources(dataset, ods_dataset, exports)

        self.process_extra_files(dataset, ods_dataset, 'alternative_export')
        self.process_extra_files(dataset, ods_dataset, 'attachment')

        dataset.harvest.ods_url = self.explore_url(dataset_id)
        dataset.harvest.remote_url = self.explore_url(dataset_id)
        if 'references' in ods_metadata:
            dataset.harvest.ods_references = ods_metadata['references']
        dataset.harvest.ods_has_records = ods_dataset['has_records']
        dataset.harvest.ods_geo = 'geo' in ods_dataset['features']

        return dataset

    def process_extra_files(self, dataset, data, data_type):
        dataset_id = data['datasetid']
        modified_at = self.parse_date(data['metas']['modified'])
        plural_type = '{0}s'.format(data_type)
        for export in data.get(plural_type, []):
            url = self.extra_file_url(dataset_id, export['id'], plural_type)
            created, resource = self.get_resource(dataset, url)
            if not resource.harvest:
                resource.harvest = HarvestResourceMetadata()
            resource.title = export.get('title', 'No title')
            resource.description = export.get('description')
            resource.format = guess_format(export.get('mimetype'),
                                           export['url'])
            resource.mime = guess_mimetype(export.get('mimetype'),
                                           export['url'])
            resource.harvest.modified_at = modified_at
            resource.harvest.ods_type = data_type
            if created:
                dataset.resources.append(resource)

    def get_resource(self, dataset, url):
        resource = get_by(dataset.resources, 'url', url)
        if not resource:
            return True, Resource(url=url)
        return False, resource

    def process_resources(self, dataset, data, formats):
        if not data.get('has_records'):
            return
        dataset_id = data['datasetid']
        ods_metadata = data['metas']
        modified_at = self.parse_date(ods_metadata['modified'])
        description = self.description_from_fields(data['fields'])
        for _format in formats:
            label, udata_format, mime = self.FORMATS[_format]
            url = self.download_url(dataset_id, _format)
            created, resource = self.get_resource(dataset, url)
            if not resource.harvest:
                resource.harvest = HarvestResourceMetadata()
            resource.title = _('{format} format export').format(format=label)
            resource.description = description
            resource.filetype = 'remote'
            resource.format = udata_format
            resource.mime = mime
            resource.harvest.modified_at = modified_at
            resource.harvest.ods_type = 'api'
            if created:
                dataset.resources.append(resource)

    def description_from_fields(self, fields):
        '''Build a resource description/schema from ODS API fields'''
        if not fields:
            return

        out = ''
        for field in fields:
            out += '- *{label}*: {name}[{type}]'.format(**field)
            if field.get('description'):
                out += ' {description}'.format(**field)
            out += '\n'
        return out

    def parse_date(self, date_str):
        try:
            return parse_date(date_str)
        except ValueError:
            pass
