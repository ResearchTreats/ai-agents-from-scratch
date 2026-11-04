# Lesson 06 quiz

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

**Q8. Lesson 5's server answers an unsupported version with -32022 and a supported list. What does this lesson's connect do with that list?**

- A. Re-raises the MCPError whatever the list holds
- B. Takes the first listed version it also knows and repeats server/discover
- C. Resends the same version with a new id
- D. Falls back to sending initialize

<details><summary>Answer</summary>

**B** - connect keeps the listed versions that are in KNOWN_VERSIONS, sets self.version to the first one and calls server/discover again. It re-raises only when the code is not -32022 or no version is shared.

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

**Q7. In mcp_client.py, what does mcp_tools(client) return for the agent loop?**

- A. A list of tool names printed by the demo
- B. A dict mapping each tool name to a function that calls that tool through the client
- C. A second MCPClient connected to the same server
- D. The subprocess the server runs in

<details><summary>Answer</summary>

**B** - mcp_tools builds {name: remote(name)} for every name from client.list_tools(), and each function calls client.call(name, arguments). The agent loop sees plain local functions.

</details>
