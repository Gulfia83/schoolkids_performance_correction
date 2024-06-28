import os
import sys
import random
import argparse
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation

def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3]).update(points=5)

def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()

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

def get_random_lesson(schoolkid, subject):
    lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter)
    if not subject:
        random_lesson = lessons.order_by('?').first()
        return random_lesson
    else:
        try:
            random_lesson = lessons.filter(subject__title__contains=subject).order_by('?').first()
        except IndexError:
            print('Такого предмета нет. Проверьте правильность ввода')
            sys.exit(3)

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

def main():
    parser = argparse.ArgumentParser(description="Исправь оценки, удали замечания и добавь похвалу")
    parser.add_argument("--name", type=str, help="Фамилия и имя ученика", default="Фролов Иван")
    parser.add_argument("--subject", type=str, help="По какому предмету добавить похвалу", default=None)

    args = parser.parse_args()

    schoolkid = get_schoolkid(args.name)
    lesson = get_random_lesson(schoolkid, args.subject)
    commendation_text = get_random_commendation()

    fix_marks(schoolkid)
    remove_chastisements(schoolkid)
    Commendation.objects.create(
        text=commendation_text,
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher 
    )

if __name__=="__main__":
    main()
