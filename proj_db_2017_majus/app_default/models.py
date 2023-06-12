from django.db import models
from datetime import datetime


class Tudos(models.Model):

    id = models.IntegerField(primary_key=True)
    nev = models.CharField(max_length=64)
    terulet = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Tudós"
        verbose_name_plural = "Tudosok"

    def __str__(self):
        return self.nev

    def feltolt(lines):
        cnt = 0
        for i, line in enumerate(lines):
            split = line.split('\t')

            if len(split) != 3:
                return cnt, f"Hiba a(z) {i+1}. rekordban. Nem megfelelő tabulátorszám!"

            try:
                id = int(split[0])
            except:
                return cnt, f"Hiba a(z) {i+1} rekordban. Az 1. mezőben egész számot kell megadni!"

            _, created = Tudos.objects.get_or_create(
                id = id,
                nev = split[1],
                terulet = split[2],
            )
            if created:
                cnt += 1
                
        return cnt, None



class Eloadas(models.Model):

    id = models.IntegerField(primary_key=True)
    cim = models.CharField(max_length=256)
    ido = models.DateField()
    tudosok = models.ManyToManyField(Tudos)
    

    class Meta:
        verbose_name = "Előadás"
        verbose_name_plural = "Előadások"

    def __str__(self):
        return self.cim

    def feltolt(lines):
        Eloadas.objects.all().delete()
        cnt = 0
        for i, line in enumerate(lines):
            split = line.split('\t')

            if len(split) != 3:
                return cnt, f"Hiba a(z) {i+1}. rekordban. Nem megfelelő tabulátorszám!"

            try:
                id = int(split[0])
            except:
                return cnt, f"Hiba a(z) {i+1} rekordban. Az 1. mezőben egész számot kell megadni!"

            try:
                ido = datetime.strptime(split[2],"%Y.%m.%d").date()
            except:
                return cnt, f"Hiba a(z) {i+1} rekordban. A 3. mezőben rossz formátumban van megadva a dátum"
                
            
            _, created = Eloadas.objects.get_or_create(
                id = id,
                cim = split[1],
                ido = ido,
            )
            if created:
                cnt += 1
                
        return cnt, None

    def feltolt_kapcsolo(lines):
        cnt = 0
        for i, line in enumerate(lines):
            split = line.split('\t')

            if len(split) != 2:
                return cnt, f"Hiba a(z) {i+1}. rekordban. Nem megfelelő tabulátorszám!"

            try:
                tudos_id = int(split[0])
            except:
                return cnt, f"Hiba a(z) {i+1} rekordban. Az 1. mezőben egész számot kell megadni!"
            
            try:
                tudos = Tudos.objects.get(id=tudos_id)
            except:
                return cnt, f"Hiba a(z) {i+1} rekordban. Nem található ilyen azonosítójú tudós!"

            try:
                eloadas_id = int(split[1])
            except:
                return cnt, f"Hiba a(z) {i+1} rekordban. A 2. mezőben egész számot kell megadni!"
            
            try:
                eloadas = Eloadas.objects.get(id=eloadas_id)
            except:
                return cnt, f"Hiba a(z) {i+1} rekordban. Nem található ilyen azonosítójú előadás!"

            if not eloadas.tudosok.filter(id=tudos_id).exists():
                eloadas.tudosok.add(tudos)
                eloadas.save()
                cnt += 1

                
        return cnt, None

