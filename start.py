from instagrapi import Client
from moviepy.editor import VideoFileClip
import requests
import os
from time import sleep

# Função para logar na conta do Instagram
def login_no_instagram(usuario, senha):
    cl = Client()
    cl.login(usuario, senha)
    return cl

# Função para obter os últimos 50 Reels postados por um usuário
def obter_reels(cliente, usuario_alvo, quantidade=50):
    user_id = cliente.user_id_from_username(usuario_alvo)
    user_medias = cliente.user_medias(user_id, amount=quantidade)
    reels = [media for media in user_medias if media.media_type == 2]  # Filtra para pegar apenas vídeos (Reels são vídeos)
    return reels

# Função para baixar um arquivo de mídia do URL
def baixar_midia(url, path):
    response = requests.get(url)
    with open(path, 'wb') as file:
        file.write(response.content)

# Função para repostar o Reels na sua conta
def repostar_reels(cliente, reels):
    reels_info = cliente.media_info(reels.pk)
    legenda = reels_info.caption_text
    video_url = reels_info.video_url
    video_path = "temp_video.mp4"
    thumbnail_path = "temp_thumbnail.jpg"
    
    # Baixar o vídeo
    baixar_midia(video_url, video_path)
    
    # Baixar a miniatura
    if reels_info.thumbnail_url:
        baixar_midia(reels_info.thumbnail_url, thumbnail_path)
    
    # Verificar se o vídeo foi baixado corretamente
    try:
        clip = VideoFileClip(video_path)
        # Verificar se o vídeo tem áudio
        if clip.audio is None:
            print("O vídeo não contém áudio.")
        clip.close()
        
        # Repostar o vídeo
        cliente.video_upload(video_path, legenda, thumbnail=thumbnail_path)
    finally:
        # Remover os arquivos temporários de vídeo e miniatura
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)

# Função principal
def principal():
    seu_usuario = 'fernanda.treinoss'
    sua_senha = '13579Adgjl@@'
    usuario_alvo = 'larissa.treinos'

    cliente = login_no_instagram(seu_usuario, sua_senha)
    reels_list = obter_reels(cliente, usuario_alvo, quantidade=50)

    for reels in reels_list:
        try:
            repostar_reels(cliente, reels)
            print(f'Repostado: {reels.pk}')
        except Exception as e:
            print(f'Ocorreu um erro ao repostar o Reels {reels.pk}: {e}')
        
        sleep(1500)  # Espera 25 minutos (1500 segundos) antes de postar o próximo Reels

if __name__ == "__main__":
    principal()
