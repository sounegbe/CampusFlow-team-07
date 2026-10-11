# AI Learning Log

## Fellow: 2solo
### Interaction 1 — Input validation and automated tests

Problem: Learn how to validate ticket details and test the function.

My initial understanding:
I understood that validation checks whether ticket details are acceptable. I initially thought it also checked authenticity and permissions. I had not yet learned how to use Python to reject invalid inputs or test those checks automatically.

Prompt to AI:
"i want to start from the ticket.py now give me the step by step command top use"

Useful AI guidance:
The explanation helped me understand how to check ticket inputs before creating a ticket. I learned that strip() removes spaces at the edges, lower() makes text lowercase, and ValueError reports invalid input. I also learned how automated tests check expected results and rejected inputs.

My independent experiment/test:
Ran python3 -m unittest discover -s tests -v locally.

Verification result:
All 6 tests passed.

Decision:
I accepted the suggested validation approach after running the six tests and seeing them pass. The tests checked that valid inputs were cleaned and invalid inputs were rejected. I have not yet independently improved or rejected an AI suggestion.

Related commit:
494848a

What I can now explain without AI:
Use this as a guide, then rewrite it in words you understand:

> **Validation** checks that ticket details follow the rules. For example, the number of affected users must be greater than zero.
>
> **Normalization** makes valid input consistent. For example, `"HIGH"` becomes `"high"`.
>
> **One test:** the blank-title test passes spaces as the title and checks that the function raises `ValueError`. This confirms that an empty title is rejected.

### Interaction 2 — Priority rules: and versus or

Problem:
Understand how urgency and affected-user count determine priority.

My initial understanding:
I predicted that high urgency with 2 users would be low,
and that low urgency with 10 users would be critical.

Prompt to AI:
We discussed predictions for different urgency and user counts.

Useful AI guidance:
"AND" requires all connected conditions/items to be true or included.
"OR" requires at least one condition/option to be true or chosen.

My independent experiment/test:
Ran python3 -m unittest discover -s tests -v.
The priority tests checked high urgency with 2 users,
low urgency with 10 users, and high urgency with 10 users.

Verification result:
These tests passed:
- high + 2 users → high
- low + 10 users → high
- high + 10 users → critical

Decision:
Accepted the explanation after checking the test results.
This corrected my predictions, not an incorrect AI suggestion.

Related commit:
282f65e

What I can now explain without AI:
I check critical first so the most urgent tickets receive the correct priority. Checking high first would return high too early.

### Interaction 3 — Checking existing ticket IDs

Problem:
Check whether the AI-suggested ID generator handles invalid IDs.

My initial understanding:
I thought removing the first letter from every ID was enough
to read its number.

Prompt to AI:
"it should remove every first latter so let's handle it"
Then I asked: "what do you think"

Useful AI guidance:
The original function removed the first character without
checking whether it was T. The AI recommended rejecting
IDs that do not follow our agreed format.

My independent experiment/test:
I ran generate_ticket_id([{"id": "X007"}]).
It returned T008 and left the original list unchanged.

Following AI guidance, I added a malformed-ID test.
The first run reported 6 failures and 2 errors.

I updated the function to check the ID type, T prefix,
at least three ASCII digits, and a number greater than zero.
I also corrected editing mistakes that caused syntax
and import errors.

Verification result:
Ran python3 -m unittest discover -s tests -v.
All 36 tests passed, including the malformed-ID test.

Decision:
I accepted the stricter checks after discussing the problem
and running the tests. This was an AI-guided improvement
that I ran and verified, rather than a flaw I discovered alone.

Related files:
campusflow/tickets.py
tests/test_tickets.py

Related test:
TestTicketID.test_malformed_existing_ids_are_rejected

What I can now explain without AI:
Removing the first letter does not prove an ID is valid.
Checking the format first prevents invalid IDs from being
used to calculate the next ticket number.