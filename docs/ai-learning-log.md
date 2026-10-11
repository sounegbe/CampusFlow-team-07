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