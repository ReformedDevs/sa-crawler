# built ins
import os
from six import string_types

# third party
import yaml

# local


def load_config():
    """Return a mapping object of configuration items from config.yaml."""

    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'config.yaml'
    )
    with open(path) as f:
        config = yaml.safe_load(f)

    return config


def build_url(config, component, sub_component, page=None, **kwargs):
    """Use config and inputs to determins url and params for crawling

    Arguments:
    config (dict): the configuration information
    component (string): the component to crawl
    sub_component (string): the sub_component/component type to crawl

    Keyword arguments:
    page (int): the page number of the data to crawl, if paginated
    **kwargs: additional inputs to substitute values into config values

    Returns:
    dict:
        url: the url to use for crawling
        params: the query string parameters to use for crawling
    """

    params = {}
    config = config.get('crawler')
    if not config:
        return None

    url = config.get('base_url')
    if not url:
        return None

    if url[-1] != '/':
        url += '/'

    comp = config.get('components', {}).get(component)
    if comp:
        url += comp.get('path', '')
        params.update(comp.get('params', {}))

        pagination_param = comp.get('pagination_param')
        if pagination_param:
            if not isinstance(page, int):
                page = 1
            params.update({pagination_param: page})

        sub = comp.get('types', {}).get(sub_component)
        if sub:
            params.update(sub.get('params', {}))

    deletes = set()
    for k, v in params.items():
        if isinstance(v, string_types) and v[0] == '{' and v[-1] == '}':
            term = v[1:-1]
            v = kwargs.get(term, v)
            if term in list(params.keys()):
                v = params[term]
                if (isinstance(v, string_types)
                        and v[0] == '{' and v[-1] == '}'):
                    v = kwargs.get(v[1:-1], v)

                deletes.add(term)

            params[k] = v

    for d in deletes:
        del params[d]

    return {'url': url, 'params': params}
