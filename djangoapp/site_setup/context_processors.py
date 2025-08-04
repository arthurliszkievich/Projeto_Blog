def site_setup(request):
    print('--- CONTEXT PROCESSOR EXECUTADO! ---')
    # Usamos getattr para não dar erro caso o atributo não exista
    data = getattr(request, 'site_setup', 'ATRIBUTO NAO ENCONTRADO')
    print(f'--- Context processor recebeu: {data} ---')
    # ----------------------------------------

    return {
        'site_setup': request.site_setup
    }
