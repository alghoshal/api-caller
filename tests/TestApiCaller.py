import pytest
from ApiCaller import isSafe, invokeWithGuardrails


def testIsSafe(): assert isSafe("hi")


def testIsUnSafe(): assert not isSafe("hi, the email is abc@g.com")


def testIsUnSafeWithJson():
	assert not isSafe("""CompletionResponse: To format the given text in a valid JSON, I'll use the following structure:

	```
	{
	  "email": "abc@g.com",
	  "username": "ixxx@dsds.in"
	}
	```
	""")


def testinvokeWithGuardrailsUnsafe():
	try:
		resp = invokeWithGuardrails(
			"Format the following text in a valid json, only respond with the json and nothing else: \"the email is abc@g.com and ixxx@dsds.in\"")
		assert False  # Exception should be thrown
	except Exception as e:
		assert True  # Exception should be thrown


def testinvokeWithGuardrailsSafe():
	resp = invokeWithGuardrails(
		"Format the following text in a valid json, only respond with the json and nothing else: \"the length is 30cm and breadth is 40cm\"")
	assert resp is not None
