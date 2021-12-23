from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent
from collective.confirmableforms import config
from collective.confirmableforms import ConfirmableFormsMessageFactory as _
from collective.confirmableforms.interfaces import IConfirmedFormMailerAdapter
from collective.confirmableforms.mailer import simple_send_mail
from collective.confirmableforms.utils import obj_to_pobj
from collective.depositbox.store import Box
from Products.Archetypes import atapi
from Products.Archetypes.utils import shasattr
from Products.CMFCore import permissions
from Products.PloneFormGen.config import EDIT_ADDRESSING_PERMISSION
from Products.PloneFormGen.config import EDIT_ADVANCED_PERMISSION
from Products.PloneFormGen.config import EDIT_TALES_PERMISSION
from Products.PloneFormGen.content.formMailerAdapter import FormMailerAdapter
from Products.PloneFormGen.content.formMailerAdapter import (
    formMailerAdapterSchema,
)  # noqa
from Products.TALESField import TALESString
from Products.TemplateFields import ZPTField as ZPTField
from zope.interface import implementer


confirmedSchema = atapi.Schema(
    (
        atapi.StringField(
            "title_mail",
            required=True,
            widget=atapi.StringWidget(
                label=_(
                    u"label_title_mail", default=u"Subject for the confirmation e-mail"
                )
            ),
            schemata="confirmation",
        ),
        atapi.StringField(
            "confirmation_recipient_email",
            searchable=0,
            required=0,
            default_method="getDefaultRecipient",
            write_permission=EDIT_ADDRESSING_PERMISSION,
            read_permission=permissions.ModifyPortalContent,
            validators=("isEmail",),
            widget=atapi.StringWidget(
                label=_(
                    u"label_recipient_email",
                    default=u"Confirmation recipient's e-mail address",
                ),
                description=_(
                    u"help_recipient_email",
                    default=u"The e-mail address that will receive the e-mail asking for confirmation.",
                ),
            ),
            schemata="confirmation",
        ),
        atapi.StringField(
            "confirmation_to_field",
            searchable=0,
            required=0,
            default="#NONE#",
            write_permission=EDIT_ADVANCED_PERMISSION,
            read_permission=permissions.ModifyPortalContent,
            vocabulary="fieldsDisplayList",
            widget=atapi.SelectionWidget(
                label=_(
                    u"label_to_extract", default=u"Extract Confirmation Recipient From"
                ),
                description=_(
                    u"help_to_extract",
                    default=u"""
                Choose a form field from which you wish to extract
                input for the To header. If you choose anything other
                than "None", this will override the "Confirmation recipient's e-mail address"
                setting above. Be very cautious about allowing unguarded user
                input for this purpose.
                """,
                ),
            ),
            schemata="confirmation",
        ),
        atapi.StringField(
            "sender_mail",
            required=False,
            widget=atapi.StringWidget(
                label=_(
                    u"label_sender_mail",
                    default=u"From address used to send the confirmation e-mail",
                )
            ),
            schemata="confirmation",
        ),
        ZPTField(
            "plain_mail",
            required=False,
            widget=atapi.TextAreaWidget(
                label=_(
                    u"label_plain_mail",
                    default=u"Content of the confirmation email (plain text)",
                ),
                description=_(
                    u"label_help_plain_mail",
                    default=(
                        u"The content of the confirmation email. "
                        "Use [[confirmation_link]] to display the "
                        "confirmation link. You can also use tal language "
                        "here for complex data integration."
                    ),
                ),
            ),
            schemata="confirmation",
        ),
        ZPTField(
            "html_mail",
            required=False,
            default_output_type="text/x-html-safe",
            widget=atapi.TextAreaWidget(
                label=_(
                    u"label_html_mail",
                    default=u"Content of the confirmation email (HTML)",
                ),
                description=_(
                    u"label_help_html_mail",
                    default=(
                        u"If the receiver can read HTML emails, "
                        "this will be displayed instead of the simple text "
                        "version specified above. Use the same substitution "
                        "for the link and tal language is also enabled."
                    ),
                ),
            ),
            schemata="confirmation",
        ),
        atapi.StringField(
            "thanksPage",
            searchable=False,
            required=False,
            vocabulary="thanksPageVocabulary",
            widget=atapi.SelectionWidget(
                label=_(u"label_thankspage_text", default=u"Thanks Page"),
                description=_(
                    u"help_thankspage_text",
                    default=(
                        u"Pick a page contained in the form that you wish to show "
                        "when the form submission has been confirmed. "
                        "(If none are available, add one.) "
                        "Choose none to display the standard thanks page "
                        "of the form."
                    ),
                ),
            ),
            schemata="confirmation",
        ),
        atapi.IntegerField(
            "expiration_time",
            required=False,
            default=7,
            widget=atapi.IntegerWidget(
                label=_(u"label_expiration_time", default=u"Expiration time"),
                description=_(
                    u"label_help_expiration_time",
                    default=(u"Maximum number of days allowed to confirm the form."),
                ),
            ),
            schemata="confirmation",
        ),
        atapi.BooleanField(
            "send_standard_mail",
            required=0,
            searchable=0,
            default="1",
            languageIndependent=1,
            widget=atapi.BooleanWidget(
                label=_(
                    u"label_send_standard_mail",
                    default=u"Send standard mail after confirmation",
                ),
                description=_(
                    u"help_send_standard_mail",
                    default=u"After the user has confirmed the email address "
                    u"by clicking on the confirmation link, "
                    u"send the standard mail, as if this was a standard "
                    u"mail action adapter.",
                ),
            ),
            schemata="confirmation",
        ),
        TALESString(
            "confirmationRecipientOverride",
            schemata="overrides",
            searchable=0,
            required=0,
            validators=("talesvalidator",),
            default="",
            write_permission=EDIT_TALES_PERMISSION,
            read_permission=permissions.ModifyPortalContent,
            isMetadata=True,  # just to hide from base view
            widget=atapi.StringWidget(
                label=_(
                    u"label_recipient_override_text",
                    default=u"Confirmation Recipient Expression",
                ),
                description=_(
                    u"help_recipient_override_text",
                    default=u"""
                    A TALES expression that will be evaluated to override any value
                    otherwise entered for the confirmation recipient e-mail address. You are strongly
                    cautioned against using unvalidated data from the request for this purpose.
                    Leave empty if unneeded. Your expression should evaluate as a string.
                    PLEASE NOTE: errors in the evaluation of this expression will cause
                    an error on form display.
                """,
                ),
                size=70,
            ),
        ),
    )
)
confirmedFormMailerAdapterSchema = formMailerAdapterSchema.copy() + confirmedSchema


@implementer(IConfirmedFormMailerAdapter)
class ConfirmedFormMailerAdapter(FormMailerAdapter):
    schema = confirmedFormMailerAdapterSchema
    security = ClassSecurityInfo()

    security.declareProtected(permissions.View, "post_validate")

    def post_validate(self, REQUEST=None, errors=None):
        # Perform a check after validation.  We do not want to make
        # plain_mail and html_mail required, but we do need at least
        # one of them filled.
        if (
            not REQUEST.form.get("plain_mail").strip()
            and not REQUEST.form.get("html_mail").strip()
        ):
            error_message = _(
                (u"You must specify either a plain text or " u"html mail (or both).")
            )
            if "plain_mail" not in errors:
                errors["plain_mail"] = error_message
            if "html_mail" not in errors:
                errors["html_mail"] = error_message

    security.declarePrivate("get_box")

    def get_box(self):
        if not hasattr(self, "_deposit_box"):
            self._deposit_box = Box()

        self._deposit_box.max_age = self.getExpiration_time()
        return self._deposit_box

    security.declarePrivate("onSuccess")

    def onSuccess(self, fields, REQUEST=None):
        # Well, we'll deal with that later on.
        self.send_confirmation_email(fields, REQUEST)

    security.declareProtected(permissions.View, "get_form")

    def get_form(self):
        return aq_parent(self)

    security.declareProtected(permissions.View, "get_mail_receiver")

    def get_mail_receiver(self, request=None):
        request = request or self.REQUEST

        # 1. Check the various confirmation recipient fields.
        if (
            shasattr(self, "confirmationRecipientOverride")
            and self.getRawConfirmationRecipientOverride()
        ):
            recip_email = self.getConfirmationRecipientOverride()
        else:
            recip_email = None
            if shasattr(self, "confirmation_to_field"):
                recip_email = request.form.get(self.confirmation_to_field, None)
            if not recip_email:
                recip_email = self.getConfirmation_recipient_email()
        if recip_email:
            return recip_email

        # 2. Check the various standard recipient fields.
        if shasattr(self, "recipientOverride") and self.getRawRecipientOverride():
            recip_email = self.getRecipientOverride()
        else:
            recip_email = None
            if shasattr(self, "to_field"):
                recip_email = request.form.get(self.to_field, None)
            if not recip_email:
                recip_email = self.recipient_email
        if recip_email:
            return recip_email

        raise ValueError("No confirmation recipient address found.")

    security.declarePrivate("send_confirmation_email")

    def send_confirmation_email(self, fields, REQUEST=None, **kwargs):
        if REQUEST is not None:
            request = REQUEST
        elif "request" in kwargs:
            request = kwargs["request"]
        else:
            request = self.REQUEST

        mail_to = self.get_mail_receiver(request=request)

        # We will pass the fields with (html) values to the mail templates.
        all_fields = [
            f
            for f in fields
            if not (f.isLabel() or f.isFileField())
            and not (getattr(self, "showAll", True) and f.getServerSide())
        ]

        # which fields should we show?
        if getattr(self, "showAll", True):
            live_fields = all_fields
        else:
            live_fields = [
                f
                for f in all_fields
                if f.fgField.getName() in getattr(self, "showFields", ())
            ]

        if not getattr(self, "includeEmpties", True):
            all_fields = live_fields
            live_fields = []
            for f in all_fields:
                value = f.htmlValue(request)
                if value and value != "No Input":
                    live_fields.append(f)

        mail_title = self.getTitle_mail()
        mail_plain_body = self.getPlain_mail(wrappedFields=live_fields).strip()
        mail_html_body = self.getHtml_mail(wrappedFields=live_fields).strip()
        mail_from = self.getSender_mail()

        box = self.get_box()
        secret = box.put(obj_to_pobj(REQUEST.form), token=mail_to)
        box.confirm(secret, token=mail_to)

        confirm_url = "%s/confirm-form?secret=%s&email=%s" % (
            self.absolute_url(),
            secret,
            mail_to,
        )

        mail_plain_body = mail_plain_body.replace("[[confirmation_link]]", confirm_url)
        mail_html_body = mail_html_body.replace("[[confirmation_link]]", confirm_url)
        mail_to = self._destFormat(mail_to)
        simple_send_mail(
            mail_plain_body, mail_html_body, [mail_to], mail_from, mail_title
        )


atapi.registerType(ConfirmedFormMailerAdapter, config.PROJECTNAME)
