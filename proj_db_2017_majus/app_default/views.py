from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError
from django.db.models import Count
from .models import Tudos, Eloadas

def index(request):
    return render(request,'index.html',{})

def feltolt(request, table):
    if(table not in [ 'tudos', 'eloadas', 'kapcsolo' ]):
        raise Exception("Nincs ilyen nevű tábla")

    if(request.method != 'POST'):
        return render(request, 'feltolt.html',{ "table": table })

    try:
        contents = request.POST['contents']
    except:
        return HttpResponseServerError("Meg kell adni a 'contents' mezőt!")

    lines = contents.replace('\r\n', '\n').split('\n')
    lines = lines[1:]
    if lines[-1] == "":
        lines = lines[0:-1]

    feltolt = Tudos.feltolt if table == "tudos" else Eloadas.feltolt if table == "eloadas" else Eloadas.feltolt_kapcsolo
    db, err = feltolt(lines)

    if err:
        return HttpResponseServerError(f"Feltöltve {db} rekord, azonban hiba történt: {err}")
        
    return HttpResponse(f"Sikeresen feltöltve {db} rekord.")


def feladat2(request):
    return render(request, 'feladat2.html', {
        'eloadasok': (e for e in Eloadas.objects.order_by('cim') if e.ido.year == 2006),
    })

def feladat3(request):
    return render(request, 'feladat3.html', {
        'eloadasok': (e for e in Eloadas.objects.all() if "nyelv" in e.cim),
    })

def feladat4(request):
    return render(request, 'feladat4.html', {
        'adatok': Tudos.objects.values('terulet').annotate(db=Count('terulet')).order_by('-db'),
    })

def feladat5(request):
    return render(request, 'feladat5.html', {
        'tudosok': (t for t in Tudos.objects.all() if t.eloadas_set.count() > 1),
    })

def feladat6(request):
    ido = Eloadas.objects.get(cim='Mit tud az emberi agy?').ido
    return render(request, 'feladat6.html', {
        'eloadasok': (e for e in Eloadas.objects.all() if e.ido.year == ido.year and e.ido.month == ido.month),
    })