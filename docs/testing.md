# Testing

## Testing Strategy

## Test-Driven Development (TDD)

### TDD Approach

### Test → Code → Refactor

### TDD Development Evidence

### Test Examples

## Automated Testing

### Model Tests

### Form Tests

### View Tests

### Custom Python Tests


#### Kometa YAML Importer

The Kometa YAML importer uses automated tests to verify that
source configuration files can be read, validated and interpreted
safely before any data is imported into the database.

**YAML Reader — Planned Tests**

| Test ID | Test | Expected result | Status |
|---|---|---|---|
| KOMETA-001 | Load valid YAML | Returns the expected Python data structure | In development |
| KOMETA-002 | Load missing file | Raises FileNotFoundError | Planned |
| KOMETA-003 | Load invalid YAML | Raises a YAML parsing error | Planned |
| KOMETA-004 | Load empty YAML | Handles empty content safely | Planned |
| KOMETA-005 | Detect duplicate keys | Rejects duplicate mapping keys | Planned |

Test outcomes will be recorded after execution. Failed tests and
subsequent fixes will be included in the TDD development evidence.

**KOMETA-001 — Test execution evidence**

- Test: `test_load_valid_yaml`
- Command: `python manage.py test catalogue_import.kometa.tests.test_yaml_reader`
- Result: Passed
- Tests discovered: 1
- Tests passed: 1
- Django system checks: No issues
- Execution time: 0.009 seconds

**Development issue encountered:**

The initial test run failed because the tests directory was
outside the Kometa package. Moving it into
`catalogue_import/kometa/tests/` resolved the issue.
The test was rerun successfully.

**KOMETA-002 — Test execution evidence**

- Test: `test_load_missing_file`
- Expected: `FileNotFoundError`
- Actual: `FileNotFoundError` raised as expected
- Result: Passed
- Total automated tests: 2
- Failures: 0

**KOMETA-003 — Test execution evidence**

- Test: `test_load_invalid_yaml`
- Expected: `yaml.YAMLError`
- Actual: YAML parsing error raised as expected
- Result: Passed
- Total automated tests: 3
- Failures: 0

**KOMETA-004 — Test execution evidence**

- Test: `test_load_empty_yaml`
- Expected: `ValueError`
- Actual: `ValueError` raised as expected
- Result: Passed
- Total automated tests: 4
- Failures: 0

**TDD evidence:**
The initial test failed because the reader returned None
for an empty YAML file. An explicit empty-content check
was implemented, after which all four tests passed.

**KOMETA-005 — Test execution evidence**

- Test: `test_load_duplicate_keys`
- Expected: `yaml.YAMLError` raised when duplicate mapping keys are encountered.
- Actual: `yaml.constructor.ConstructorError` raised as expected. This is a subclass of `yaml.YAMLError`.
- Result: Passed
- Total automated tests: 5
- Tests passed: 5
- Django system checks: No issues
- Execution time: 0.089 seconds

### JavaScript Tests

## Manual Testing

## User Story Acceptance Testing

## Responsive Testing

## Accessibility Testing

## Browser Testing

## Validation

## Bugs Found and Fixed

## Test Results
