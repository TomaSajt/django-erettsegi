from django.db import models
from datetime import datetime




class Tudos(models.Model):

    azon = models.IntegerField()
    nev = models.CharField(max_length=64)
    terulet = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Tudós"
        verbose_name_plural = "Tudosok"

    def __str__(self):
        return self.nev

    def feltolt(lines):
        return 1,None



class Eloadas(models.Model):

    azon = models.IntegerField()
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
            print(split[0])

            if len(split) != 3:
                return cnt, f"Hiba a(z) {i+1}. rekordban. Nem megfelelő tabulátorszám!"

            try:
                azon = int(split[0])
            except:
                return cnt, f"Hiba a(z) {i+1} rekordban. Az 1. mezőben egész számot kell megadni!"

            try:
                ido = datetime.strptime(split[2],"%Y.%m.%d").date()
            except:
                return cnt, f"Hiba a(z) {i+1} rekordban. Az 3. mezőben rossz formátumban van megadva a dátum"
                
            
            _, created = Eloadas.objects.get_or_create(
                azon = azon,
                cim = split[1],
                ido = ido,
            )

            if created:
                cnt += 1
                
        return cnt, None

    def feltolt_kapcsolat(lines):
        return 1,None

