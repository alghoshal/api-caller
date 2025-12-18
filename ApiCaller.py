import httpx
from llama_index.llms.ollama import Ollama
from Utilities import sanitize
import os

BASE_MODEL = os.getenv("BASE_MODEL", "llama3.2:1b")
GUARD_MODEL = os.getenv("GUARD_MODEL", "llama-guard3:1b")

'''
Fetches content from an API for the given endpoint
baseUrl, auth_key, content_id
'''


def fetchContent(baseUrl, authKey, contentId):
    with httpx.Client() as client:
        headers = None
        if authKey is not None:
            headers = {
                k.lower().strip(): v.strip() for
                k, sep, v in
                {(authKey.partition(":") or None),
                    ("User-Agent", ":", "py-api-caller")}
                if v is not None
            }
        resp = client.get(baseUrl + contentId,
                          headers=headers,
                          follow_redirects=True)

        if resp.status_code != 200:
        	content = ""
        	print("Error!! Response code: " + str(resp.status_code))
        	exit(1)
        else:
	        content = resp.json()['data']['attributes']['text']
	        print("Content fetched.")

    return sanitize(content)


'''
Calls an llm with the content
'''


def invokeLlm(content):
    llm = Ollama(
        model=BASE_MODEL,
        request_timeout=600.0,
        context_window=4000,
        retry=1)
    resp = llm.complete(content)
    print("Llm call done.")
    return resp


'''
True if the content is found to be safe and doesn't violate any of 
the MLCommons AI Safety Taxonomies/ Categories 
(ref: Llama Guard & https://mlcommons.org/2024/04/mlc-aisafety-v0-5-poc/)
'''


def isSafe(content):
    # Determines if content is safe using the guard
    guard = Ollama(model=GUARD_MODEL,
                   request_timeout=120.0,
                   context_window=4000,
                   retry=1)
    guardResp = guard.complete(content)
    print("Guardrails: "+guardResp.text)
    return not guardResp.text.startswith("unsafe")


'''
Invokes guardrails pre/ post invokeLlm
Throws Exception if the guardrail fails
'''


def invokeWithGuardrails(content):
    resp = invokeLlm(sanitize(content))
    if isSafe(resp.text):
        return resp
    raise Exception("Input: "+content+", led to unsafe reply: "+resp.text)


'''
Updates content via Http PATCH request to an API call at the given endpoint
baseUrl, auth_key, content_id, fieldName, fieldValue
'''


def updateContent(baseUrl, authKey, contentId, fieldName, fieldValue):
    with httpx.Client() as client:
        headers = None
        if authKey is not None:
            headers = {
                k.strip(): v.strip() for
                k, sep, v in
                {(authKey.partition(":") or None),
                    ("User-Agent", ":", "py-api-caller"),
                    ("Content-Type", ":", "application/json")}
                if v is not None}
        data = "{\"" + fieldName + "\":\"" + fieldValue + "\"}"
        resp = client.patch(baseUrl + contentId,
                            headers=headers,
                            data=data,
                            follow_redirects=True)

        if resp.status_code != 200:
        	print("Error!! Response code: " + str(resp.status_code))
        	print(resp)
        else:
	        print("Content updated.")

    return resp
