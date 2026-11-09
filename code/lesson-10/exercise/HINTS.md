# Lesson 10 exercise: hints

Open one hint at a time, only when you are stuck.

<details><summary>Hint 1</summary>

Open exercise_10.py. TEAMS is just a dict that classify() and scoped() both read - add_returns_team() needs to add one more entry to it, shaped exactly like the 'tech' or 'shipping' entries already in supervisor.py: a 'words' list and a 'tools' list.

</details>

<details><summary>Hint 2</summary>

test_exercise_10.py checks TEAMS['returns']['tools'] == ['lookup_order', 'search_help'] and that classify(RETURN_TICKET['text']) == 'returns'. Look at RETURN_TICKET's text - 'I want to return my jacket from order A17. It does not fit.' - and pick 'words' for the returns team that actually appear in that sentence, the same way 'shipping' matches words like 'order' and 'deliver'.

</details>

<details><summary>Hint 3</summary>

In add_returns_team(), set TEAMS['returns'] = {'words': ['return', 'fit', 'exchange', 'size'], 'tools': ['lookup_order', 'search_help']} - classify() will then score 'returns' above every other team for RETURN_TICKET, and Supervisor(ScriptedBrain(), helpdesk_tools()).handle(RETURN_TICKET) will route it there since scoped() can build a ToolBox from any team name now present in TEAMS.

</details>
