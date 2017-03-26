# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-26 19:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('spells', '0001_initial'),
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=1024)),
                ('examples', models.CharField(blank=True, max_length=512, null=True)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Background',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=10000)),
                ('gold_start', models.SmallIntegerField()),
                ('specials', models.CharField(blank=True, max_length=512, null=True)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('armor_starts', models.ManyToManyField(blank=True, related_name='background_armor_starts', to='equipment.Armor')),
            ],
        ),
        migrations.CreateModel(
            name='Bond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.CharField(max_length=1024)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=10000)),
                ('hit_die_size', models.SmallIntegerField(choices=[(4, 4), (6, 6), (8, 8), (10, 10), (12, 12), (20, 20), (100, 100)])),
                ('primary_ability_1', models.CharField(choices=[('Strength', 'Strength'), ('Dexterity', 'Dexterity'), ('Constitution', 'Constitution'), ('Intelligence', 'Intelligence'), ('Wisdom', 'Wisdom'), ('Charisma', 'Charisma')], max_length=16)),
                ('primary_ability_2', models.CharField(blank=True, choices=[('Strength', 'Strength'), ('Dexterity', 'Dexterity'), ('Constitution', 'Constitution'), ('Intelligence', 'Intelligence'), ('Wisdom', 'Wisdom'), ('Charisma', 'Charisma')], max_length=16, null=True)),
                ('saving_throw_1', models.CharField(choices=[('Strength', 'Strength'), ('Dexterity', 'Dexterity'), ('Constitution', 'Constitution'), ('Intelligence', 'Intelligence'), ('Wisdom', 'Wisdom'), ('Charisma', 'Charisma')], max_length=16)),
                ('saving_throw_2', models.CharField(blank=True, choices=[('Strength', 'Strength'), ('Dexterity', 'Dexterity'), ('Constitution', 'Constitution'), ('Intelligence', 'Intelligence'), ('Wisdom', 'Wisdom'), ('Charisma', 'Charisma')], max_length=16, null=True)),
                ('starting_gold', models.SmallIntegerField(blank=True, null=True)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
            },
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1024)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='DamageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=512)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='DragonAncestry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('description', models.CharField(max_length=1024)),
                ('breath_weapon_size', models.CharField(blank=True, max_length=128, null=True)),
                ('breath_weapon_save', models.CharField(blank=True, max_length=8, null=True)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('damage_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dragon_damage_type', to='rules.DamageType')),
            ],
            options={
                'verbose_name': 'Dragon Ancestry',
                'verbose_name_plural': 'Dragon Ancestries',
            },
        ),
        migrations.CreateModel(
            name='EnemyRace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('usual_location', models.CharField(blank=True, max_length=1024, null=True)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=10000)),
                ('is_proficiency', models.BooleanField(default=False)),
                ('is_choice', models.BooleanField(default=False)),
                ('changes_at_level', models.BooleanField(default=False)),
                ('ability_level', models.SmallIntegerField(blank=True, null=True)),
                ('grants_advantage', models.BooleanField(default=False)),
                ('choice_type', models.CharField(blank=True, max_length=128, null=True)),
                ('choices', models.CharField(blank=True, max_length=1024, null=True)),
                ('choice_amount', models.SmallIntegerField(blank=True, null=True)),
                ('action_type', models.CharField(blank=True, choices=[('Attack', 'Attack'), ('Cast', 'Cast a Spell'), ('Dash', 'Dash'), ('Disengage', 'Disengage'), ('Dodge', 'Dodge'), ('Help', 'Help'), ('Hide', 'Hide'), ('Ready', 'Ready'), ('Search', 'Search'), ('Use', 'Use an Object'), ('Action', 'Action'), ('Bonus', 'Bonus Action'), ('Reaction', 'Reaction'), ('Move', 'Move'), ('None', 'None')], max_length=64, null=True)),
                ('action_constraint_start', models.CharField(blank=True, max_length=128, null=True)),
                ('action_constraint_end', models.CharField(blank=True, max_length=128, null=True)),
                ('action_duration', models.CharField(blank=True, max_length=128, null=True)),
                ('action_distance', models.CharField(blank=True, max_length=128, null=True)),
                ('action_use_stat', models.CharField(blank=True, max_length=128, null=True)),
                ('action_uses_per_day', models.CharField(blank=True, max_length=128, null=True)),
                ('ability_to_change', models.CharField(blank=True, choices=[('Strength', 'Strength'), ('Dexterity', 'Dexterity'), ('Constitution', 'Constitution'), ('Intelligence', 'Intelligence'), ('Wisdom', 'Wisdom'), ('Charisma', 'Charisma')], max_length=32, null=True)),
                ('ability_change_amount', models.SmallIntegerField(blank=True, null=True)),
                ('stat_to_change', models.CharField(blank=True, choices=[('Speed', 'Speed'), ('AC', 'Armor Class'), ('Initiative', 'Initiative'), ('Age', 'Age'), ('Size', 'Size'), ('Rest', 'Long Rest Duration'), ('Sight', 'Sight'), ('Sight - Darkvision', 'Sight - Darkvision'), ('HP', 'Hit Points')], max_length=32, null=True)),
                ('stat_change_amount', models.SmallIntegerField(blank=True, null=True)),
                ('armor_prof', models.CharField(blank=True, choices=[('Heavy', 'Heavy Armor'), ('Medium', 'Medium Armor'), ('Light', 'Light Armor'), ('Shield', 'Shield')], max_length=32, null=True)),
                ('spell_choice_number', models.SmallIntegerField(blank=True, null=True)),
                ('spell_choice_level', models.SmallIntegerField(blank=True, null=True)),
                ('spell_choices_class_list', models.CharField(blank=True, max_length=512, null=True)),
                ('spell_known_constraint', models.CharField(blank=True, max_length=512, null=True)),
                ('damage_dice_number', models.SmallIntegerField(blank=True, null=True)),
                ('damage_dice_size', models.SmallIntegerField(blank=True, choices=[(4, 4), (6, 6), (8, 8), (10, 10), (12, 12), (20, 20), (100, 100)], null=True)),
                ('damage_dice_bonus', models.SmallIntegerField(blank=True, null=True)),
                ('spell_resistance', models.BooleanField(default=False)),
                ('prereq_ability', models.CharField(blank=True, choices=[('Strength', 'Strength'), ('Dexterity', 'Dexterity'), ('Constitution', 'Constitution'), ('Intelligence', 'Intelligence'), ('Wisdom', 'Wisdom'), ('Charisma', 'Charisma')], max_length=16, null=True)),
                ('prereq_ability_amount', models.SmallIntegerField(blank=True, null=True)),
                ('prereq_character_level', models.SmallIntegerField(blank=True, null=True)),
                ('prereq_class_level', models.SmallIntegerField(blank=True, null=True)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('condition_resistance', models.ManyToManyField(blank=True, related_name='feature_conditions', to='rules.Condition')),
                ('damage_resistance_type', models.ManyToManyField(blank=True, related_name='feature_damage_resistance_types', to='rules.DamageType')),
                ('damage_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feature_damage_types', to='rules.DamageType')),
            ],
        ),
        migrations.CreateModel(
            name='Flaw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.CharField(max_length=1024)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ideal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.CharField(max_length=1024)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='LandType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('circle_spells_3', models.ManyToManyField(blank=True, related_name='land_spells_3', to='spells.Spell')),
                ('circle_spells_5', models.ManyToManyField(blank=True, related_name='land_spells_5', to='spells.Spell')),
                ('circle_spells_7', models.ManyToManyField(blank=True, related_name='land_spells_7', to='spells.Spell')),
                ('circle_spells_9', models.ManyToManyField(blank=True, related_name='land_spells_9', to='spells.Spell')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=10000)),
                ('typical_speakers', models.CharField(max_length=512)),
                ('script', models.CharField(blank=True, max_length=512, null=True)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalityTrait',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.CharField(max_length=1024)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='PrestigeClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=10000)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('features', models.ManyToManyField(related_name='prestige_class_features', to='rules.Feature')),
            ],
            options={
                'verbose_name': 'Prestige Class',
                'verbose_name_plural': 'Prestige Classes',
            },
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=10000)),
                ('ability_score_1', models.CharField(max_length=16)),
                ('ability_score_1_bonus', models.SmallIntegerField(blank=True, null=True)),
                ('ability_score_2', models.CharField(blank=True, max_length=16, null=True)),
                ('ability_score_2_bonus', models.SmallIntegerField(blank=True, null=True)),
                ('age_adult', models.SmallIntegerField()),
                ('age_mortality', models.SmallIntegerField()),
                ('size', models.CharField(choices=[('Tiny', 'Tiny'), ('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large'), ('Huge', 'Huge'), ('Gargantuan', 'Gargantuan')], max_length=16)),
                ('typical_height_min', models.SmallIntegerField()),
                ('typical_height_max', models.SmallIntegerField()),
                ('typical_weight_min', models.SmallIntegerField()),
                ('typical_weight_max', models.SmallIntegerField()),
                ('speed', models.SmallIntegerField()),
                ('speed_special', models.CharField(blank=True, max_length=128, null=True)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('features', models.ManyToManyField(related_name='race_features', to='rules.Feature')),
                ('race_armor_starts', models.ManyToManyField(blank=True, related_name='race_armor_starts', to='equipment.Armor')),
                ('race_item_starts', models.ManyToManyField(blank=True, related_name='race_item_starts', to='equipment.Item')),
                ('race_tool_starts', models.ManyToManyField(blank=True, related_name='race_tool_starts', to='equipment.Tool')),
                ('race_weapon_starts', models.ManyToManyField(blank=True, related_name='race_weapon_starts', to='equipment.Weapon')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('associated_ability', models.CharField(choices=[('Strength', 'Strength'), ('Dexterity', 'Dexterity'), ('Constitution', 'Constitution'), ('Intelligence', 'Intelligence'), ('Wisdom', 'Wisdom'), ('Charisma', 'Charisma')], max_length=16)),
                ('description', models.CharField(max_length=10000)),
                ('example_tasks', models.CharField(blank=True, max_length=512, null=True)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Subrace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1024)),
                ('ability_score_1', models.CharField(choices=[('Strength', 'Strength'), ('Dexterity', 'Dexterity'), ('Constitution', 'Constitution'), ('Intelligence', 'Intelligence'), ('Wisdom', 'Wisdom'), ('Charisma', 'Charisma')], max_length=16)),
                ('ability_score_1_bonus', models.SmallIntegerField(blank=True, null=True)),
                ('ability_score_2', models.CharField(blank=True, choices=[('Strength', 'Strength'), ('Dexterity', 'Dexterity'), ('Constitution', 'Constitution'), ('Intelligence', 'Intelligence'), ('Wisdom', 'Wisdom'), ('Charisma', 'Charisma')], max_length=16, null=True)),
                ('ability_score_2_bonus', models.SmallIntegerField(blank=True, null=True)),
                ('srd', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('features', models.ManyToManyField(related_name='subrace_features', to='rules.Feature')),
                ('subrace_armor_starts', models.ManyToManyField(blank=True, related_name='subrace_armor_starts', to='equipment.Armor')),
                ('subrace_item_starts', models.ManyToManyField(blank=True, related_name='subrace_item_starts', to='equipment.Item')),
                ('subrace_tool_starts', models.ManyToManyField(blank=True, related_name='subrace_tool_starts', to='equipment.Tool')),
                ('subrace_weapon_starts', models.ManyToManyField(blank=True, related_name='subrace_weapon_starts', to='equipment.Weapon')),
            ],
        ),
        migrations.AddField(
            model_name='race',
            name='subraces',
            field=models.ManyToManyField(blank=True, related_name='race_subraces', to='rules.Subrace'),
        ),
        migrations.AddField(
            model_name='race',
            name='typical_alignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='race_alignment', to='rules.Alignment'),
        ),
        migrations.AddField(
            model_name='feature',
            name='languages_known',
            field=models.ManyToManyField(blank=True, related_name='feature_languages', to='rules.Language'),
        ),
        migrations.AddField(
            model_name='feature',
            name='prereq_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feature_prereq_class', to='rules.Class'),
        ),
        migrations.AddField(
            model_name='feature',
            name='prereq_prestige_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feature_prereq_prestige_class', to='rules.PrestigeClass'),
        ),
        migrations.AddField(
            model_name='feature',
            name='prereq_proficiency',
            field=models.ManyToManyField(blank=True, related_name='feature_prereq_proficiency', to='rules.Feature'),
        ),
        migrations.AddField(
            model_name='feature',
            name='prereq_race',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feature_prereq_race', to='rules.Race'),
        ),
        migrations.AddField(
            model_name='feature',
            name='prereq_subrace',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feature_prereq_subrace', to='rules.Subrace'),
        ),
        migrations.AddField(
            model_name='feature',
            name='skill_prof',
            field=models.ManyToManyField(blank=True, related_name='feature_skill_profs', to='rules.Skill'),
        ),
        migrations.AddField(
            model_name='feature',
            name='spell_choice',
            field=models.ManyToManyField(blank=True, related_name='feature_spell_choices', to='spells.Spell'),
        ),
        migrations.AddField(
            model_name='feature',
            name='spell_known',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feature_spell_known', to='spells.Spell'),
        ),
        migrations.AddField(
            model_name='feature',
            name='tool_prof',
            field=models.ManyToManyField(blank=True, related_name='feature_tool_profs', to='equipment.Tool'),
        ),
        migrations.AddField(
            model_name='feature',
            name='weapon_prof',
            field=models.ManyToManyField(blank=True, related_name='feature_weapon_profs', to='equipment.Weapon'),
        ),
        migrations.AddField(
            model_name='class',
            name='features',
            field=models.ManyToManyField(related_name='class_features', to='rules.Feature'),
        ),
        migrations.AddField(
            model_name='class',
            name='prestige_classes',
            field=models.ManyToManyField(blank=True, related_name='class_prestige_classes', to='rules.PrestigeClass'),
        ),
        migrations.AddField(
            model_name='class',
            name='starting_armor',
            field=models.ManyToManyField(blank=True, related_name='class_armor_starts', to='equipment.Armor'),
        ),
        migrations.AddField(
            model_name='class',
            name='starting_items',
            field=models.ManyToManyField(blank=True, related_name='classes_item_start', to='equipment.Item'),
        ),
        migrations.AddField(
            model_name='class',
            name='starting_tools',
            field=models.ManyToManyField(blank=True, related_name='classes_tool_start', to='equipment.Tool'),
        ),
        migrations.AddField(
            model_name='class',
            name='starting_weapons',
            field=models.ManyToManyField(blank=True, related_name='class_weapon_starts', to='equipment.Weapon'),
        ),
        migrations.AddField(
            model_name='background',
            name='features',
            field=models.ManyToManyField(blank=True, related_name='background_features', to='rules.Feature'),
        ),
        migrations.AddField(
            model_name='background',
            name='item_starts',
            field=models.ManyToManyField(blank=True, related_name='background_item_starts', to='equipment.Item'),
        ),
        migrations.AddField(
            model_name='background',
            name='languages',
            field=models.ManyToManyField(blank=True, related_name='background_languages', to='rules.Language'),
        ),
        migrations.AddField(
            model_name='background',
            name='suggested_bonds',
            field=models.ManyToManyField(blank=True, related_name='background_bonds', to='rules.Bond'),
        ),
        migrations.AddField(
            model_name='background',
            name='suggested_flaws',
            field=models.ManyToManyField(blank=True, related_name='background_flaws', to='rules.Flaw'),
        ),
        migrations.AddField(
            model_name='background',
            name='suggested_ideals',
            field=models.ManyToManyField(blank=True, related_name='background_ideals', to='rules.Ideal'),
        ),
        migrations.AddField(
            model_name='background',
            name='suggested_personality_traits',
            field=models.ManyToManyField(blank=True, related_name='background_personality_traits', to='rules.PersonalityTrait'),
        ),
        migrations.AddField(
            model_name='background',
            name='tool_starts',
            field=models.ManyToManyField(blank=True, related_name='background_tool_starts', to='equipment.Tool'),
        ),
        migrations.AddField(
            model_name='background',
            name='weapon_starts',
            field=models.ManyToManyField(blank=True, related_name='background_weapon_starts', to='equipment.Weapon'),
        ),
    ]
