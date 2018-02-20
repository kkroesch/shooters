# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

class Organization(models.Model):
    """
    Represent an organisation, which can be everything from society to union.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = u'Verein'
        verbose_name_plural = u'Vereine'


class Shooter(models.Model):
    """
    Represents a shooter and is related to a certain user account.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='shooter', null=True, on_delete=models.DO_NOTHING)
    organization = models.ForeignKey(Organization, related_name='members', on_delete=models.DO_NOTHING)
    date_of_birth = models.DateField()
    license_number = models.CharField(max_length=32, null=True)

    is_supervisor = models.BooleanField(default=False, verbose_name=u'Schützenmeister')

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta():
        verbose_name = u'Schütze'
        verbose_name_plural = u'Schützen'


class Match(models.Model):
    """
    Represents a match or similar event.
    """
    name = models.CharField(max_length=255)
    organizer = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True)
    match_date = models.DateField()
    begins = models.TimeField(blank=True, null=True)
    ends = models.TimeField(blank=True, null=True)

    medal_limit = models.IntegerField(blank=True, null=True)

    supervisor = models.ForeignKey(Shooter, null=True, blank=True, verbose_name=u'Schützenmeister', on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s (%s)' % (self.name, self.match_date.isoformat())

    def get_absolute_url(self):
        return reverse('event', kwargs={'pk': self.id})

    class Meta():
        verbose_name_plural = u'Matches'
        ordering = ['-match_date']


class Participation(models.Model):
    """
    Holds participation for shooter on a certain match.
    """
    shooter = models.ForeignKey(Shooter, related_name='participations', on_delete=models.DO_NOTHING)
    match = models.ForeignKey(Match, related_name='participations', on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s nimmt teil am %s' % (self.shooter, self.match)

    class Meta():
        verbose_name = u'Teilnahme'
        verbose_name_plural = u'Teilnahmen'


class Result(models.Model):
    """
    Represents a result for a shooter on a match.
    """
    shooter = models.ForeignKey(Shooter, related_name='shooters', on_delete=models.DO_NOTHING)
    match = models.ForeignKey(Match, related_name='results', on_delete=models.DO_NOTHING)
    count = models.IntegerField()

    def earns_medal(self):
        return self.count >= self.match.medal_limit

    """ Implement ranking algorithm here
    def __cmp__(self, other):

    """

    def __str__(self):
        return '%s: %d' % (self.shooter, self.count)

    class Meta():
        verbose_name = u'Resultat'
        verbose_name_plural = u'Resultate'
