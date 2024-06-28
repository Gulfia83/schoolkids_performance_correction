import os
import argparse
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from datacenter.models import Mark, Chastisement, Commendation
from schoolbase_helpers import get_schoolkid
from schoolbase_helpers import get_random_lesson
from schoolbase_helpers import get_random_commendation


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3]).update(points=5)

def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()

def create_commendation(schoolkid, subject, commendation):
    lesson = get_random_lesson(schoolkid, subject)
    Commendation.objects.create(
        text=commendation,
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher 
    )

def main():
    parser = argparse.ArgumentParser(description="Исправь оценки, удали замечания и добавь похвалу")
    parser.add_argument("--name", type=str, help="Фамилия и имя ученика", default="Фролов Иван")
    parser.add_argument("--subject", type=str, help="По какому предмету добавить похвалу", default=None)

    args = parser.parse_args()

    schoolkid = get_schoolkid(args.name)
    commendation_text = get_random_commendation()

    fix_marks(schoolkid)
    remove_chastisements(schoolkid)
    create_commendation(schoolkid, args.subject, commendation_text)

if __name__=="__main__":
    main()
