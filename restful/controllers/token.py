# Part of odoo. See LICENSE file for full copyright and licensing details.
import json
import logging

import werkzeug.wrappers

from odoo import http
from odoo.addons.restful.common import invalid_response, valid_response
from odoo.http import request
from odoo.exceptions import AccessError, AccessDenied

_logger = logging.getLogger(__name__)

expires_in = "restful.access_token_expires_in"


class AccessToken(http.Controller):
    """."""

    def __init__(self):

        self._token = request.env["api.access_token"]
        self._expires_in = request.env.ref(expires_in).sudo().value
        
    @http.route('/api/token', type='json', auth="public")
    def get_api_token(self, **kw):
        """The token URL to be used for getting the access_token:

        Args:
            **post must contain login and password.
        Returns:

            returns https response code 404 if failed error message in the body in json format
            and status code 202 if successful with the access_token.
        Example:
           import requests

           headers = {'content-type': 'text/plain', 'charset':'utf-8'}

           data = {
               'login': 'admin',
               'password': 'admin',
               'db': 'galago.ng'
            }
           base_url = 'http://odoo.ng'
           eq = requests.post(
               '{}/api/auth/token'.format(base_url), data=data, headers=headers)
           content = json.loads(req.content.decode('utf-8'))
           headers.update(access-token=content.get('access_token'))
        """
        _token = request.env["api.access_token"]
        db = kw.get('db')
        username = kw.get('login')
        password = kw.get('password')

        _credentials_includes_in_body = all([db, username, password])
        if not _credentials_includes_in_body:
            # The request post body is empty the credetials maybe passed via the headers.
            headers = request.httprequest.headers
            db = headers.get("db")
            username = headers.get("login")
            password = headers.get("password")
            _credentials_includes_in_headers = all([db, username, password])
            if not _credentials_includes_in_headers:
                # Empty 'db' or 'username' or 'password:
                return invalid_response(
                    "missing error", "either of the following are missing [db, username,password]", 403,
                )
        # Login in odoo database:
        try:
            request.session.authenticate(db, username, password)
        except AccessError as aee:
            return invalid_response("Access error", "Error: %s" % aee.name)
        except AccessDenied as ade:
            return invalid_response("Access denied", "Login, password or db invalid")
        except Exception as e:
            # Invalid database:
            info = "The database name is not valid {}".format((e))
            error = "invalid_database"
            _logger.error(info)
            return invalid_response("wrong database name", error, 403)

        uid = request.session.uid
        # odoo login failed:
        if not uid:
            info = "authentication failed"
            error = "authentication failed"
            _logger.error(info)
            return invalid_response(401, error, info)

        # Generate tokens
        access_token = _token.find_one_or_create_token(user_id=uid, create=True)
        request_value = []
        request_value.append({
            "uid": uid,
            "user_context": request.session.get_context() if uid else {},
            "company_id": request.env.user.company_id.id if uid else None,
            "company_ids": request.env.user.company_ids.ids if uid else None,
            "partner_id": request.env.user.partner_id.id,
            "access_token": access_token,
            #             "expires_in": self._expires_in,
        })

        request.params['request_value'] = request_value
        print(request.params)
        return request.params