from django.db import models

class Theme(models.Model):
    name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=6, decimal_places=3)
    calculated_value = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_theme = models.ForeignKey("ranking.Theme", on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=3)
    calculated_value = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    question = models.CharField(max_length=200)
    parent_category = models.ForeignKey("ranking.Category", on_delete=models.CASCADE)
    mappable = models.BooleanField(default=True)
    map_to_field = models.CharField(max_length=200)
    map_to_model = models.CharField(max_length=500)
    weight = models.DecimalField(max_digits=6, decimal_places=3)
    calculated_value = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.question

class Answer(models.Model):
    answer_choice = models.CharField(max_length=100)
    parent_question = models.ForeignKey("ranking.Question", on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=3)
    calculated_value = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.answer_choice