from pathlib import Path
import os
from django.conf import settings
from PIL import Image  # type: ignore


def resize_image(image_django, new_width=800, optimize=True, quality=60):
    """
    Redimensiona uma imagem mantendo a proporção e otimizando a qualidade.
    Salva a imagem sobre a original de forma segura.
    """
    # Pega o caminho completo da imagem
    image_path = Path(settings.MEDIA_ROOT / image_django.name).resolve()

    # Abre a imagem usando um gerenciador de contexto para garantir que seja fechada
    try:
        with Image.open(image_path) as img:
            original_width, original_height = img.size

            # Se a imagem já for pequena, não faz nada
            if original_width <= new_width:
                # Retorna o objeto de imagem original (já fechado pelo 'with')
                return img

            # Calcula a nova altura mantendo a proporção
            new_height = round(new_width * original_height / original_width)

            # Redimensiona a imagem com o filtro LANCZOS de alta qualidade
            new_image = img.resize(
                (new_width, new_height), Image.LANCZOS)  # type: ignore

            # Prepara os argumentos para salvar, dependendo do formato
            save_kwargs = {
                'optimize': optimize,
            }
            # O parâmetro 'quality' é mais relevante para JPEGs
            if img.format and img.format.lower() in ['jpeg', 'jpg']:
                save_kwargs['quality'] = quality  # type: ignore
                # Melhora o carregamento em navegadores
                save_kwargs['progressive'] = True

            # Salva a imagem no mesmo caminho, sobrescrevendo a original
            new_image.save(
                image_path,
                **save_kwargs  # type: ignore
            )

            return new_image

    except FileNotFoundError:
        # Lida com o caso de o arquivo de imagem não existir no disco
        # Você pode logar o erro ou simplesmente retornar None
        print(f"Erro: Arquivo não encontrado em {image_path}")
        return None
