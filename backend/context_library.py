#backend/context_library.py
CPI_STANDARD_HEADERS = [
    "CamelHttpUri",
    "CamelHttpPath",
    "CamelHttpMethod",
    "CamelHttpResponseCode",
    "CamelHttpQuery",
    "CamelAuthentication",
    "SAP_RECEIVER",
    "SAP_Sender",
    "CamelHttpContentType",
    "CamelHttpCharacterEncoding",
    "CamelHttpUserAgent"
]

CPI_SPECIALIZED_CONTEXTS = {
    "xml_json": """
    For XML to JSON / JSON to XML transformations:
    *  Always use `groovy.json.JsonSlurper` and `groovy.json.JsonOutput` or `groovy.util.XmlSlurper`.
    * Ensure `XmlSlurper` disbales external DTD processing to prevent XXE VULNERABILITIES:
      def parser = new XmlSlurper(false, false)
      parser.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)
    """,
    "logging": """
    For logging in Groovy scripts: 
    * Fetch messageLog using `def messageLog = messageLogFactory.getMessageLog(message)`.
    * Use `messageLog` to log messages at different levels:
      - `messageLog.setStringProperty("logLevel", "INFO")` for INFO level
      - `messageLog.setStringProperty("logLevel", "DEBUG")` for DEBUG level
      - `messageLog.setStringProperty("logLevel", "ERROR")` for ERROR level

    * Log messages using `messageLog.addAttachmentAsString("Payload Log", body,'text/plain')`.
    * always add attchments with proper content type, e.g., 'text/plain' for text, 'application/json' for JSON, etc.
    """,
    "secure_store": """
    For secure store access in Groovy scripts:
    * Use `com.sap.it.api.ITApiFactory` and `com.sap.it.api.SecureStore.SecureStoreService` to access the secure store
    * Example:
      def secureStoreService = com.sap.it.api.ITApiFactory.getApi(SecureStoreService.class, null)
      def secureStoreEntry = secureStoreService.getSecureStoreEntry("MySecureStoreEntry")
      def password = secureStoreEntry.getPassword()
    * Always handle sensitive data securely and avoid logging passwords or sensitive information.
      """,
    "error_handling": """
    For error handling in Groovy scripts:
    * Retriee the caught Camel Exception using :
    def ex = message.getProperty("CamelExceptionCaught"):
    * Read the exception message using `ex.getMessage()` 
    * Read the root cause safely without throwing null pointer exceptions using:
    """
}
def detect_specialized_context(user_prompt: str) -> str:
    """
    Detects specialized context based on keywords in the user prompt.
    Returns the context key if found, otherwise returns None.
    """
    injected_instructions = []
    user_prompt_lower = user_prompt.lower()
    if any(keyword in user_prompt_lower for keyword in ["xml", "json", "xml to json", "json to xml"]):
        injected_instructions.append(CPI_SPECIALIZED_CONTEXTS["xml_json"])
    if any(keyword in user_prompt_lower for keyword in ["log", "logging", "message log"]):
        injected_instructions.append(CPI_SPECIALIZED_CONTEXTS["logging"])
    if any(keyword in user_prompt_lower for keyword in ["secure store", "password", "credentials"]):
        injected_instructions.append(CPI_SPECIALIZED_CONTEXTS["secure_store"])
    if any(keyword in user_prompt_lower for keyword in ["error handling", "exception", "try catch"]):
        injected_instructions.append(CPI_SPECIALIZED_CONTEXTS["error_handling"])
    return injected_instructions