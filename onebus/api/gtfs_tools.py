from models import Calender


dayofweek_mapping = {0: 'monday',
                     1: 'tuesday',
                     2: 'wednesday',
                     3: 'thursday',
                     4: 'friday',
                     5: 'saturday',
                     6: 'sunday'}


def get_services(date):
    """
    Get service_id by date
    :param date: date object
    :return:
    """

    dayofweek = dayofweek_mapping[date.weekday()]

    kwargs = {"start_date__lte": date,
              "end_date__gte": date,
              dayofweek: 1}

    return Calender.objects.filter(**kwargs).all()

