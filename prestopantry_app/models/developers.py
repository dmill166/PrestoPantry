from django.db import models


class Developer(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    git_hub_link = models.CharField(max_length=200, null=True)
    linkedin_link = models.CharField(max_length=200, null=True)
    developer_about = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
