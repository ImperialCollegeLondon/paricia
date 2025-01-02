# Quality assurance

## Tests

The tests are run with `python manage.py test` from inside the docker container (see the [installation instructions](./installation.md) to see how to do that).

For that to work, development-related dependencies needs to be installed. They should be, already, but if they don't, get into the container and run:

```bash
python -m pip install -r requirements-dev.txt
```

Tests are created using the `unittest` framework. Read the [Testing in Django documentation](https://docs.djangoproject.com/en/5.1/topics/testing/) on how to write tests for a Django application.

### Run selected tests

The above command will run all of the available tests. However, often - especially during debugging - you will want to run only specific tests. To do so, write the tests or group or tests that you want to run using the dot notation to indicate the path to the test:

- Run a specific test, eg. `test_launch_reports_calculation`
```bash
python manage.py test tests.measurement.test_reporting.TestReporting.test_launch_reports_calculation
```
- Run all the tests within a test class, eg. `TestReporting`
```bash
python manage.py test tests.measurement.test_reporting.TestReporting
```
- Run all the tests within a directory, eg. `measurement`, within the `test` directory
```bash
python manage.py test tests.measurement
```

## Continuous integration

### Pre-commit hooks

Pre-commit hooks are set up to run code quality checks (`ruff` and `mypy`) before committing. To run these locally, you will need to `pip install pre-commit` then `pre-commit install`. Now, quality assurance tools will be run automatically with every commit.

### GitHub Workflows

Github workflows are set up to run the following automatically:

- With every push to a branch with a pull request open:
    - Run pre-commit on all files (like running locally `pre-commit run --all-files`). This is done in an external service, [precommit.ci](https://pre-commit.ci/)
    - Run the full tests suite.
    - Check links in the documentation.
    - Build the documentation (not deploying it)
- When a new release is created in GitHub:
    - All of the above, and if successful,
    - The new version of the documentation is published in [GitHub Pages](https://imperialcollegelondon.github.io/paricia/)
    - A docker image is created for Paricia and published to the [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

If any deployment of Paricia is watching for new versions in the registry, the new release might trigger an automated update of such deployment.

Additionally, the Paricia repository is configured to receive automatic upgrades to packages and dependencies via `dependabot` and `pre-commit` bots. Periodically, they will open pull requests with the updated versions and, if the above checks are successful, they will be automatically merged. While sometimes manual intervention is necessary if the updated versions do not work, this process helps to keep Paricia up to date and simplifies the work of maintainers.
