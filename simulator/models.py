from django.db import models


class Simulator(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()  
    interval = models.DurationField()    
    formula = models.TextField()         

    def __str__(self):
        return self.name


class KPI(models.Model):
    name = models.CharField(max_length=100)
    simulator = models.ForeignKey(Simulator, null=True, blank=True, on_delete=models.CASCADE, related_name='kpis')
    formula = models.TextField()  
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
