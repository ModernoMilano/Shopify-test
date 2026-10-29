"""'From our community': a Community review metaobject (filled in the admin, genuine comments only) and the
cc-community section. The section is placed on every product template (product_templates.py) and the homepage
(homepage.py); it stays invisible until the first entry exists."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check, put_theme_files

if not gql('{metaobjectDefinitionByType(type:"$app:community_review"){id}}')["metaobjectDefinitionByType"]:
    check(gql("""mutation($d:MetaobjectDefinitionCreateInput!){metaobjectDefinitionCreate(definition:$d){metaobjectDefinition{id} userErrors{field message}}}""",
        {"d": {"type": "$app:community_review", "name": "Community review", "displayNameKey": "author",
               "description": "A genuine customer comment (e.g. from Instagram) for the 'From our community' section.",
               "access": {"admin": "MERCHANT_READ_WRITE", "storefront": "PUBLIC_READ"}, "capabilities": {"publishable": {"enabled": True}},
               "fieldDefinitions": [
                   {"key": "author", "name": "Name", "type": "single_line_text_field", "required": True},
                   {"key": "instagram", "name": "Instagram handle", "type": "single_line_text_field"},
                   {"key": "body", "name": "Comment", "type": "multi_line_text_field", "required": True},
                   {"key": "rating", "name": "Rating (only if the customer gave one)", "type": "rating",
                    "validations": [{"name": "scale_min", "value": "1"}, {"name": "scale_max", "value": "5"}]},
                   {"key": "product", "name": "Product it is about", "type": "product_reference"},
                   {"key": "photo", "name": "Customer photo", "type": "file_reference", "validations": [{"name": "file_type_options", "value": "[\"Image\"]"}]},
                   {"key": "source_url", "name": "Link to the original comment", "type": "url"}]}})["metaobjectDefinitionCreate"], "definition")
    print("created metaobject definition $app:community_review")
print(put_theme_files({"sections/cc-community.liquid": open(os.path.join(S, "cc-community.liquid")).read()}))
