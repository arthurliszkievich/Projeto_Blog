from .models import SiteSetup


class SiteSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Código a ser executado para cada requisição ANTES da view

        # Busca a primeira (e única) instância de SiteSetup
        # Usamos o .first() para não dar erro se a tabela estiver vazia
        print('--- MIDDLEWARE EXECUTADO! ---')
        setup = SiteSetup.objects.first()
        print(f'--- Middleware encontrou: {setup} ---')

        # Anexa o objeto de setup ao objeto request
        request.site_setup = setup

        response = self.get_response(request)

        # Código a ser executado DEPOIS da view (não precisamos aqui)

        return response
