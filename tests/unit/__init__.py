
import os
import sys
import dummy_settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adapters.certuk_adhoc.tests.unit.dummy_settings')
sys.modules['repository.settings'] = sys.modules['adapters.certuk_adhoc.tests.unit.dummy_settings']
