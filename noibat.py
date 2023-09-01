import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Substitua pelas suas credenciais do Spotify for developers
CLIENT_ID = 'Client ID'
CLIENT_SECRET = 'Client Secret'

# Autenticação na API do Spotify
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def media(notas):
    if len(notas) == 0:
        return 0
    return sum(notas) / len(notas)

def main():
    nome_artista = input("Digite o nome do artista: ")
    
    resultados = sp.search(q=nome_artista, type='artist', limit=1)
    if not resultados['artists']['items']:
        print("Artista não encontrado.")
        return
    
    artista = resultados['artists']['items'][0]
    
    albuns = sp.artist_albums(artista['id'], album_type='album', limit=50)
    
    avaliacoes = {}
    
    for album in albuns['items']:
        nome_album = album['name']
        album_tracks = sp.album_tracks(album['id'])
        
        notas = []
        print(f"\nAvalie as músicas do álbum '{nome_album}' de 0 a 10:")
        
        for track in album_tracks['items']:
            print(f"{track['name']}: ", end='')
            nota = int(input())
            notas.append(nota)
        
        media_album = media(notas)
        avaliacoes[nome_album] = media_album
    
    albums_ordenados = sorted(avaliacoes, key=avaliacoes.get, reverse=True)
    
    print("\nRanking dos álbuns:")
    for index, nome_album in enumerate(albums_ordenados, start=1):
        print(f"{index}. {nome_album} - {avaliacoes[nome_album]:.2f}")

if __name__ == "__main__":
    main()
