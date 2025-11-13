import os

from ApiCaller import fetchContent, invokeLlm, updateContent

CMS_API_BASE_URL = os.getenv('CMS_API_BASE_URL', None)
CMS_ENDPOINT_AUTH_KEY = os.getenv('CMS_ENDPOINT_AUTH_KEY', None)
TRANSLATION_LANGUAGE = os.getenv('TRANSLATION_LANGUAGE', 'hindi')
CONTENT_ID=os.getenv('CONTENT_ID', '32')

# Fetch content
content = fetchContent(CMS_API_BASE_URL, CMS_ENDPOINT_AUTH_KEY, CONTENT_ID)

# Translate to specified TRANSLATION_LANGUAGE
if content is not None:
    translation=invokeLlm("Translate the following to "+TRANSLATION_LANGUAGE +" (only include the translation in the response): " +content)

print(translation)
# Update translation
if translation is not None:
    finalResponse = updateContent(CMS_API_BASE_URL, CMS_ENDPOINT_AUTH_KEY, CONTENT_ID,TRANSLATION_LANGUAGE,translation.text)