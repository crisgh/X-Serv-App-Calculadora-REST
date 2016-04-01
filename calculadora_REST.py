#!/usr/bin/python

import webapp
import sys

class Calculadora_REST(webapp.webApp):

    def parse(self, request):
        metodo = request.split(' ', 2)[0]
        operacion = request.split(' ', 2)[1]
        cuerpo = request.split('\r\n\r\n')[1];

        return (metodo, operacion , cuerpo)

    def process(self, parsedRequest):
        metodo,operacion,cuerpo = parsedRequest

        if metodo == "PUT":
            httpCode = "200 OK"
            oper1 = cuerpo.split(' ', 2)[0]
            signo = cuerpo.split(' ', 2)[1]
            oper2 = cuerpo.split(' ', 2)[2]

            if signo == "+":
                self.resultado = str(int(oper1) + int(oper2))
                htmlBody = "<html><body><h1> " + oper1 + " + " + oper2 + " = " \
                            + self.resultado + " </h1></body></html>"
            elif signo == "-":
                self.resultado = str(int(oper1) - int(oper2))
                htmlBody = "<html><body><h1> " + oper1 + " - " + oper2 + " = " \
                            + self.resultado + " </h1></body></html>"
            elif signo == "*":
                self.resultado = str(int(oper1) * int(oper2))
                htmlBody = "<html><body><h1> " + oper1 + " * " + oper2 + " = " \
                            + self.resultado + " </h1></body></html>"
            elif signo == "/":
                self.resultado = str(int(oper1) / int(oper2))
                htmlBody = "<html><body><h1> " + oper1 + " / " + oper2 + " = " \
                            + self.resultado + " </h1></body></html>"

        elif metodo == "GET":
            try:
                httpCode = "200 OK"
                htmlBody = "<html><body><h1> " + 'Solucion: '+ self.result + " </h1></html></body>"
            except ValueError:
                return ("404 Not Found","<html><body>Error: ValueError</body></html>")
            except AttributeError:
                return ("404 Not Found","<html><body>Error: AttributeError</body></html>")
        else:
            httpCode = "405 Method not allowed"
            htmlBody = "<html><body><h1> " +'Solo metodos PUT o GET.'+ " </h1></html></body>"

        return (httpCode, htmlBody)

if __name__ == '__main__':
    try:
        calc = Calculadora_REST("localhost", 2312)
    except KeyboardInterrupt:
        print "Servidor Cerrado"
        sys.exit()
