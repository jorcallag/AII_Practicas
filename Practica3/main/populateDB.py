from main.models import Puntuacion, Anime, Genero
from datetime import datetime

path = "data"

def populate():
    a = populateAnimes()
    populateRatings(a)
    

def populateAnimes():
    Anime.objects.all().delete()
    
    lista_animes = []
    dict_categorias = {}
    fileobj=open("C:\\Users\\Jorlu\\Desktop\\WS\\AII\\Practica3\\data\\anime.txt", "r") #Aqui debe de aparecer el path completo del archivo
    for line in fileobj.readlines()[1:]:
        rip = line.strip().split('\t')
        
        if rip[4] == 'Unknown':
            rip[4] = 0
            
        
        lista_animes.append(Anime(idAnime=rip[0], titulo=rip[1], formato=rip[3], nEpisodios=rip[4]))
        
        lista_aux=[]
        for genero in rip[2].split(', '):
            if not Genero.objects.filter(nombre=genero).exists():
                Genero.objects.create(nombre=genero)
            lista_aux.append(Genero.objects.get(pk = genero))
            
        dict_categorias[rip[0]]=lista_aux
    fileobj.close()    
    Anime.objects.bulk_create(lista_animes)

    dict={} 
    for anime in Anime.objects.all():
        anime.generos.set(dict_categorias[anime.idAnime])
        dict[anime.idAnime]=anime

    return(dict)

def populateRatings(a):
    Puntuacion.objects.all().delete()

    lista=[]
    fileobj=open("C:\\Users\\Jorlu\\Desktop\\WS\\AII\\Practica3\\data\\ratings.txt", "r") #Aqui debe de aparecer el path completo del archivo
    for line in fileobj.readlines()[1:]:
        rip = str(line.strip()).split('\t')
        lista.append(Puntuacion(idUsuario=rip[0], idAnime=a[rip[1]], puntuacion=rip[2]))
    fileobj.close()
    Puntuacion.objects.bulk_create(lista)


