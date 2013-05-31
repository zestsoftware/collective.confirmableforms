# The profile id of your package:
PROFILE_ID = 'profile-collective.confirmableforms:default'


def update_workflow(context):
    context.runImportStepFromProfile(PROFILE_ID, 'workflow')
