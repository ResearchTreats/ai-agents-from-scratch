# Lesson 09: going further

Optional extensions, once the exercise passes.

1. Give run_case an optional judge: a function that asks a model ONE yes-or-no question about the answer (does it tell the customer something the trace does not support?). Label all six CASES' answers yourself first, then run the judge and count where it disagrees with you. Trust it only where it agrees: practitioners keep each judge to one failure mode and check it against human labels before it gates anything.
2. Map lessons 1 through 8's core mechanism to the CASES ticket that would catch it breaking — T4 already covers lesson 8's injection guard (must_not_call=['refund']). Write a new Case for any earlier lesson that doesn't have one yet, and add it to CASES.
3. Measure trajectory efficiency. Wrap a brain in a small class whose reply(messages) calls the real brain and counts the 'Action:' lines it returns. Run each case on its own with run_suite([case], make_helpdesk(counting_brain)), once with the scripted brain and once with OllamaBrain. Write down the fewest steps a person needs for each ticket, and print steps divided by that minimum next to each PASS/FAIL. Where does the real model take a longer path, and does a longer path ever still pass?
