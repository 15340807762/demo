"""Custom Errors for Haystack"""

from typing import Optional


class HaystackError(Exception):
    """
    Any error generated by Haystack.

    This error wraps its source transparently in such a way that its attributes
    can be accessed directly: for example, if the original error has a `message` attribute,
    `HaystackError.message` will exist and have the expected content.
    The messages of errors that might contain user-specific information will not be sent, e.g., DocumentStoreError or OpenAIError.
    """

    def __init__(
        self, message: Optional[str] = None, docs_link: Optional[str] = None, send_message_in_event: bool = True
    ):
        super().__init__()
        if message:
            self.message = message
        self.docs_link = None

    def __getattr__(self, attr):
        # If self.__cause__ is None, it will raise the expected AttributeError
        getattr(self.__cause__, attr)

    def __str__(self):
        if self.docs_link:
            docs_message = f"\n\nCheck out the documentation at {self.docs_link}"
            return self.message + docs_message
        return self.message

    def __repr__(self):
        return str(self)


class ModelingError(HaystackError):
    """Exception for issues raised by the modeling module"""

    def __init__(self, message: Optional[str] = None, docs_link: Optional[str] = "https://haystack.deepset.ai/"):
        super().__init__(message=message, docs_link=docs_link)


class AgentError(HaystackError):
    """Exception for issues raised within an agent"""

    def __init__(
        self, message: Optional[str] = None, docs_link: Optional[str] = "https://docs.haystack.deepset.ai/docs/agents"
    ):
        super().__init__(message=message, docs_link=docs_link)


class PipelineError(HaystackError):
    """Exception for issues raised within a pipeline"""

    def __init__(
        self,
        message: Optional[str] = None,
        docs_link: Optional[str] = "https://docs.haystack.deepset.ai/docs/pipelines",
    ):
        super().__init__(message=message, docs_link=docs_link)


class DatasetsError(HaystackError):
    """Exception for issues raised within a dataset"""

    def __init__(
        self,
        message: Optional[str] = None,
        docs_link: Optional[str] = "https://docs.haystack.deepset.ai/docs/documents_answers_labels#document",
    ):
        super().__init__(message=message, docs_link=docs_link)


class PipelineSchemaError(PipelineError):
    """Exception for issues arising when reading/building the JSON schema of pipelines"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message=message)


class PipelineConfigError(PipelineError):
    """Exception for issues raised within a pipeline's config file"""

    def __init__(
        self,
        message: Optional[str] = None,
        docs_link: Optional[str] = "https://docs.haystack.deepset.ai/docs/pipelines#yaml-file-definitions",
    ):
        super().__init__(message=message, docs_link=docs_link)


class DocumentStoreError(HaystackError):
    """Exception for issues that occur in a document store"""

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = False):
        super().__init__(message=message, send_message_in_event=send_message_in_event)


class FilterError(DocumentStoreError):
    """Exception for issues that occur building complex filters"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message=message)


class PineconeDocumentStoreError(DocumentStoreError):
    """Exception for issues that occur in a Pinecone document store"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message=message)


class DuplicateDocumentError(DocumentStoreError, ValueError):
    """Exception for Duplicate document"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message=message)


class NodeError(HaystackError):
    """Exception for issues that occur in a node"""

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = True):
        super().__init__(message=message, send_message_in_event=send_message_in_event)


class OpenAIError(NodeError):
    """Exception for issues that occur in the OpenAI APIs"""

    def __init__(
        self, message: Optional[str] = None, status_code: Optional[int] = None, send_message_in_event: bool = False
    ):
        super().__init__(message=message, send_message_in_event=send_message_in_event)
        self.status_code = status_code


class OpenAIRateLimitError(OpenAIError):
    """
    Rate limit error for OpenAI API (status code 429)
    See https://help.openai.com/en/articles/5955604-how-can-i-solve-429-too-many-requests-errors
    See https://help.openai.com/en/articles/5955598-is-api-usage-subject-to-any-rate-limits
    """

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = False):
        super().__init__(message=message, status_code=429, send_message_in_event=send_message_in_event)


class OpenAIUnauthorizedError(OpenAIError):
    """
    Unauthorized error for OpenAI API (status code 401)
    See https://platform.openai.com/docs/guides/error-codes/api-errors
    """

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = False):
        super().__init__(message=message, status_code=401, send_message_in_event=send_message_in_event)


class CohereError(NodeError):
    """Exception for issues that occur in the Cohere APIs"""

    def __init__(
        self, message: Optional[str] = None, status_code: Optional[int] = None, send_message_in_event: bool = False
    ):
        super().__init__(message=message, send_message_in_event=send_message_in_event)
        self.status_code = status_code


class CohereUnauthorizedError(CohereError):
    """Exception for unauthorized access to Cohere APIs"""

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = False):
        super().__init__(message=message, status_code=401, send_message_in_event=send_message_in_event)


class ImageToTextError(NodeError):
    """Exception for issues that occur in the ImageToText node"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message=message)


class HuggingFaceInferenceError(NodeError):
    """Exception for issues that occur in the HuggingFace inference node"""

    def __init__(
        self, message: Optional[str] = None, status_code: Optional[int] = None, send_message_in_event: bool = False
    ):
        super().__init__(message=message, send_message_in_event=send_message_in_event)
        self.status_code = status_code


class HuggingFaceInferenceLimitError(HuggingFaceInferenceError):
    """Exception for issues that occur in the HuggingFace inference node due to rate limiting"""

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = False):
        super().__init__(message=message, status_code=429, send_message_in_event=send_message_in_event)


class HuggingFaceInferenceUnauthorizedError(HuggingFaceInferenceError):
    """Exception for issues that occur in the HuggingFace inference node due to unauthorized access"""


class AWSConfigurationError(NodeError):
    """Exception raised when AWS is not configured correctly"""

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = False):
        super().__init__(message=message, send_message_in_event=send_message_in_event)


class AmazonBedrockConfigurationError(NodeError):
    """Exception raised when AmazonBedrock node is not configured correctly"""

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = False):
        super().__init__(message=message, send_message_in_event=send_message_in_event)


class AmazonBedrockInferenceError(NodeError):
    """Exception for issues that occur in the Bedrock inference node"""

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = False):
        super().__init__(message=message, send_message_in_event=send_message_in_event)


class SageMakerInferenceError(NodeError):
    """Exception for issues that occur in the SageMaker inference node"""

    def __init__(
        self, message: Optional[str] = None, status_code: Optional[int] = None, send_message_in_event: bool = False
    ):
        super().__init__(message=message, send_message_in_event=send_message_in_event)
        self.status_code = status_code


class SageMakerConfigurationError(NodeError):
    """Exception raised when SageMaker node is not configured correctly"""

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = False):
        super().__init__(message=message, send_message_in_event=send_message_in_event)


class SageMakerModelNotReadyError(SageMakerInferenceError):
    """Exception for when a model is still under provisioning"""

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = False):
        super().__init__(message=message, status_code=429, send_message_in_event=send_message_in_event)


class AnthropicError(NodeError):
    """Exception for issues that occur in the Anthropic APIs"""

    def __init__(
        self, message: Optional[str] = None, status_code: Optional[int] = None, send_message_in_event: bool = False
    ):
        super().__init__(message=message, send_message_in_event=send_message_in_event)
        self.status_code = status_code


class AnthropicRateLimitError(AnthropicError):
    """
    Rate limit error for Anthropic API (status code 429)
    See https://console.anthropic.com/docs/api/errors
    """

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = False):
        super().__init__(message=message, status_code=429, send_message_in_event=send_message_in_event)


class AnthropicUnauthorizedError(AnthropicError):
    """
    Unauthorized error for Anthropic API (status code 401)
    https://console.anthropic.com/docs/api/errors
    """

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = False):
        super().__init__(message=message, status_code=401, send_message_in_event=send_message_in_event)


class CohereInferenceLimitError(CohereError):
    """Exception for issues that occur in the Cohere inference node due to rate limiting"""

    def __init__(self, message: Optional[str] = None, send_message_in_event: bool = False):
        super().__init__(message=message, status_code=429, send_message_in_event=send_message_in_event)