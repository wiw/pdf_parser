from classic.components import component

from ...application import services

from .join_points import join_point


@component
class TaskController:
    task: services.TaskService

    @join_point
    def on_post_add_task(self, request, response):
        self.task.add_task(
            **request.media,
        )

    @join_point
    def on_get_get_question_type(self, request, response):
        question_types = self.task.get_question_type()
        response.media = {
            'types': question_types
        }

    @join_point
    def on_get_get_treatment_status(self, request, response):
        treatment_status = self.task.get_treatment_status()
        response.media = {
            'status': treatment_status
        }
