from string import Template

from gemeaux import TemplateError, responses

class TemplateStrResponse(responses.Response):
    def __init__(self, template, **context):
        self.template = Template(template)
        self.context = context

    def __body__(self):
        try:
            body = self.template.substitute(self.context)
            return bytes(body, encoding="utf-8")
        except KeyError as exc:
            raise TemplateError(exc.args[0])