from dynamic_preferences.types import BooleanPreference, IntegerPreference
from dynamic_preferences.registries import global_preferences_registry

@global_preferences_registry.register
class SpoonacularApiEnabled(BooleanPreference):
    name = 'spoonacular_api_enabled'
    default = True
    help_text = 'Enable/Disable Spoonacular API'

@global_preferences_registry.register
class GoogleCustomSearchApiEnabled(BooleanPreference):
    name = 'google_custom_search_api_enabled'
    default = True
    help_text = 'Enable/Disable Google Custom Search API'

@global_preferences_registry.register
class TimeBetweenApiCalls(IntegerPreference):
    name = 'time_between_api_calls'
    default = 5
    help_text = 'Time in seconds between API calls (in seconds)'