from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError
from .models import Tudos, Eloadas

def index(request):
    return render(request,'index.html',{})

def feltoltes(request, table):
    if(table not in [ 'tudos', 'eloadas', 'kapcsolat' ]):
        raise Exception("Nincs ilyen nevű tábla")

    if(request.method != 'POST'):
        return render(request, 'feltoltes.html',{ "table": table })

    try:
        contents = request.POST['contents']
    except:
        return HttpResponseServerError("Meg kell adni a 'contents' mezőt!")

    lines = contents.replace('\r\n', '\n').split('\n')
    lines = lines[1:]
    if lines[-1] == "":
        lines = lines[0:-1]

    feltolt = Tudos.feltolt if table == "tudos" else Eloadas.feltolt if table == "eloadas" else Eloadas.feltolt_kapcsolat
    db, err = feltolt(lines)

    if err:
        return HttpResponseServerError(f"Sikeresen feltöltve {db} rekord. Azonban hiba történt: {err}")
        
    return HttpResponse(f"Sikeresen feltöltve {db} rekord.")


def feladat2(request):
    return render(request, 'feladat2.html', {
        'eloadasok': [e for e in Eloadas.objects.order_by('cim') if e.ido.year == 2006],
    })