import pytest
from Utilities import sanitize

WITH_EMAIL = "hi, the email is abc@g.com. Please send it there. "
WITH_HTML = WITH_EMAIL + "<div class='sdsds' id='abc' onclick='dosomething' />"


def testSanitizeEmail(): assert WITH_EMAIL == sanitize(WITH_EMAIL)


def testSanitizeHtml(): assert WITH_EMAIL == sanitize(WITH_HTML)
