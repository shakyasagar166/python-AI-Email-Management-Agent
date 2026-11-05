"""
Custom Domain Exceptions for AI Email Management Agent
"""

class MailMindException(Exception):
    def __init__(self, message="An internal email management error occurred.", status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class EmailNotFoundException(MailMindException):
    def __init__(self, message="Email record was not found."):
        super().__init__(message, status_code=404)


class UserNotFoundException(MailMindException):
    def __init__(self, message="User profile was not found."):
        super().__init__(message, status_code=404)


class DuplicateUserException(MailMindException):
    def __init__(self, message="A user with this email already exists."):
        super().__init__(message, status_code=409)


class CategoryNotFoundException(MailMindException):
    def __init__(self, message="Email category was not found."):
        super().__init__(message, status_code=404)


class DraftNotFoundException(MailMindException):
    def __init__(self, message="Email draft was not found."):
        super().__init__(message, status_code=404)


class RuleNotFoundException(MailMindException):
    def __init__(self, message="Automation rule was not found."):
        super().__init__(message, status_code=404)


class AuthenticationException(MailMindException):
    def __init__(self, message="Authentication credential is invalid or expired."):
        super().__init__(message, status_code=401)


class AIServiceException(MailMindException):
    def __init__(self, message="AI LLM inference service encountered an error."):
        super().__init__(message, status_code=502)


class ValidationException(MailMindException):
    def __init__(self, message="Validation failed on submitted payload."):
        super().__init__(message, status_code=422)
