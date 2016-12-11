from __future__ import unicode_literals

from django.db import models


class StoreItem(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):  # __unicode__ on Python 2
        return "%s " % self.name


class ItemProperty(models.Model):
    property_name = models.CharField(max_length=200)
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.property_name

    def __str__(self):  # __unicode__ on Python 2
        return self.property_name + ' - ' + self.item.name


class PropertyValue(models.Model):
    value = models.CharField(max_length=200)
    ItemProperty = models.ForeignKey(ItemProperty, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.value


# Create your models here.

class Fact(models.Model):
    type = models.CharField(max_length=3, )
    mean = models.CharField(max_length=100, )
    value = models.CharField(max_length=2, )
    is_value = models.CharField(max_length=2, )
    cf = models.FloatField()

    def __unicode__(self):
        return self.id


class Rule(models.Model):
    left = models.CharField(max_length=50, )
    right = models.CharField(max_length=10, )
    cf = models.FloatField()

    def __unicode__(self):
        return self.id


class RightFactModel(models.Model):
    content = models.CharField(max_length=100)
    type = models.CharField(max_length=3)

    def __unicode__(self):
        return self.content


class RuleModel(models.Model):
    right = models.OneToOneField(
        RightFactModel,
        on_delete=models.CASCADE,
    )
    cf = models.FloatField()


class LeftFactModel(models.Model):
    rule_model = models.ForeignKey(RuleModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=100, )
    type = models.CharField(max_length=3, )

    def __unicode__(self):
        return self.content

