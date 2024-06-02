import random
from datacenter.models import Mark, Schoolkid, Chastisement, Lesson, Commendation


def get_schoolkid():
    while True:
        name = input('Введите ФИО ученика: ')
        try:
            return Schoolkid.objects.filter(full_name__contains=name).get()
        except Schoolkid.DoesNotExist:
            print(f'Проверьте написание имени и фамилии ученика {name} - такого нет в базе учеников школы')
        except Schoolkid.MultipleObjectsReturned:
            print(f'По Вашему запросу {name} нашлось несколько учеников, уточните запрос')


def fix_marks():
    schoolkid = get_schoolkid()
    if schoolkid:
        two_and_three_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
        for two_and_three_mark in two_and_three_marks:
            two_and_three_mark.points = 5
            two_and_three_mark.save()


def remove_chastisements():
    schoolkid = get_schoolkid()
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation():
    commendation_list = [
        "Ты сегодня был как волшебник!",
        "Твои ответы — это настоящая музыка для моих ушей!",
        "Ты так классно справился, что мне хочется поставить тебе памятник из мела!",
        "Сегодня ты был настоящей звездой класса!",
        "Ты сегодня решил такую задачу, что сам Эйнштейн бы аплодировал стоя!",
        "Если бы была премия «Лучший ученик дня», ты бы её получил!",
        "Ты решил задачу быстрее, чем я успел её задать!",
        "Если бы знания были спортом, ты бы был чемпионом мира!",
        "После твоего ответа у меня поднялось настроение на целый день!",
        "Сегодня превзошел все мои ожидания!",
        "Ты заслуживаешь медаль за свои старания и успехи!",
        "Если бы я мог, я бы поставил тебе десять пятёрок!",
        "Ты просто рок-звезда!",
        "Твои ответы просто на высоте, я в восторге!",
        "Был как Джеймс Бонд, но в учёбе!",
        "Превратил скучный урок в настоящее приключение!",
        "Сегодня поднял планку для всего класса!",
        "Твои успехи заставляют меня гордиться быть твоим учителем!"
    ]

    schoolkid = get_schoolkid()
    while True:
        subject_title = input("Введите название предмета: ")
        if schoolkid:
            lessons = list(Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                                 group_letter=schoolkid.group_letter,
                                                 subject__title=subject_title))
            if not lessons:
                print("Проверь написание название предмета")
            else:
                random_text = random.choice(commendation_list)
                random_lesson = random.choice(lessons)
                created = random_lesson.date
                subject = random_lesson.subject
                teacher = random_lesson.teacher
                commendation = Commendation.objects.create(text=random_text, created=created, schoolkid=schoolkid,
                                                           subject=subject, teacher=teacher)
                commendation.save()
                print(f'Поздравляю!\n Тебя похвалил {created} по предмету {subject_title} '
                      f'учитель {teacher} \nзаписью: \n{random_text}')
                return None
