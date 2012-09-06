from Products.TemplateFields import ZPTField as ZPTField

class HTMLZPTField(ZPTField):
    """ Small hack to use TinyMCE with ZPTField.
    """

    def getAllowedContentTypes(self, *args, **kwargs):
        return ('html', )
