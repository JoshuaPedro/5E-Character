# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 21:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rules', '0001_initial'),
        ('character', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spells', '0001_initial'),
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classlevel',
            name='char_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classlevels', to='rules.Class'),
        ),
        migrations.AddField(
            model_name='classlevel',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classlevels', to='character.Character'),
        ),
        migrations.AddField(
            model_name='character',
            name='alignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_alignments', to='rules.Alignment'),
        ),
        migrations.AddField(
            model_name='character',
            name='armor_inv',
            field=models.ManyToManyField(blank=True, related_name='character_armor_inv', to='equipment.Armor'),
        ),
        migrations.AddField(
            model_name='character',
            name='char_background',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='rules.Background'),
        ),
        migrations.AddField(
            model_name='character',
            name='char_classes',
            field=models.ManyToManyField(related_name='characters', through='character.ClassLevel', to='rules.Class'),
        ),
        migrations.AddField(
            model_name='character',
            name='char_race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='rules.Race'),
        ),
        migrations.AddField(
            model_name='character',
            name='conditions',
            field=models.ManyToManyField(blank=True, related_name='character_conditions', to='rules.Condition'),
        ),
        migrations.AddField(
            model_name='character',
            name='features',
            field=models.ManyToManyField(related_name='character_features', to='rules.Feature'),
        ),
        migrations.AddField(
            model_name='character',
            name='items_inv',
            field=models.ManyToManyField(blank=True, related_name='character_items_inv', to='equipment.Item'),
        ),
        migrations.AddField(
            model_name='character',
            name='spell_book',
            field=models.ManyToManyField(blank=True, related_name='character_spells', through='character.SpellsReady', to='spells.Spell'),
        ),
        migrations.AddField(
            model_name='character',
            name='tools_inv',
            field=models.ManyToManyField(blank=True, related_name='character_tools_inv', to='equipment.Tool'),
        ),
        migrations.AddField(
            model_name='character',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='character',
            name='weapons_inv',
            field=models.ManyToManyField(blank=True, related_name='character_weapons_inv', to='equipment.Weapon'),
        ),
    ]
