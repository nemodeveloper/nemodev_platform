# -*- coding: utf-8 -*-


# События по работе с расписанием
from src.apps.schedule.models import WorkPlan, Lesson, SchoolQuarter

LESSON_EVENTS = (
    'CANCELED', 'EDIT', 'MOVED'
)


class NodeAnalyzeError(object):

    def __init__(self, error_type, message, **kwargs):
        self.error_type = error_type
        self.message = message
        self.kwargs = kwargs


# Базовый узел графа целостности
class BaseNode(object):

    def __init__(self):
        super(BaseNode, self).__init__()

    def analyze(self, event_info):
        raise NotImplementedError('Метод анализа расписания узлом')


# Узел нагрузки
class LoadNode(BaseNode):

    # data - урок для анализа
    def __init__(self, data):
        super(LoadNode, self).__init__()
        self.data = data
        self.cur_quarter = self._get_current_quarter()
        self.subject_name = self.data.subject.sub_name

    # Получить текущий учебный период
    def _get_current_quarter(self):
        return SchoolQuarter.objects.filter(
            start_date__gte=self.data.lesson_date.date,
            end_date__lte=self.data.lesson_date.date
        ).first()

    # Получить количество уроков по учебному плану
    def _get_subject_count(self):
        work_plan = WorkPlan.objects.filter(school_quarter=self.cur_quarter,
                                            subject=self.data.subject,
                                            school_class=self.data.school_class
                                            ).first()
        return work_plan.total_lesson_count if work_plan else 0

    # Получить фактическое проведенное количество уроков
    def _get_current_subject_count(self):
        return Lesson.objects.filter(subject=self.data.subject, school_class=self.data.school_class).count()

    # Получить отмененные уроки
    def _get_canceled_lessons(self):
        return Lesson.objects.filter(subject=self.data.subject,
                                     school_class=self.data.school_class,
                                     lesson_status='CANCELED')

    def _build_base_verdict(self):
        return {
            'type': '',
            'errors': [],
        }

    def analyze(self, event_info):
        verdict = self._build_base_verdict()

        work_plan_subject_count = self._get_subject_count()
        current_subject_count = self._get_current_subject_count()
        not_done_count = work_plan_subject_count - current_subject_count

        event_type = event_info['type']
        verdict['type'] = event_type
        if event_info in LESSON_EVENTS:
            errors = verdict['errors']
            base_kwargs = {
                'plan_count': work_plan_subject_count,
                'current_count': current_subject_count,
            }
            if not_done_count < 0:
                errors.append(
                    NodeAnalyzeError('TO_MORE_LESSON_DONE',
                                     'По предмету %s проведено больше предметов чем по учебному плану!' % self.subject_name,
                                     **base_kwargs)
                )
            if not_done_count > 0:
                errors.append(
                    NodeAnalyzeError('NOT_MORE_LESSON_DONE',
                                     'По предмет %s проведено меньше уроков чем по учебному плану!' % self.subject_name,
                                     **base_kwargs)
                )

            canceled_lessons = self._get_canceled_lessons()
            if canceled_lessons:
                base_kwargs['canceled_lessons'] = canceled_lessons
                errors.append(
                    NodeAnalyzeError('HAVE_CANCELED_LESSON',
                                     'По предмету %s есть отмененные уроки!' % self.subject_name,
                                     **base_kwargs)
                )

        else:
            verdict['errors'].append(
                NodeAnalyzeError('NOT_CORRECT_EVENT', 'Не корректное событие по работе с расписанием для узла нагрузки - %s' % event_type)
            )

        return verdict


# Узел согласования
class CoordinationNode(BaseNode):

    def __init__(self):
        super(CoordinationNode, self).__init__()

    def analyze(self, event_info):
        pass


# Узел приоритетов
class PriorityNode(BaseNode):

    def __init__(self):
        super(PriorityNode, self).__init__()

    def analyze(self, event_info):
        pass
