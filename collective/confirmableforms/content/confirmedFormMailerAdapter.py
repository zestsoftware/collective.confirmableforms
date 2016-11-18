from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent
from collective.confirmableforms import config
from collective.confirmableforms import ConfirmableFormsMessageFactory as _
from collective.confirmableforms.mailer import simple_send_mail
from collective.confirmableforms.utils import obj_to_pobj
from collective.depositbox.store import Box
from Products.Archetypes import atapi
from Products.CMFCore import permissions
from Products.PloneFormGen.content.formMailerAdapter import FormMailerAdapter
from Products.PloneFormGen.content.formMailerAdapter import formMailerAdapterSchema  # noqa
from Products.TemplateFields import ZPTField as ZPTField


confirmedSchema = atapi.Schema((
    atapi.StringField(
        'title_mail',
        required=True,
        widget=atapi.StringWidget(
            label=_(u'label_title_mail',
                    default=u'Subject for the confirmation e-mail'),
        ),
        schemata='confirmation'
    ),

    atapi.StringField(
        'sender_mail',
        required=False,
        widget=atapi.StringWidget(
            label=_(
                u'label_sender_mail',
                default=u'From address used to send the confirmation e-mail'),
        ),
        schemata='confirmation'
    ),

    ZPTField(
        'plain_mail',
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(
                u'label_plain_mail',
                default=u'Content of the confirmation email (plain text)'),
            description=_(
                u'label_help_plain_mail',
                default=(u'The content of the confirmation email. '
                         'Use [[confirmation_link]] to display the '
                         'confirmation link. You can also use tal language '
                         'here for complex data integration.')),
        ),
        schemata='confirmation'
    ),

    ZPTField(
        'html_mail',
        required=False,
        default_output_type='text/x-html-safe',
        widget=atapi.TextAreaWidget(
            label=_(
                u'label_html_mail',
                default=u'Content of the confirmation email (HTML)'),
            description=_(
                u'label_help_html_mail',
                default=(u'If the receiver can read HTML emails, '
                         'this will be displayed instead of the simple text '
                         'version specified above. Use the same substitution '
                         'for the link and tal language is also enabled.')),
        ),
        schemata='confirmation'
    ),

    atapi.StringField(
        'thanksPage',
        searchable=False,
        required=False,
        vocabulary='thanksPageVocabulary',
        widget=atapi.SelectionWidget(
            label=_(
                u'label_thankspage_text',
                default=u'Thanks Page'),
            description=_(
                u'help_thankspage_text',
                default=(
                    u'Pick a page contained in the form that you wish to show '
                    'when the form submission has been confirmed. '
                    '(If none are available, add one.) '
                    'Choose none to display the standard thanks page '
                    'of the form.')),
        ),
        schemata='confirmation'
    ),

    atapi.IntegerField(
        'expiration_time',
        required=False,
        default=7,
        widget=atapi.IntegerWidget(
            label=_(u'label_expiration_time',
                    default=u'Expiration time'),
            description=_(
                u'label_help_expiration_time',
                default=(
                    u'Maximum number of days allowed to confirm the form.')),
        ),
        schemata='confirmation'
    ),

))
confirmedFormMailerAdapterSchema = formMailerAdapterSchema.copy() + \
    confirmedSchema


class ConfirmedFormMailerAdapter(FormMailerAdapter):
    schema = confirmedFormMailerAdapterSchema
    security = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'post_validate')

    def post_validate(self, REQUEST=None, errors=None):
        # Perform a check after validation.  We do not want to make
        # plain_mail and html_mail required, but we do need at least
        # one of them filled.
        if (not REQUEST.form.get('plain_mail').strip() and
                not REQUEST.form.get('html_mail').strip()):
            error_message = _((u"You must specify either a plain text or "
                               u"html mail (or both)."))
            if 'plain_mail' not in errors:
                errors['plain_mail'] = error_message
            if 'html_mail' not in errors:
                errors['html_mail'] = error_message

    security.declarePrivate('get_box')

    def get_box(self):
        if not hasattr(self, '_deposit_box'):
            self._deposit_box = Box()

        self._deposit_box.max_age = self.getExpiration_time()
        return self._deposit_box

    security.declarePrivate('onSuccess')

    def onSuccess(self, fields, REQUEST=None):
        # Well, we'll deal with that later on.
        self.send_confirmation_email(fields, REQUEST)

    security.declareProtected(permissions.View, 'get_form')

    def get_form(self):
        return aq_parent(self)

    security.declareProtected(permissions.View, 'get_mail_receiver')

    def get_mail_receiver(self):
        # This does not really get the email value but checks that
        # there is a replyto field available in the form.
        form = self.get_form()
        try:
            return form.get('replyto')
        except:
            return None

    security.declarePrivate('send_confirmation_email')

    def send_confirmation_email(self, fields, REQUEST=None):
        receiver_field = self.get_mail_receiver()

        if receiver_field is None:
            # Not much to do in that case.
            return

        mail_title = self.getTitle_mail()
        mail_plain_body = self.getPlain_mail().strip()
        mail_html_body = self.getHtml_mail().strip()
        mail_to = self.REQUEST.form.get('replyto')
        mail_from = self.getSender_mail()

        box = self.get_box()
        secret = box.put(obj_to_pobj(REQUEST.form), token=mail_to)
        box.confirm(secret, token=mail_to)

        confirm_url = '%s/confirm-form?secret=%s&email=%s' % (
            self.absolute_url(),
            secret,
            mail_to
        )

        mail_plain_body = mail_plain_body.replace(
            '[[confirmation_link]]', confirm_url)
        mail_html_body = mail_html_body.replace(
            '[[confirmation_link]]', confirm_url)

        simple_send_mail(
            mail_plain_body,
            mail_html_body,
            [mail_to],
            mail_from,
            mail_title)


atapi.registerType(ConfirmedFormMailerAdapter, config.PROJECTNAME)
