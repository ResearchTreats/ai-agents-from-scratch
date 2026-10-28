# Lesson 05 quiz

Answer first, then open the answer.

## Before you start

**Q1. What creates protocol state between two MCP 2026-07-28 requests?**

- A. The HTTP connection
- B. Nothing in the protocol core
- C. Mcp-Session-Id
- D. The stdio process

<details><summary>Answer</summary>

**B** - The modern protocol core is stateless. Each request carries its own version and capabilities.

</details>

## Check yourself

**Q2. Which two params._meta fields are required on every modern request?**

- A. clientInfo and cacheScope
- B. protocolVersion and clientCapabilities
- C. sessionId and capabilities
- D. serverInfo and ttlMs

<details><summary>Answer</summary>

**B** - Protocol version and client capabilities are required. Client identity is recommended.

</details>

**Q3. What method must every modern MCP server implement for up-front discovery?**

- A. tools/list
- B. initialize
- C. server/discover
- D. notifications/initialized

<details><summary>Answer</summary>

**C** - server/discover advertises supported versions, capabilities, instructions, and server identity.

</details>

**Q4. What does error code -32022 mean?**

- A. Internal error
- B. Header mismatch
- C. Method not found
- D. Unsupported protocol version

<details><summary>Answer</summary>

**D** - UnsupportedProtocolVersionError includes the requested version and the versions the server supports.

</details>

**Q7. Lesson 4's tool_use_id correlated each tool result with the call that produced it. In this lesson's mcp_server.py, what plays that same correlating role between a JSON-RPC request and its reply?**

- A. The jsonrpc field
- B. The method string
- C. The id field
- D. The params._meta object

<details><summary>Answer</summary>

**C** - Just like tool_use_id in lesson 4, the JSON-RPC id from the request is echoed back unchanged in result()/error()'s {'jsonrpc': '2.0', 'id': request_id, ...}, so a client matches each reply to the call that produced it; a notification has no id and gets no reply at all.

</details>

## After the lesson

**Q5. Which result requires ttlMs and cacheScope in MCP 2026-07-28?**

- A. A JSON-RPC error
- B. A tools/list result
- C. A tools/call result
- D. A cancellation notification

<details><summary>Answer</summary>

**B** - List results and resources/read are cacheable results with required cache hints.

</details>

**Q6. How should a server choose capabilities for the current request?**

- A. Read them from Mcp-Session-Id
- B. Infer them from the process
- C. Reuse the first request's declaration
- D. Read them from the current request metadata

<details><summary>Answer</summary>

**D** - A server must not infer modern capabilities from connection or previous-request state.

</details>
