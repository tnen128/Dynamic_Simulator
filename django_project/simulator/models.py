from django.db import models

class Simulator(models.Model):
    start_date = models.DateTimeField()
    interval = models.CharField(max_length=50)  # e.g., "2s", "5s"
    kpi_id = models.IntegerField()

class Kpi(models.Model):
    name = models.CharField(max_length=50)
    formula = models.CharField(max_length=255)  # Store as a Python expression (e.g., "value + 2")

    def calculate(self, value):
        return eval(self.formula.replace("value", str(value)))
