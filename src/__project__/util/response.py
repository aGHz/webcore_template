import json
from web.core.http import WSGIHTTPException
from webob.response import Response

__all__ = ['TEMPLATE', 'SUCCESS', 'FAILURE',
           'APIException',
           'APIBadRequest', 'APIUnauthorized', 'APIForbidden', 'APINotFound', 'APIConflict',
           'APIInternalServerError', 'APINotImplemented', 'APIBadGateway',
           ]


def TEMPLATE(name, data={}):
    return ('./usr/templates/{name}.html'.format(name=name), data)

def SUCCESS(result=''):
    return ('json:', {'status': 'success', 'result': result})

def FAILURE(error='', data=None):
    return ('json:', {'status': 'error', 'error': error, 'result': data})


class APIException(WSGIHTTPException):
    def json_body(self, environ):
        """ application/json representation of the exception """
        return unicode(json.dumps({
            'status': 'error',
            'error': '%s %s' % (getattr(self, 'real_code', self.code), self.title),
            'result': self.detail
            }))

    def plain_body(self, environ):
        """ text/plain representation of the exception """
        return unicode(self.detail)

    def generate_response(self, environ, start_response):
        if self.content_length is not None:
            del self.content_length
        headerlist = list(self.headerlist)
        accept = environ.get('HTTP_ACCEPT', '')
        if accept and 'json' in accept or '*/*' in accept:
            content_type = 'application/json'
            body = self.json_body(environ)
        else:
            content_type = 'text/plain'
            body = self.plain_body(environ)
        extra_kw = {}
        if isinstance(body, unicode):
            extra_kw.update(charset='utf-8')
        resp = Response(body,
            status=self.status,
            headerlist=headerlist,
            content_type=content_type,
            **extra_kw
        )
        resp.content_type = content_type
        return resp(environ, start_response)

    def __repr__(self):
        return '<%s %s; code=%s>' % (self.__class__.__name__,
                                     self.title, self.code)

class APIBadRequest(APIException):
    code = 400
    real_code = 400
    title = 'Bad Request'
    explanation = ('The server could not comply with the request since'
                   'it is either malformed or otherwise incorrect.')

class APIUnauthorized(APIException):
    code = 401
    real_code = 401
    title = 'Unauthorized'
    explanation = (
        'This server could not verify that you are authorized to'
        'access the document you requested.  Either you supplied the'
        'wrong credentials (e.g., bad password), or your browser'
        'does not understand how to supply the credentials required.')

class APIForbidden(APIException):
    code = 403
    real_code = 403
    title = 'Forbidden'
    explanation = ('Access was denied to this resource.')

class APINotFound(APIException):
    code = 404
    real_code = 404
    title = 'Not Found'
    explanation = ('The resource could not be found.')

class APIConflict(APIException):
    code = 409
    real_code = 409
    title = 'Conflict'
    explanation = ('There was a conflict when trying to complete '
                   'your request.')

class APIInternalServerError(APIException):
    code = 500
    real_code = 500
    title = 'Internal Server Error'
    explanation = (
      'The server has either erred or is incapable of performing\r\n'
      'the requested operation.\r\n')

class APINotImplemented(APIException):
    code = 501
    real_code = 501
    title = 'Not Implemented'
    explanation = ('The server does not support the functionality required to fulfill the request')

class APIBadGateway(APIException):
    code = 502
    real_code = 502
    title = 'Bad Gateway'
    explanation = (
        'The server, while acting as a gateway or proxy,'
        'received an invalid response from the upstream server'
        'it accessed in attempting to fulfill the request.')
