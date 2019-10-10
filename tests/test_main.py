import os
import sys

path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '..',
    'sa-crawler'
)
sys.path.append(path)

import main  # noqa E402


def test_load_config():
    config = main.load_config()
    assert isinstance(config, dict)
    assert 'records' in config
    assert 'crawler' in config
    assert 'base_url' in config['crawler']
    assert 'components' in config['crawler']


def test_build_url():
    config = {}
    result = main.build_url(config, None, None)
    assert result is None

    config['crawler'] = {}
    result = main.build_url(config, None, None)
    assert result is None

    config['crawler']['base_url'] = 'https://nowhere.com'
    result = main.build_url(config, None, None)
    assert result['url'] == 'https://nowhere.com/'

    config = main.load_config()
    result = main.build_url(config, 'list_records', 'by_speaker')
    assert result['url'] == 'https://sermonaudio.com/search.asp'
    assert result['params'].get('currpage') == 1
    assert result['params'].get('sortby') == 'date'
    assert result['params'].get('AudioOnly') == 'false'
    assert result['params'].get('keyword') == '{speaker_name}'
    assert result['params'].get('SpeakerOnly') == 'true'
    assert 'search_term' not in result['params']

    result = main.build_url(config, 'list_records', 'by_speaker', page=3,
                            speaker_name='Steven Anderson')
    assert result['url'] == 'https://sermonaudio.com/search.asp'
    assert result['params'].get('currpage') == 3
    assert result['params'].get('sortby') == 'date'
    assert result['params'].get('AudioOnly') == 'false'
    assert result['params'].get('keyword') == 'Steven Anderson'
    assert result['params'].get('SpeakerOnly') == 'true'
    assert 'search_term' not in result['params']
