# Security

Sensitive values belong in environment variables or a managed secret store. Provider,
weather and database credentials must not be committed.

The implementation rejects prompt-injection and sensitive-data patterns at the
advisory boundary and requires tool registration plus Pydantic validation. It does not
replace a production WAF, identity provider, authorization policy or secret scanner.
