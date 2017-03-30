"""
All the views that a user will see on the site.
"""
import pdb

# Python Imports:
import re, json


# Django Imports:
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView, CreateView
from django.urls import reverse_lazy
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound

from django.contrib import messages

# Module and Form Imports:
from .forms import SearchDatabase
from .forms import (AbilityScoresChoice, CCRace, CCClass, CCPersonality, CCBackground, CCEquipment, NCResolve,
                    ChoiceForm, BattleSheet)
from api.serializers import CharacterModelSerializer

# Model Imports:
from rules.models import (Alignment, Class, PrestigeClass, Race, Subrace, DamageType, Feature, Skill, Background,
                          Language, Condition, )
from rules import models as rules_models

from spells.models import Spell
from character.models import Character, ClassLevel, SpellsReady
from equipment.models import (Weapon, Armor, Tool, Item, MountAndVehicle)

from spells import models as spell_models
from rules import models as rule_models

from accounts.models import Member


def landing(request):

    context = dict()

    # messages.info(request, "Hello there! Welcome!")

    return render(request, 'landing.html', context)


def about_us(request):
    """
    Basic contact form for web page.
    """

    context = {'title': 'About Us!'}

    return render(request, 'company/about_us.html', context)


def report_issue(request):
    """
    Basic contact form for web page.
    """

    context = {'title': 'Report an Issue!'}

    return render(request, 'company/report_issue.html', context)


def search_home(request):
    """Shows the home search screen and allows the user to search for all the things."""

    if request.method == 'GET':
        query = ''
        results = dict()
        total = 0

    elif request.method == 'POST':
        models = (Spell, Weapon, Armor, Item, Tool, Feature, Class, Race, PrestigeClass, Subrace,
                  Skill, Alignment, DamageType, MountAndVehicle, Background, Language, Condition)
        results = dict()
        query = request.POST.get('query')
        total = 0

        for model in models:
            found = model.objects.filter(name__icontains=query)
            model_name = ' '.join(re.findall(r'[A-Z][a-z]+', str(model)))

            if found and model_name[-1] == 's':
                model_name += 'es'
                results[model_name] = list()
                for item in found:
                    results[model_name].append(item)
                    total += 1

            elif found and model_name[-1] != 's':
                model_name += 's'
                results[model_name] = list()
                for item in found:
                    results[model_name].append(item)
                    total += 1

    context = {'query': query, 'results': results, 'total': total}

    return render(request, 'database_view/search_home.html', context)

@login_required()
def character_sheet(request, username, slug):
    """Details for a user's character."""

    username = Member.objects.get(username__icontains=username)

    character = Character.objects.filter(username=username).filter(slug__icontains=slug)[0]

    if request.method == "GET":

        exp = r'(?<=: )\w*'

        skills = {re.findall(exp, feature.name)[0].lower(): True for feature in Feature.objects.filter(name__icontains='Skill: ')
                                                                             if feature in character.features.all()}
        battle_form = BattleSheet(initial={
            'STR': character.STR_score, 'DEX': character.DEX_score, 'CON': character.CON_score,
            'INT': character.INT_score, 'WIS': character.WIS_score, 'CHA': character.CHA_score,
            'STR_ST': character.STR_saving_throw, 'DEX_ST': character.DEX_saving_throw, 'CON_ST': character.CON_saving_throw,
            'INT_ST': character.INT_saving_throw, 'WIS_ST': character.WIS_saving_throw, 'CHA_ST': character.CHA_saving_throw,
            'ac': character.get_armor_class, 'init': character.get_initiative_bonus, 'speed': character.speed,
            'max_hp': character.max_health, 'cur_hp': character.current_health, 'temp_hp': character.temp_addtl_hp,
            'conditions': character.conditions.all(), 'spell_slots_1': character.spell_slots_1, 'spell_slots_2': character.spell_slots_2,
            'spell_slots_3': character.spell_slots_3, 'spell_slots_4': character.spell_slots_4, 'spell_slots_5': character.spell_slots_5,
            'spell_slots_6': character.spell_slots_6, 'spell_slots_7': character.spell_slots_7, 'spell_slots_8': character.spell_slots_8,
            'spell_slots_9': character.spell_slots_9, 'current_points': character.current_points, 'max_points': character.max_points,
            'acrobatics': skills.get('acrobatics', False), 'animal': skills.get('animal handling', False), 'arcana': skills.get('arcana', False),
            'athletics': skills.get('athletics', False),'deception': skills.get('deception', False), 'history': skills.get('history', False),
            'insight': skills.get('insight', False), 'intimidation': skills.get('intimidation', False), 'investigation': skills.get('investigation', False),
            'medicine': skills.get('medicine', False),'nature': skills.get('nature', False), 'perception': skills.get('perception', False),
            'performance': skills.get('performance', False),'persuasion': skills.get('persuasion', False), 'religion': skills.get('religion', False),
            'sleight': skills.get('sleight of hand', False),'stealth': skills.get('stealth', False), 'survival': skills.get('survival', False),
        })

        context = {'character': character, 'battle_form': battle_form}
        # import pdb;pdb.set_trace()
        if bool(character):
            return render(request, 'character_sheet/main.html', context)
        else:
            return HttpResponseNotFound("Sorry, we couldn't find your character!")


# Rule Detail Views:
def spell_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    spell = get_object_or_404(Spell, slug=slug)

    classes = list()
    for klass in spell.available_to.split(', '):
        if klass != '':
            classes.append(klass)

    context = {'result': spell, 'classes': classes, 'rit': spell.ritual, 'con': spell.concentration}

    return render(request, 'database_view/detail_pages/spell_details.html', context)


def subrace_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    subrace = get_object_or_404(Subrace, slug=slug)

    context = {'result': subrace, 'features': subrace.features.all(), 'parent': subrace.race_subraces.get()}

    return render(request, 'database_view/detail_pages/subrace_details.html', context)


def race_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    race = get_object_or_404(Race, slug=slug)

    context = {'result': race, 'features': race.features.all(), 'subraces': race.subraces.all()}

    return render(request, 'database_view/detail_pages/race_details.html', context)


def prestige_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    prestige = get_object_or_404(PrestigeClass, slug=slug)

    context = {'result': prestige, 'features': prestige.features.all(), 'parent': prestige.class_prestige_classes.get()}

    return render(request, 'database_view/detail_pages/prestige_details.html', context)


def class_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    klass = get_object_or_404(Class, slug=slug)

    pa2 = False
    if klass.primary_ability_2 != 'None':
        pa2 = True;

    context = {'result': klass, 'prestiges': klass.prestige_classes.all(), 'pa2': pa2, 'features': klass.features.all()}

    return render(request, 'database_view/detail_pages/class_details.html', context)


def feature_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    feature = get_object_or_404(Feature, slug=slug)

    parent = False
    search_type = None

    try:
        parent = feature.class_features.all()
        search_type = 'classes'
    except ObjectDoesNotExist:
        pass
    try:
        parent = feature.prestige_class_features.all()
        search_type = 'prestige_classes'
    except ObjectDoesNotExist:
        pass
    try:
        parent = feature.race_features.all()
        search_type = 'races'
    except ObjectDoesNotExist:
        pass
    try:
        parent = feature.subrace_features.all()
        search_type = 'subraces'
    except ObjectDoesNotExist:
        pass
    try:
        parent = feature.background_features.all()
        search_type = 'backgrounds'
    except ObjectDoesNotExist:
        pass

    context = {'result': feature, 'parent': parent, 'type': search_type}

    return render(request, 'database_view/detail_pages/feature_details.html', context)


def background_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    background = get_object_or_404(Background, slug=slug)

    context = {'result': background, 'features': background.features.all()}

    return render(request, 'database_view/detail_pages/background_details.html', context)


def skill_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    skill = get_object_or_404(Skill, slug=slug)

    context = {'result': skill}

    return render(request, 'database_view/detail_pages/skill_details.html', context)


def language_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    language = get_object_or_404(Language, slug=slug)

    context = {'result': language}

    return render(request, 'database_view/detail_pages/language_details.html', context)


def condition_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    condition = get_object_or_404(Condition, slug=slug)

    context = {'result': condition}

    return render(request, 'database_view/detail_pages/condition_details.html', context)


# Equipment Detail Views:
def item_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    item = get_object_or_404(Item, slug=slug)

    context = {'result': item}

    return render(request, 'database_view/detail_pages/item_details.html', context)


def weapon_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    weapon = get_object_or_404(Weapon, slug=slug)

    ranged = False
    if weapon.melee_or_ranged == 'Ranged':
        ranged = True

    dmg_type = weapon.base_damage_type.get()

    context = {'result': weapon, 'ranged': ranged, 'properties': weapon.properties.all(), 'dmg_type': dmg_type.name}

    return render(request, 'database_view/detail_pages/weapon_details.html', context)


def armor_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    armor = get_object_or_404(Armor, slug=slug)

    maximum = False

    if armor.dexterity_modifier_max > 0:
        maximum = armor.dexterity_modifier_max

    minute = False
    if armor.don_time != '1 action':
        minute = True

    if armor.don_time != '1':
        don_s = 's'
    else:
        don_s = ''

    if armor.doff_time != '1':
        doff_s = 's'
    else:
        doff_s = ''

    context = {'result': armor, 'max': maximum, 'minute': minute, 'don_s': don_s, 'doff_s': doff_s}

    return render(request, 'database_view/detail_pages/armor_details.html', context)


def tool_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    tool = get_object_or_404(Tool, slug=slug)

    context = {'result': tool}

    return render(request, 'database_view/detail_pages/tool_details.html', context)


def mount_details(request, slug):
    """
    Detail HTML for Spell instances
    """
    mount = get_object_or_404(MountAndVehicle, slug=slug)

    speed = 'feet'
    if mount.vehicle_type == 'Water':
        speed = 'mph'

    context = {'result': mount, 'speed': speed}

    return render(request, 'database_view/detail_pages/mount_details.html', context)


# Character Creation Screens (CC):
@method_decorator(login_required, name='dispatch')
class CharacterCreationName(CreateView):
    """First view in the character creation flow."""

    model = Character
    fields = ['char_name',]
    success_url = reverse_lazy('nc_race')
    template_name = 'characters/char_creation_name.html'

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super(CharacterCreationName, self).form_valid(form)


@login_required()
def nc_race(request):
    """Choose a race and subclass if available."""

    if request.method == "GET":
        character = request.user.characters.latest('accessed')
        request.session['character'] = character.pk
        form = CCRace()

        context = {'race_form': form, 'character': character}

        return render(request, 'characters/nc_race.html', context)

    elif request.method == "POST":
        character = Character.objects.get(pk=request.session['character'])
        form = CCRace(data=request.POST)

        context = {'race_form': form, 'character': character}

        if form.is_valid():

            character.char_race = form.cleaned_data['race']
            character.char_subrace = form.cleaned_data['subrace']
            character.save()

            request.session['character'] = character.pk
            request.session['next_screen'] = 'nc_class'

            for feature in character.char_race.features.all():
                if feature.is_choice:
                    return redirect('choice_screen')

            for feature in character.char_subrace.features.all():
                if feature.is_choice:
                    return redirect('choice_screen')

            return redirect('nc_class')

        return render(request, 'characters/nc_race.html', context)

@login_required()
def nc_choice(request):
    """This is a general purpose screen for choosing when a feature has is_choice set to True."""

    ChoiceFormSet = formset_factory(ChoiceForm, max_num=1)

    if request.method == "GET":

        character = Character.objects.get(pk=request.session['character'])

        redirect_to = request.session['next_screen']

        feature_search = dict()

        if redirect_to == 'nc_class':
            features = character.char_race.features.all()
            feature_search[character.char_race.name] = list()

            for feature in features:
                if feature.is_choice and feature.choice_amount != -1:
                    feature_search[character.char_race.name].append(feature)

            if len(feature_search[character.char_race.name]) == 0:
                del feature_search[character.char_race.name]

            features = character.char_subrace.features.all()
            feature_search[character.char_subrace.name] = list()

            for feature in features:
                if feature.is_choice and feature.choice_amount != -1:
                    feature_search[character.char_subrace.name].append(feature)

            if len(feature_search[character.char_subrace.name]) == 0:
                del feature_search[character.char_subrace.name]

        elif redirect_to == 'nc_ability_scores':
            features = character.classlevels.all()[0].char_class.features.all()
            feature_search[character.classlevels.all()[0].char_class.name] = list()

            for feature in features:
                if feature.is_choice and feature.prereq_class_level <= 1:
                    feature_search[character.classlevels.all()[0].char_class.name].append(feature)

            if len(feature_search[character.classlevels.all()[0].char_class.name]) == 0:
                del feature_search[character.classlevels.all()[0].char_class.name]

            try:
                features = character.char_prestige_classes.all()[0].features.all()
                feature_search[character.char_prestige_classes.all()[0].name] = list()

                for feature in features:
                    if feature.is_choice and feature.prereq_class_level <= 1:
                        feature_search[character.char_prestige_classes.all()[0].name].append(feature)

                if len(feature_search[character.char_prestige_classes.all[0].name]) == 0:
                    del feature_search[character.char_prestige_classes.all[0].name]

            except IndexError:
                pass

        elif redirect_to == 'nc_equipment':
            features = character.char_background.features.all()
            feature_search[character.char_background.name] = list()

            for feature in features:
                if feature.is_choice and feature.choice_amount != -1:
                    feature_search[character.char_background.name].append(feature)

            if len(feature_search[character.char_background.name]) == 0:
                del feature_search[character.char_background.name]

        spell_levels = ['Cantrip', '1st-Level', '2nd-Level', '3rd-Level', '4th-Level', '5th-Level', '6th-Level',
                        '7th-Level', '8th-Level', '9th-Level']

        multi_search = ['character', 'Spell']
        
        single_search = ['Feature', 'DragonAncestry', 'Language', 'EnemyRace', 'LandType']
        
        lvl_1_skip = ['PrestigeClass']

        initial = list()

        for search_type, feature_list in enumerate(feature_search.values()):
            for index, feature in enumerate(feature_list):
                data = dict()

                redirect_page = redirect_to
                max_choices = feature.choice_amount
                min_choices = feature.choice_amount
                feature_name = feature.name

                choice_type = feature.choice_type.split(', ')

                if choice_type[0] in single_search:
                    feature_choices = feature.choices.split(', ')
                    if feature_choices[0] == 'Skill':
                        queryset = getattr(rules_models, choice_type[0]).objects.filter(name__iregex=r'Skill:')
                    else:
                        queryset = getattr(rules_models, choice_type[0]).objects.filter(name__in=feature_choices)

                elif choice_type[0] in multi_search:
                    feature_choices = feature.choices.split(', ')
                    if choice_type[0] == 'Spell':
                        if feature_choices[0] == 'Any':
                            queryset = Spell.objects.filter(level__in=spell_levels)
                        else:
                            choice_class = feature_choices[0]
                            choice_level = feature_choices[1]
                            queryset = Spell.objects.filter(available_to__icontains=choice_class).filter(level__iexact=choice_level)

                    elif choice_type[0] == 'Feature':
                        queryset = character.features.filter(name__icontains=feature_choices[0])

                elif choice_type[0] in lvl_1_skip:
                    if len(character.classlevels.all()) == 1:
                        if character.classlevels.all()[0].class_level == 1:
                            continue
                        else:
                            """prestige_search"""
                else:
                    continue

                data['redirect_page'] = redirect_page
                data['max_choices'] = max_choices
                data['min_choices'] = min_choices
                data['feature_name'] = feature_name
                data['feature_type'] = choice_type[0]
                data['choices'] = queryset

                initial.append(data)

            formset = ChoiceFormSet(initial=initial)

            context = {'formset': formset, 'feature_search': feature_search}

            return render(request, 'characters/choice_screen.html', context)

    if request.method == 'POST':
        pass


@login_required()
def nc_choice_set(request):

    character = Character.objects.get(pk=request.session['character'])

    if request.method == 'POST':

        feature_info = dict(request.POST.copy())

        for data in feature_info.values():
            search_type = data[0]
            item_pk = data[1].split(',')
            redirect_to = data[2]

            if search_type == 'Spell':
                new_spell = Spell.objects.filter(pk__in=item_pk)

                for spell in new_spell:
                    ready = False

                    if spell.level == 'Cantrip':
                        ready = True

                    SpellsReady.objects.create(
                        character=character,
                        spells=spell,
                        spell_ready=ready,
                    )

            elif search_type == 'Feature':
                new_feature = getattr(rule_models, search_type).objects.filter(pk__in=item_pk)
                for feature in new_feature:
                    character.features.add(feature)

            else:
                new_feature = getattr(rule_models, search_type).objects.get(pk__in=item_pk)
                character.char_traits.add(new_feature)

        return HttpResponse(redirect_to)

@login_required()
def nc_class(request):
    """Choose a class for new character."""

    if request.method == "GET":
        character = Character.objects.get(pk=request.session['character'])
        form = CCClass()

        context = {'character': character, 'class_form': form}

        return render(request, 'characters/nc_class.html', context)

    elif request.method == "POST":
        character = Character.objects.get(pk=request.session['character'])
        form = CCClass(data=request.POST)

        context = {'class_form': form, 'character': character}

        if form.is_valid():

            # check if a character already has levels in a class, if so, don't create another association.
            klass = form.cleaned_data['klass']

            current_class_levels = ClassLevel.objects.filter(character__pk=request.session['character'])
            if len(current_class_levels) != 0:
                for char in current_class_levels:
                    if char.char_class == klass:
                        pass
                    else:
                        ClassLevel.objects.create(
                            character=character,
                            char_class=klass,
                            class_level=1
                        )
            else:
                ClassLevel.objects.create(
                    character=character,
                    char_class=klass,
                    class_level=1
                )

            if klass == Class.objects.get(name='Cleric'):
                character.char_prestige_classes.add(form.cleaned_data['cleric_prestige'])

            elif klass == Class.objects.get(name='Sorcerer'):
                character.char_prestige_classes.add(form.cleaned_data['sorcerer_prestige'])

            elif klass == Class.objects.get(name='Warlock'):
                character.char_prestige_classes.add(form.cleaned_data['warlock_prestige'])

            # else:
            #     character.char_prestige = PrestigeClass.objects.get(name='None')

            character.max_health = form.cleaned_data['hp']
            character.current_health = form.cleaned_data['hp']

            if klass.saving_throw_1 == 'Strength' or klass.saving_throw_2 == 'Strength':
                character.STR_saving_throw = True

            if klass.saving_throw_1 == 'Dexterity' or klass.saving_throw_2 == 'Dexterity':
                character.DEX_saving_throw = True

            if klass.saving_throw_1 == 'Constitution' or klass.saving_throw_2 == 'Constitution':
                character.CON_saving_throw = True

            if klass.saving_throw_1 == 'Intelligence' or klass.saving_throw_2 == 'Intelligence':
                character.INT_saving_throw = True

            if klass.saving_throw_1 == 'Wisdom' or klass.saving_throw_2 == 'Wisdom':
                character.WIS_saving_throw = True

            if klass.saving_throw_1 == 'Charisma' or klass.saving_throw_2 == 'Charisma':
                character.CHA_saving_throw = True

            character.save()

            request.session['character'] = character.pk
            request.session['next_screen'] = 'nc_ability_scores'

            for feature in character.char_classes.all()[0].features.all():
                if feature.is_choice and feature.prereq_class_level == 1:
                    return redirect('choice_screen')

            for feature in character.char_prestige_classes.all()[0].features.all():
                if feature.is_choice and feature.prereq_class_level == 1:
                    return redirect('choice_screen')

            return redirect('nc_ability_scores')

        return render(request, 'characters/nc_class.html', context)


@login_required()
def nc_ability_scores(request):
    """
    Help with character creation?
    """

    if request.method == "GET":
        choice_form = AbilityScoresChoice()
        roll_form = AbilityScoresChoice()
        buy_form = AbilityScoresChoice()
        class_level = ClassLevel.objects.filter(character__pk=request.session['character'])
        character = Character.objects.get(pk=request.session['character'])

        context = {'character': character, 'class_level': class_level, 'choice_form': choice_form, 'roll_form': roll_form, 'buy_form': buy_form}

        return render(request, 'characters/nc_ability_scores.html', context)

    elif request.method == "POST":
        form = AbilityScoresChoice(data=request.POST)
        class_level = ClassLevel.objects.filter(character__pk=request.session['character'])
        character = Character.objects.get(pk=request.session['character'])

        context = {'character': character, 'class_level': class_level, 'form': form}

        if form.is_valid():
            form.cleaned_data['None'] = 0  # Catch all if race or subrace doesn't have an ability modifier.
            # TODO: allow humans to add one to two separate choices.
            # For humans to add one to each score:
            if character.char_race.ability_score_1 == 'All':
                form.cleaned_data['All'] = 0
                all_add = 1
            else:
                form.cleaned_data[character.char_race.ability_score_1] += character.char_race.ability_score_1_bonus
                form.cleaned_data[character.char_race.ability_score_2] += character.char_race.ability_score_2_bonus
                form.cleaned_data[character.char_subrace.ability_score_1] += character.char_subrace.ability_score_1_bonus
                form.cleaned_data[character.char_subrace.ability_score_2] += character.char_subrace.ability_score_2_bonus
                all_add = 0

            character = Character.objects.get(pk=request.session['character'])

            character.STR_score = form.cleaned_data['Strength'] + all_add
            character.DEX_score = form.cleaned_data['Dexterity'] + all_add
            character.CON_score = form.cleaned_data['Constitution'] + all_add
            character.INT_score = form.cleaned_data['Intelligence'] + all_add
            character.WIS_score = form.cleaned_data['Wisdom'] + all_add
            character.CHA_score = form.cleaned_data['Charisma'] + all_add

            character.save()

            request.session['character'] = character.pk
            request.session['next_screen'] = 'nc_personality'

            return redirect('nc_personality')

        return render(request, 'characters/nc_ability_scores.html', context)


@login_required()
def nc_personality(request):
    """Get information about the character's personality."""

    if request.method == "GET":

        form = CCPersonality()
        class_level = ClassLevel.objects.filter(character__pk=request.session['character'])
        character = Character.objects.get(pk=request.session['character'])

        context = {'character': character, 'class_level': class_level, 'form': form}

        return render(request, 'characters/nc_personality.html', context)

    elif request.method == "POST":
        form = CCPersonality(data=request.POST)
        class_level = ClassLevel.objects.filter(character__pk=request.session['character'])
        character = Character.objects.get(pk=request.session['character'])

        context = {'character': character, 'class_level': class_level, 'form': form}

        if form.is_valid():

            character.alignment = form.cleaned_data['alignment']

            if form.cleaned_data['ideals'] != "":
                character.ideals = form.cleaned_data['ideals']

            if form.cleaned_data['bonds'] != "":
                character.ideals = form.cleaned_data['bonds']

            if form.cleaned_data['flaws'] != "":
                character.ideals = form.cleaned_data['flaws']

            character.save()
            request.session['next_screen'] = 'nc_background'

            return redirect('nc_background')

        return render(request, 'characters/nc_personality.html', context)


@login_required()
def nc_background(request):
    """Assign the character's background."""

    if request.method == "GET":
        form = CCBackground()
        class_level = ClassLevel.objects.filter(character__pk=request.session['character'])
        character = Character.objects.get(pk=request.session['character'])

        context = {'character': character, 'class_level': class_level, 'form': form}

        return render(request, 'characters/nc_background.html', context)

    elif request.method == "POST":
        form = CCBackground(data=request.POST)
        class_level = ClassLevel.objects.filter(character__pk=request.session['character'])
        character = Character.objects.get(pk=request.session['character'])

        context = {'character': character, 'class_level': class_level, 'form': form}

        if form.is_valid():
            character.char_background = form.cleaned_data['background']

            character.save()
            request.session['next_screen'] = 'nc_equipment'

            for feature in character.char_background.features.all():
                if feature.is_choice:
                    return redirect('choice_screen')

            return redirect('nc_equipment')

        return render(request, 'characters/nc_background.html', context)


@login_required()
def nc_equipment(request):
    """Assigning starting equipment"""

    if request.method == "GET":
        form = CCEquipment()
        class_level = ClassLevel.objects.filter(character__pk=request.session['character'])
        character = Character.objects.get(pk=request.session['character'])

        context = {'character': character, 'class_level': class_level, 'form': form}

        return render(request, 'characters/nc_equipment.html', context)

    elif request.method == "POST":
        form = CCEquipment(data=request.POST)
        class_level = ClassLevel.objects.filter(character__pk=request.session['character'])
        character = Character.objects.get(pk=request.session['character'])

        context = {'character': character, 'class_level': class_level, 'form': form}

        if form.is_valid():
            character.weapons_inv = form.cleaned_data['weapons']
            character.tools_inv = form.cleaned_data['tools']
            character.items_inv = form.cleaned_data['items']
            character.armor_inv = form.cleaned_data['armor']

            character.save()
            request.session['next_screen'] = 'nc_resolve'

            return redirect('nc_resolve')

        return render(request, "characters/nc_resolve.html", context)


@login_required()
def nc_resolve(request):
    """Final screen for character. Show all information and as where they want to go next."""

    if request.method == "GET":
        form = NCResolve()
        class_level = ClassLevel.objects.filter(character__pk=request.session['character'])
        character = Character.objects.get(pk=request.session['character'])

        context = {'character': character, 'class_level': class_level, 'form': form}

        return render(request, "characters/nc_resolve.html", context)

    elif request.method == "POST":

        form = NCResolve(data=request.POST)

        context = {'form': form}

        if form.is_valid():

            next_page = form.cleaned_data['next_page']

            if next_page == "delete":
                Character.objects.get(pk=request.session['character']).delete()
                next_page = "home"

            elif next_page == "":
                next_page = "home"

            del request.session['character']
            del request.session['next_screen']

            return redirect(next_page)

        return render(request, "characters/nc_resolve.html", context)
