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
    MAPPING_CHOICES = (
        ('substrings',	'scoring based on a fixed number of substrings'),
        ('yes/no',	'scoring based on simple yes or no'),
        ('keywords', 'scoring based on a fixed number of keywords'),
        ('composite_count',	'options varries from No to More than 1'),
        ('multifield_substring', 'one that combines data from 2 or more fields based on substrings'),
        ('range_based', 'options have some kind of range of values, e.g. distance 50-100 metre, 100-200 metre')
    )
    question = models.CharField(max_length=200)
    parent_category = models.ForeignKey("ranking.Category", on_delete=models.CASCADE)
    directly_mappable = models.BooleanField(default=True)
    scoring_method = models.CharField(choices=MAPPING_CHOICES, max_length=200, default='substrings')
    map_to_field_1 = models.CharField(max_length=200)
    map_to_field_2 = models.CharField(max_length=200, null=True, blank=True)
    map_to_model = models.CharField(max_length=500)
    weight = models.DecimalField(max_digits=6, decimal_places=3)
    calculated_value = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.question

class Answer(models.Model):
    ANSWER_TYPES_CHOICES = (
        ('substring', 'answer should be derived from substring of the field data'),
        ('code_mapping', 'certain coding mechanism in the data, e.g. number codes mentioned in data for different answer options'),
        ('time_range_from_substring', 'time range need to be derived from substring of the field'),
        ('count_from_substring', 'count need to be derived from substring of the field'),
        ('complex_calculation',	'involves a number of factors ans fields to find the score')
    )
    answer_choice = models.CharField(max_length=100)
    parent_question = models.ForeignKey("ranking.Question", on_delete=models.CASCADE)
    answer_types = models.CharField(choices=ANSWER_TYPES_CHOICES, max_length=200, default='substrings')
    weight = models.DecimalField(max_digits=6, decimal_places=3)
    calculated_value = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.answer_choice