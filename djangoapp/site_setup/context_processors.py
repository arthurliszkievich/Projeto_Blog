from site_setup.models import SiteSetup


def site_setup(request):
    """
    Este context processor busca o objeto de configuração do site
    e o adiciona ao contexto de todos os templates.
    """
    # Busca o primeiro (e único) objeto SiteSetup do banco de dados
    setup = SiteSetup.objects.first()

    return {
        'site_setup': setup,
    }
