# Open Source Plan

## Repository Positioning

This repository provides a lightweight, read-only VPS proxy health dashboard for personal use. It is designed for cautious operators who want visibility without changing proxy runtime state.

## Open Source License

The project uses the MIT License.

## README Strategy

The README should stay practical:

- State what the project does in one sentence
- Explain safety boundaries clearly
- Provide a quick start
- Show screenshots after the UI matures
- Keep the roadmap visible

## Issues Strategy

Issues should focus on:

- Read-only health check correctness
- Dashboard usability
- Installation problems
- Safe diagnostic suggestions
- Documentation gaps

Requests for automatic repair, firewall mutation, or proxy configuration editing should be redirected to the non-goals unless a future design explicitly allows opt-in write actions.

## Future Contribution Guide

A future `CONTRIBUTING.md` should define:

- Code style
- Test expectations
- Security and privacy rules
- How to add a checker
- How to avoid sensitive data collection

## Privacy Boundary

The repository must not contain any private IP, domain, token, proxy configuration, UUID, password, subscription link, or private node plaintext.
