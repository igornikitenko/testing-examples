# ----------conftest.py

API_URL = '/api/v1.0'
cohort_data = '/get_cohort_data?'
overall_data = '/get_overall_data?'
advt_data = '/get_advertising_data?'
flurry_data = '/get_flurry_data?'
impressions_data = '/get_impressions?'
cohort_revenue = '/get_cohort_revenue?'

no_chache = '&without_cache=1'

REPORT_TYPES = [1, 2, 3, 4]
APPLICATIONS = [1, 2, 3, 4]

@pytest.fixture(scope="function", autouse=True)
def set_up_login():
    """ setup login state for application"""

    bitool.app.testing = True
    bitool.app.config['TESTING'] = True
    bitool.app.login_manager.init_app(bitool.app)
    app = bitool.app.test_client()

    return app

@pytest.fixture(scope="function")
def no_login():
    """ setup no login state for application"""

    bitool.app.testing = True
    bitool.app.config['TESTING'] = True
    app = bitool.app.test_client()

    return app

# -----------------------------------------------

import datetime
from conftest import *

app = bitool.app.test_client()
resp_oa = app.get('/api/v1.0/get_overall_data?application=1&period=1&date=01-09-2017+-+30-09-2017&without_cache=1', follow_redirects=True)
overall_data = json.loads(resp_oa.data)
resp_cd = app.get(API_URL + '/get_cohort_data?report_type=0&period=1&date=01-09-2017+-+30-09-2017&days_limit=30&'
                             'without_cache=1&application=1&advt_revenue_type=1', follow_redirects=True)
cohort_data = json.loads(resp_cd.data)


def test_overall_report_keys():
    """
    Testing json from application, with test data fixtures, has correct keys - for overall report
    """
    keys = overall_data.keys()
    assert('banner_report' in keys)
    assert('rewarded_report' in keys)
    assert('interstitial_report' in keys)
    assert('overall_report' in keys)


def test_overall_report_banner():
    """
    Testing json from application, with test data fixtures, verify length - for overall banner report
    """
    assert (len(overall_data['banner_report']['data']) == 8)


def test_overall_report_banner_users():
    """
    Testing json from application, with test data fixtures, verify users data
    - for overall banner report
    """
    assert (overall_data['banner_report']['data'][0][0] == 'Users')
    for num in overall_data['banner_report']['data'][0][1:]:
        assert (num == 90)


def test_overall_report_banner_revenue():
    """
     Testing json from application, with test data fixtures, verify revenue data
     - for overall banner report
     """
    assert (overall_data['banner_report']['data'][1][0] == 'Revenue')
    for num in overall_data['banner_report']['data'][1][1:]:
        assert (num == 600)


def test_overall_report_banner_revenue_per_user():
    """
    Testing json from application, with test data fixtures, verify revenue per user data
    - for overall banner report
    """
    assert (overall_data['banner_report']['data'][2][0] == 'Revenue per user')
    for num in overall_data['banner_report']['data'][2][1:]:
        assert (num == 6.6667)


def test_overall_report_banner_impressions():
    """
    Testing json from application, with test data fixtures, verify impressions data
    - for overall banner report
    """
    assert (overall_data['banner_report']['data'][3][0] == 'Impressions')
    for num in overall_data['banner_report']['data'][3][1:]:
        assert (num == 150)


def test_overall_report_banner_ecpm():
    """
    Testing json from application, with test data fixtures, verify eCPM data
    - for overall banner report
    """
    assert (overall_data['banner_report']['data'][6][0] == 'eCPM')
    for num in overall_data['banner_report']['data'][6][1:]:
        assert (num == 4000)


def test_overall_report_columns():
    """
    Testing json from application, with test data fixtures, verify dates list length
    """
    assert (len(overall_data['columns']) == 31)


def test_overall_report_data():
    """
    Testing json from application, with test data fixtures, verify overall data list length
    """
    assert (len(overall_data['overall_report']['data']) == 8)


def test_overall_report_installs():
    """
    Testing json from application, with test data fixtures, verify Installs data
    - for overall report
    """
    assert (overall_data['overall_report']['data'][0][0] == 'Installs')
    for num in overall_data['overall_report']['data'][0][1:]:
        assert (num == 3)


def test_overall_report_active_users():
    """
    Testing json from application, with test data fixtures, verify Active users data
    - for overall report
    """
    assert (overall_data['overall_report']['data'][1][0] == 'Active users')
    for num in overall_data['overall_report']['data'][1][1:]:
        assert (num == 3)


def test_overall_report_sessions():
    """
    Testing json from application, with test data fixtures, verify Sessions data
    - for overall report
    """
    assert (overall_data['overall_report']['data'][2][0] == 'Sessions')
    for num in overall_data['overall_report']['data'][2][1:]:
        assert (num == 6)


def test_overall_report_sessions_per_active_user():
    """
    Testing json from application, with test data fixtures, verify Sessions per active user data
    - for overall report
    """
    assert (overall_data['overall_report']['data'][3][0] == 'Sessions per active user')
    for num in overall_data['overall_report']['data'][3][1:]:
        assert (num == 2)


def test_overall_report_inapp_revenue():
    """
    Testing json from application, with test data fixtures, verify IAP revenue data
    - for overall report
    """
    assert (overall_data['overall_report']['data'][4][0] == 'IAP revenue')
    assert (overall_data['overall_report']['data'][4][10] == 55)


def test_overall_report_ad_revenue():
    """
    Testing json from application, with test data fixtures, verify Ad revenue data
    - for overall report
    """
    assert (overall_data['overall_report']['data'][5][0] == 'Ad revenue')
    for num in overall_data['overall_report']['data'][5][1:]:
        assert (num == 600)


# -----------------------------------------------

def test_cohort_data():
    """
    Testing application api response for "/get_cohort_data?", checks response code and if
    response json has proper keys according to requested data
    """
    app = bitool.app.test_client()
    resp = app.get(API_URL + cohort_data + no_chache, follow_redirects=True)
    assert (resp.status_code == 200)
    data = json.loads(resp.data)
    calculated_users = sum([x[1] for x in data['report']['data']])
    sum_users = data['sum']['data'][0][0]
    assert (calculated_users == sum_users)


# -----------------------------------------------

@pytest.mark.usefixture('no_login')
def test_cohort_data_access_no_login():
    """
    Testing application response at "/cohort_data" address as non logged user, should redirect
    to login page
    """
    response = app.get('/cohort_data')
    assert (response._status_code == 302)
    assert (response.location[:36] =='https://accounts.google.com/o/oauth2')


# -----------------------------------------------


@pytest.mark.parametrize('rep_type', REPORT_TYPES)
@pytest.mark.parametrize('application', APPLICATIONS)
@pytest.mark.parametrize('periods, selected', [('1', "Daily"),
                                               ('2', "Weekly"),
                                               ('4', "Monthly")])
def test_periods_response(periods, selected, application, rep_type):
    """
    Testing application response, checks the response code and that html had selected option according
    to "periods" code, and html has appropriate title of selected option
    :param periods: 1, 2, 3
    :param selected: Daily, Weekly, Monthly
    :return:
    """
    app = bitool.app.test_client()
    resp = app.get('/cohort_data?period={}&report_type={}&application={}'.format(periods, rep_type, application))
    soup = BeautifulSoup(resp.data, "html5lib").find('select', id='period')
    text = soup.find('option', selected="selected").text
    assert (text == selected)
    assert(resp._status_code == 200)