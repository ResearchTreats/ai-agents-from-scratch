# Lesson 05 key terms

- **Stateless protocol** - Every request supplies the metadata needed to interpret it
- **Request metadata** - Version, client capabilities, and recommended client identity in `params._meta`
- **`server/discover`** - Mandatory server method for versions, capabilities, instructions, and identity
- **`resultType`** - Discriminator on every successful modern result
- **Protocol era** - Modern per-request metadata or legacy connection-scoped initialization
- **Transport lifetime** - Process, connection, or response-stream lifetime, not protocol session state
- **`-32022`** - Unsupported protocol version error with requested and supported versions
