'''
This class uses the Salesforce API to get data using an icp number.
- Salesforce API Documentation:
    https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_what_is_rest_api.htm
- GET Bearer token oauth2/token
- GET icp data data/v40.0/sobjects/Assessor_Production__c/Name/{icpNumber}/
- GET notes for the icp number using the record id (from salesforce) data/v40.0/sobjects/Assessor_Production__c/{id}/Notes
- UPDATE ICP record with PATCH https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_update_fields.htm
- GET List icp numbers based on submission status using SOQL
'''
import os

import requests
import jwt
import time
import inspect


class SalesforceApi(object):

    def __init__(self, configs_obj):
        self.configs_obj = configs_obj
        self.log = configs_obj.log
        self.env_config = configs_obj.env_config
        self.app_config = configs_obj.app_config

        self.log.info('SalesforceApi object created...')
        self.sf_env = self.env_config.sf_environment()
        if self.sf_env == 'config1':
            self.log.info('{} env'.format(self.sf_env))
            self.base_url = self.env_config.config_base_url()
            self.headers = {
                'Authorization': 'Bearer ' + self.get_token() + '',
                'Content-Type': 'application/json'
            }
        elif self.sf_env == 'prod':
            self.log.info('{} env'.format(self.sf_env))
            self.base_url = self.env_config.base_url()
            self.headers = {
                'Authorization': 'Bearer ' + self.get_token() + '',
                'Content-Type': 'application/json'
            }
        else:
            self.log.error('{} env does not exist'.format(self.sf_env))
            raise Exception('{} env does not exist'.format(self.sf_env))

    '''---------Update-------------------'''

    def get_jwt(self):
        self.log.info('fnc: {}'.format(inspect.getframeinfo(inspect.currentframe()).function))
        key_file = ''
        issuer = ''
        subject = ''
        aud = ''
        claim = {}
        assertion = ''
        if self.sf_env == 'config1':
            key_file = self.env_config.config_key_file()
            # client id
            issuer = self.env_config.config_issuer()
            subject = self.env_config.config_subject()
            aud = self.env_config.config_audience()
            # *******************************************************
        else:
            key_file = self.env_config.key_file()
            # client id
            issuer = self.env_config.issuer()
            subject = self.env_config.subject()
            aud = self.env_config.audience()
            # *******************************************************
        # Load private key
        with open(key_file) as fd:
            private_key = fd.read()
        # Generate signed JWT assertion
        claim = {
            'iss': issuer,
            'exp': int(time.time()) + 300,
            'aud': aud,
            'sub': subject,
        }
        assertion = jwt.encode(claim, private_key, algorithm='RS256', headers={'alg': 'RS256'})
        return assertion

    def get_token(self):
        self.log.info('fnc: {}'.format(inspect.getframeinfo(inspect.currentframe()).function))
        assertion = self.get_jwt()
        # JWT flow
        auth_params = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': assertion,
        }
        resp = requests.post(self.base_url + 'oauth2/token', params=auth_params,
                             verify=False)
        json_res = resp.json()
        if json_res['access_token']:
            self.log.info('Successful authentication')
            return json_res['access_token']
        else:
            self.log.error('Could not get access token: {}'.format(json_res))
            return json_res

    # SF API request to get icp data using the icp number
    def get_data(self, var):
        self.log.info('fnc: {}'.format(inspect.getframeinfo(inspect.currentframe()).function))
        try:
            resp = requests.get(
                self.base_url + 'data/v40.0/sobjects/object/Name/{}/'.format(var),
                headers=self.headers,
                verify=False)
        except Exception as e:
            self.log.info(f"{e}")
        else:
            return resp
