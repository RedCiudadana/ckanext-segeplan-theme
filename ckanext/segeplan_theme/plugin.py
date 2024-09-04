from __future__ import annotations

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.types import Schema
from ckan.common import CKANConfig


def homepage_values_helper():
    homepage_config = {
        'homepage_what_is': toolkit.config.get('ckanext.segeplan_theme.homepage_what_is'),
        'homepage_guide': toolkit.config.get('ckanext.segeplan_theme.homepage_guide'),
        'homepage_events': toolkit.config.get('ckanext.segeplan_theme.homepage_events'),
    }

    print(homepage_config)

    return homepage_config


class SegeplanThemePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, "public")
        toolkit.add_resource("assets", "segeplan_theme")

        # [IBlueprint#todo] We can add custom tabs and page with this. For now disabled.
        # Add a new ckan-admin tabs for our extension
        # toolkit.add_ckan_admin_tab(
        #     config, u'segeplan_theme.config_homepage',
        #     u'Home page texts'
        # )

    def update_config_schema(self, schema: Schema):

        ignore_missing = toolkit.get_validator('ignore_missing')
        unicode_safe = toolkit.get_validator('unicode_safe')
        is_positive_integer = toolkit.get_validator('is_positive_integer')

        schema.update({
            # This is a custom configuration option
            u'ckanext.segeplan_theme.homepage_what_is': [ignore_missing, unicode_safe],
            u'ckanext.segeplan_theme.homepage_guide': [ignore_missing, unicode_safe],
            u'ckanext.segeplan_theme.homepage_events': [ignore_missing, unicode_safe],
        })

        return schema

    # # IBlueprint

    # [IBlueprint#todo] We can add custom tabs and page with this. For now disabled.
    # def get_blueprint(self):
    #     return blueprint.segeplan_theme

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self) -> list[str]:
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def get_helpers(self):
        return {'segeplan_theme_homepage_values': homepage_values_helper}