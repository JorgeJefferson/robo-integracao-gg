import requests
from bs4 import BeautifulSoup


class LoginService:
    @staticmethod
    def obter_pagina_login(session, login_url):
        response = session.get(login_url)
        return response.text

    @staticmethod
    def capturar_campos_ocultos(response_text, data=None):
        if data is None:
            data = {}

        soup = BeautifulSoup(response_text, "html.parser")

        # Capturar campos ocultos
        viewstate_elem = soup.find("input", {"name": "__VIEWSTATE"})
        viewstategenerator_elem = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})
        eventvalidation_elem = soup.find("input", {"name": "__EVENTVALIDATION"})

        if value := viewstate_elem.get("value") if viewstate_elem else None:  # type: ignore
            data["__VIEWSTATE"] = value
        if value := (
            viewstategenerator_elem.get("value") if viewstategenerator_elem else None  # type: ignore
        ):
            data["__VIEWSTATEGENERATOR"] = value
        if value := eventvalidation_elem.get("value") if eventvalidation_elem else None:  # type: ignore
            data["__EVENTVALIDATION"] = value

        return data

    @staticmethod
    def preparar_dados_login(data, email, senha):
        return {
            **data,
            "ctl00$txtEmail": email,
            "ctl00$txtSenha": senha,
            "ctl00$btnEntrar": "ENTRAR NO SISTEMA",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
        }

    @staticmethod
    def logar(session, login_url, login_data):
        response = session.post(login_url, data=login_data)
        return response
