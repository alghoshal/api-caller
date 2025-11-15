import os

from ApiCaller import fetchContent, invokeWithGuardrails, updateContent

CMS_API_BASE_URL = os.getenv('CMS_API_BASE_URL', None)
CMS_ENDPOINT_AUTH_KEY = os.getenv('CMS_ENDPOINT_AUTH_KEY', None)
FIELD_NAME_SUMMARY = os.getenv('FIELD_NAME_SUMMARY', 'sum2')
CONTENT_ID=os.getenv('CONTENT_ID', '32')

# Fetch content
content = fetchContent(CMS_API_BASE_URL, CMS_ENDPOINT_AUTH_KEY, CONTENT_ID)

# Summarize
if content is not None:
    summary=invokeWithGuardrails("Summarize the following in less than 40 words (only include the summary in the response): " +content)

# Update summary
if summary is not None:
    finalResponse = updateContent(CMS_API_BASE_URL, CMS_ENDPOINT_AUTH_KEY, CONTENT_ID,FIELD_NAME_SUMMARY,summary.text)