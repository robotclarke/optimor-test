# -*- coding: utf8 -*-

from StringIO import StringIO
import sys
import uuid

from mock import MagicMock
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

import app


class MockWebDriver(object):
    def get(self, url):
        self.url = url


class MockWait(object):
    def __init__(self, field):
        self.field = field

    def until(self, expected_condition):
        return self.field


class MockInputField(WebElement):
    def __init__(self, *args, **kwargs):
        self.keys = []
        self.cleared = False
        super(MockInputField, self).__init__(*args, **kwargs)

    def send_keys(self, *value):
        for key in value:
            if isinstance(key, basestring):
                for char in key:
                    self.keys.append(char)
            else:
                self.keys.append(key)

    def clear(self):
        self.cleared = True


class MockHTMLField(WebElement):
    def get_attribute(self, name):
        if name == 'innerHTML':
            return u'£5'
        else:
            return super(MockHTMLField, self).get_attribute(name)


@pytest.fixture(scope='function')
def browser():
    return MockWebDriver()


@pytest.fixture(scope='function')
def input_field():
    return MockInputField(MagicMock(), uuid.uuid4())


@pytest.fixture(scope='function')
def html_field():
    return MockHTMLField(MagicMock(), uuid.uuid4())


@pytest.fixture(scope='function')
def html_field_wait(html_field):
    return MockWait(html_field)


def test_print_all_tariffs_sets_browser_url_correctly(browser, html_field_wait):
    app.print_all_tariffs([], browser, html_field_wait)

    assert browser.url == app.TARIFF_URL


def test_print_country_landline_tariff_inputs_country_name_correctly(input_field, html_field_wait):
    app._print_country_landline_tariff('Canada', input_field, html_field_wait)

    assert input_field.keys == ['C', 'a', 'n', 'a', 'd', 'a', Keys.RETURN]


def test_print_country_landline_tariff_clears_input(input_field, html_field_wait):
    app._print_country_landline_tariff('Canada', input_field, html_field_wait)

    assert input_field.cleared


def test_print_country_landline_tariff_prints_correctly(input_field, html_field_wait, request):
    printer = StringIO()
    sys.stdout = printer
    def tear_down():
        sys.stdout = sys.__stdout__
    request.addfinalizer(tear_down)

    app._print_country_landline_tariff('Canada', input_field, html_field_wait)

    assert printer.getvalue() == u'Canada: £5\n'
