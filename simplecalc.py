#!/usr/bin/python

#
# Simple calculator: add, subs, mult, div
# Can only perform one operation "at a time"
# (well, one of each of the operations"
#
# Copyright Jesus M. Gonzalez-Barahona 2009
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# October 2009
#

import webappmulti
import urlparse

def decorateHTML (text):

    return ("<html><body>" + text + "</body></html>")

class operation (webappmulti.app):
    """Void class for all operations (sum, sub, mul, div)
    Acts when receiving the following HTTP requests:
     - PUT (arguments in body, as query string): performs the operation
            (and returns the result of the operation)

         #

     - GET: returns the result of the operation
    Methods operate and sign should be overidden by children classes
    """

    def operate (self, oper1, oper2):
        """Placeholder operation, to be extended by children of this class.
        Returns the value of applying it to oper1, oper2."""

        return None

    def sign (self):
        """Placeholder operation, to be extended by children of this class.
        Returns the sign of the operation."""

        return None

    def parse (self, request, rest):

        verb = request.split(' ',1)[0]
        parts = request.split('\r\n\r\n',1)
        if len (parts) == 2:
            body = parts[1]
        else:
            body = ""
        return (verb, body)

    def process (self, (verb, body)):

        if verb == 'PUT':
            params = urlparse.parse_qs(body)  # nos dice lo que viene en el cuerpo
            # buscar modulo python  urlparse.parse_qs
            try:
                self.oper1 = int(params['oper1'][0]) # cogemos el elemento (1º)
                self.oper2 = int(params['oper2'][0]) # cogemos el elemento (2º)
                self.result = self.operate (self.oper1, self.oper2) # calculamos el estado del recurso
                success = True
                # params :  diccionario como ua lista -- nos quedamos con el primer
                # elemento de la lista o el segundo
            except:
                success = False # Fallos en los parametros
                (error, message) = ("400 Error",
                                    "Error in parameters for operation")
        elif verb == 'GET':
            success = True
        else: # cuando el verbo no es ni GET ni PUT
            success = False
            (error, message) = ("400 Error",
                                "HTTP verb " + verb + " not supported")

        if success:
            return ("200 OK", decorateHTML(str(self.oper1) + self.sign() +
                                           str(self.oper2) +
                                           "=" + str(self.result)))
        else:
            return (error, decorateHTML(message))

    def __init__ (self):

        self.oper1 = 0
        self.oper2 = 0
        self.result = 0

class add (operation):
    def operate (self, oper1, oper2):

        return oper1 + oper2

    def sign (self):

        return '+'

class sub (operation):
    def operate (self, oper1, oper2):

        return oper1 - oper2

    def sign (self):

        return '-'

class mul (operation):
    def operate (self, oper1, oper2):

        return oper1 * oper2

    def sign (self):

        return '*'

class div (operation):
    def operate (self, oper1, oper2):

        return oper1 / oper2

    def sign (self):

        return '/'

if __name__ == "__main__":
    addObj = add()
    subObj = sub()
    mulObj = mul()
    divObj = div()
    multiCalc = webappmulti.webApp ("localhost", 1234,
                                    {'/add': addObj,
                                     '/sub': subObj,
                                     '/mul': mulObj,
                                     '/div': divObj,})
