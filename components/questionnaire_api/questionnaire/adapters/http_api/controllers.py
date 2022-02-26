from classic.components import component

from questionnaire.application.dashboard import services

from .join_points import join_point


@component
class QuestionnaireController:
    questionnaire: services.QuestionnaireService

    @join_point
    def on_post_add_product_to_cart(self, request, response):
        self.questionnaire.do_smth(
            **request.media,
        )
