from django.db import models

# Create your models here.

class TreeMenu(models.Model):
    name            = models.CharField(unique=True, max_length=300)

    def __str__(self):
        return self.name

class TreeMenuItem(models.Model):
    public_name     = models.CharField(max_length=300)
    link            = models.CharField(max_length=100, blank=True)
    reverse_link    = models.BooleanField(default=False)
    sort_priority   = models.IntegerField()
    menu            = models.ForeignKey('TreeMenu', on_delete=models.CASCADE)
    parent_item     = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='children',
    )

    def __str__(self):
        return '%s:%s'%(self.menu.name, self.link)

            