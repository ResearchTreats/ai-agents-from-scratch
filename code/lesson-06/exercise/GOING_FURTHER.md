# Lesson 06: going further

Optional extensions, once the exercise passes.

1. Make request put an empty io.modelcontextprotocol/clientCapabilities object and an io.modelcontextprotocol/clientInfo with a name and version into _meta next to the version key. Then remove clientInfo and send tools/list again, and remove clientCapabilities from the second of two requests. Print what the server answers each time and say which fields it needs on every request and which are only recommended.
2. Send tools/list with version='2027-01-01', catch the MCPError, and print e.code and e.data['supported'].
3. Call client.list_tools() twice on the same client and assert both lists are identical and in the same order.
4. In request, raise an error if a successful result's resultType is not 'complete'. Then cache the list_tools result for result['ttlMs'] milliseconds, and write down which users may reuse the cached copy when result['cacheScope'] is 'public' and when it is 'private'.
