Promp the user to feed in {updated_requirements} and do requirement elicitation 
# Requirement Elicitation

Prompt the user to give the updated requirements ={updated_requirements}

Perform requirement elicitation and make sure that the requirements follow a structure and are not ambiguous, since an ambiguous requirement could cause further issues down the process. [Make sure the user-provided requirements have a clear Actor/Subject, Action Verb, Specific Function/Behaviour, Conditions and Triggers, ASIL safety, Performance Criteria, Constraints and Boundaries, classification explicitly provided, Interface specifications if any, Diagnostic Requirements.] If any of these are not present, query the user for input regarding these. Also give the user an option to continue the modification without these.

Note: The requirements in DOORS .csv's don't correspond to user-given {updated_requirements}. The {updated_requirements}
acts as an update to existing DOORS requirements. Wait for user input after requirement elicitation, then only move to impact analysis.
