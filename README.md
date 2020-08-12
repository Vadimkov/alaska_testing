# alaska_testing
## Prerequisites
Docker image https://hub.docker.com/r/azshoo/alaska should be uploaded and the user should have permissions for run docker containers.

## Commentaries
Every test runs a separate container for testing. It makes tests slow. But it makes tests more clear and independent.
But the current solution allows running tests in several processes for decrease time of testing.
Other ways to speed up tests:
- use one instance for all tests, but delete all notes in the test fixture;
- use other test architecture with depended tests (like in the first group of tests in the test_plan.md)