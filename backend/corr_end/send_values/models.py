from django.db import models

# Create your models here.
"""
# Sample post below
{
"experiment_name": "replicateSV21",
"row_num": "1",
"col_num": "1",
"row_label": "ENCFF415GFH",
"col_label": "ENCFF415GFH",
"corr_value": "1.0"
}
"""


class Link(models.Model):
    encode_url = models.CharField(max_length=1000)
    submitted_by = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ("encode_url",)

    def __unicode__(self):
        return self.encode_url


class Researcher(models.Model):
    name = models.CharField(
        max_length=512, blank=True, null=True, help_text="J. Michael Cherry"
    )
    institution = models.CharField(
        max_length=512, blank=True, null=True, help_text="Stanford University"
    )
    link = models.ForeignKey(
        Link,
        blank=True,
        null=True,
        related_name="researchers",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ("institution",)

    def __unicode__(self):
        return self.name


class Correlations(models.Model):
    experiment_name = models.CharField(max_length=100)
    row_num = models.PositiveIntegerField()
    col_num = models.PositiveIntegerField()
    row_label = models.CharField(max_length=100)
    col_label = models.CharField(max_length=100)
    corr_value = models.FloatField()

    class Meta:
        ordering = ("experiment_name",)

    def __unicode__(self):
        if not (
            self.experiment_name
            or self.row_num
            or self.col_num
            or self.row_label
            or self.col_label
            or self.corr_value
        ):
            return u"One or more of the fields is missing"
        else:
            return (
                u"Experiment Name: %s, Row Num: %d, Col Num: %d, Row Label: %s, Col Label: %s, Corr Value: %f"
                % (
                    self.experiment_name,
                    self.row_num,
                    self.col_num,
                    self.row_label,
                    self.col_label,
                    self.corr_value,
                )
            )


class Dinosaur(models.Model):
    age = models.PositiveIntegerField()
    species = models.TextField()
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        if not self.name:
            name_details = "No Name"
        else:
            name_details = self.name
        return "name %s " % [name_details]
