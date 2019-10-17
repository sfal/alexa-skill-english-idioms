# -*- coding: utf-8 -*-
"""App in Italian for English idioms"""

import random
import logging
import json

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
import modi_di_dire
from modi_di_dire import data
import backgrounds
from backgrounds import data
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, ExecuteCommandsDirective, SpeakItemCommand,
    AutoPageCommand, HighlightMode)


SKILL_NAME = "Idiomi Inglesi"
GET_FACT_MESSAGE = "Ecco un modo di dire: "
HELP_MESSAGE = "Puoi chiedermi: dimmi un modo di dire inglese. Oppure: dimmi un idioma inglese."
HELP_REPROMPT = "Come posso aiutarti?"
STOP_MESSAGE = "Alla prossima!"
FALLBACK_MESSAGE = "Idiomi Inglesi non può aiutarti. Può aiutarti a imparare nuovi modi di dire inglesi se mi chiedi: dimmi un modo di dire. Come posso aiutarti?"
FALLBACK_REPROMPT = 'Come posso aiutarti?'
EXCEPTION_MESSAGE = "Mi dispiace. Non posso aiutarti."


sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# check if device supports apl


def _supports_apl(handler_input):
    # type: (HandlerInput) -> bool
    device = handler_input.request_envelope.context.system.device
    apl_interface = device.supported_interfaces.alexa_presentation_apl
    return bool(apl_interface)


def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)


# Built-in Intent Handlers
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Benvenuto in Idiomi Inglesi. Puoi chiedermi: dimmi un modo di dire inglese."

        # handler_input.response_builder.speak(speech_text).set_card(
        #     SimpleCard(speech_text)).set_should_end_session(
        #     False)
        # return handler_input.response_builder.response

        if _supports_apl(handler_input):  # check if APL is supported on device
            handler_input.response_builder.speak(speech_text).add_directive(RenderDocumentDirective(
                token="idiomiToken", document=_load_apl_document("apl-welcome.json"))).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard(speech_text)).set_should_end_session(False)

        return handler_input.response_builder.response


class IdiomaHandler(AbstractRequestHandler):
    """Handler for Skill Launch and IdiomaIntent Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("IdiomaIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In IdiomaHandler")

        random_fact = random.choice(modi_di_dire.data)
        idiom = random_fact["Idioma"]
        meaning = random_fact["Significato"]
        example = random_fact["Esempio"]

        random_background = random.choice(backgrounds.data)
        image = random_background["img"]

        speech = GET_FACT_MESSAGE + \
            ("<voice name='Emma'><lang xml:lang='en-GB'>{}</lang></voice>. Significa: {}. Ecco un esempio: <voice name='Emma'><lang xml:lang='en-GB'>{}</lang></voice>".format(idiom, meaning, example))

        # handler_input.response_builder.speak(speech).set_card(SimpleCard(SKILL_NAME, idiom + "\n" + example)).set_should_end_session(
        #     True)
        # return handler_input.response_builder.response

        if _supports_apl(handler_input):  # check if APL is supported on device
            handler_input.response_builder.speak(speech).add_directive(
                RenderDocumentDirective(
                    token="idiomiToken",
                    document=_load_apl_document("apl-idioma.json"),
                    datasources={
                        'idiomaTemplateData': {
                            'type': 'object',
                            'properties': {
                                'text': "{}".format(idiom)
                            }
                        },
                        'backgroundsData': {
                            'image': "{}".format(image)
                        }

                    }
                )).set_should_end_session(True)
        else:
            handler_input.response_builder.speak(speech).set_card(SimpleCard(SKILL_NAME, idiom + "\n" + meaning)).set_should_end_session(
                True)

        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.
    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(IdiomaHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
