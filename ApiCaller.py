import os
import httpx

CMS_API_BASE_URL = os.getenv('CMS_API_BASE_URL', None)
CMS_ENDPOINT_AUTH_KEY = os.getenv('CMS_ENDPOINT_AUTH_KEY', None)
FIELD_NAME_SUMMARY = os.getenv('FIELD_NAME_SUMMARY', 'sum2')
CONTENT_ID="32"

'''
Fetches content from an API for the given enpoint
baseUrl, auth_key, content_id
'''
def fetchContent(baseUrl, authKey, contentId):
    with httpx.Client( # Talk to CMS 
        # enable HTTP2 support 
        # http2=True, 
        # set headers for all requests 
        # headers={"x-secret": "foo"} 
        # max_redirects=2,
        ) as client:
        headers = None
        if authKey is not None:
            headers = {
                k.lower().strip():v.strip() for 
                k, sep, v in 
                {(authKey.partition(":") or None), 
                    ("User-Agent", ":", "py-api-caller")} if 
                v is not None}
        resp = client.get(baseUrl + contentId, 
            headers=headers, 
            follow_redirects=True)
        
        if resp.status_code != 200: 
        	content = "";
        	print("Error!! Response code: "+str(resp.status_code))
        	exit(1)
        else:
	        content = resp.json()['data']['attributes']['text']
	        print("Content fetched.")
	    
    return content

'''
Invokes a llm to summarize the content
'''
def summarize(content):
    from llama_index.llms.ollama import Ollama # Get LLM to Summarize
    llm = Ollama(
        model="llama3.2:1b", 
        request_timeout=600.0, 
        context_window=4000,
        retry=2)
    resp = llm.complete("Summarize the following in less than 40 words (only include the summary in the response): " + content)
    print("Summarizing Done.")
    return resp

'''
Updates content via Http PATCH request to an API call at the given enpoint
baseUrl, auth_key, content_id, fieldName, fieldValue
'''
def updateContent(baseUrl, authKey, contentId, fieldName, fieldValue):
    with httpx.Client( # Talk to CMS 
        # enable HTTP2 support 
        # http2=True, 
        # set headers for all requests 
        # headers={"x-secret": "foo"} 
        # max_redirects=2,
        ) as client:
        headers = None
        if authKey is not None:
            headers = {
                k.strip():v.strip() for 
                k, sep, v in 
                {(authKey.partition(":") or None), 
                    ("User-Agent", ":", "py-api-caller"),
                    ("Content-Type",":","application/json")} if 
                v is not None}
        data = "{\""+fieldName+"\":\""+fieldValue+"\"}"
        resp = client.patch(baseUrl + contentId, 
            headers=headers, 
            data=data,
            follow_redirects=True)
        
        if resp.status_code != 200: 
        	print("Error!! Response code: "+str(resp.status_code))
        	print(resp)
        else:
	        print("Content updated.")
	    
    return resp

# Fetch content
content = fetchContent(CMS_API_BASE_URL, CMS_ENDPOINT_AUTH_KEY, CONTENT_ID)

# Summarize
if content is not None:
    summary=summarize(content)

# Update summary
if summary is not None:
    finalResponse = updateContent(CMS_API_BASE_URL, CMS_ENDPOINT_AUTH_KEY, CONTENT_ID,FIELD_NAME_SUMMARY,summary.text)