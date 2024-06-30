import sys
import random
from datacenter.models import Schoolkid, Lesson

def get_schoolkid(args):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=args)
        return schoolkid
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников с эти именем. Уточните имя.')
        sys.exit(1)
    except Schoolkid.DoesNotExist:
        print('Такого имени нет. Проверьте правильность ввода')
        sys.exit(2)

def get_random_lesson(schoolkid, args):
    lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter)
    if not args:
        random_lesson = lessons.order_by('?').first()
        return random_lesson
    else:
        random_lesson = lessons.filter(subject__title__contains=args).order_by('?').first()
        if not random_lesson:
            print('Такого предмета нет. Проверьте правильность ввода')
            sys.exit(3)
        else:
            return random_lesson

def get_random_commendation():
    commendations = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',   
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!'
    ]

    random_commendation = random.choice(commendations)
    return random_commendation