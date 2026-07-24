# Learning Journal

Repository: `python-fundamentals`  
Programme: Loadberry Ltd AI Engineering Trainee Programme  
Month: Month One  
Focus: Week Two - Professional Python Engineering, OOP, dataclasses, type hints, validation, testing, Git branching and PR workflow

---

## Session 01 - Repository Setup and Branch Workflow

#### What was worked on
- The `python-fundamentals` repository was created on GitHub.
- The repository was cloned locally under `~/projects/python-fundamentals`.
- Python 3.13.14 was configured using `pyenv`.
- A local `.venv` virtual environment was created.
- `pytest` was installed for automated testing.
- A `src/` project layout was created.
- A `pyproject.toml` file was added for editable package installation.
- Git feature branches were introduced instead of committing directly to `main`.

#### What was learned
- A separate repository helps keep OOP foundation practice separate from the `developer-toolkit` CLI tools.
- `pyenv local 3.13.14` creates a `.python-version` file for project-specific Python version control.
- A `.venv` environment isolates project dependencies.
- `pyproject.toml` allows the package to be installed in editable mode using `python -m pip install -e .`.
- Feature branches allow work to be developed safely before merging into `main`.
- Pull Requests provide a reviewable summary of code changes before merging.

#### Issues encountered
- The workflow initially used direct commits to `main` in the previous repository.
- Feature branch and Pull Request workflow was introduced to build more professional Git confidence.

#### Questions for mentor
- Should every feature be developed through a Pull Request, even for solo practice projects? Personally I thinks so even if it is only for practice purpose.


## Session 02 - Student Model

#### What was worked on
- A `Student` dataclass was implemented in `src/student_records/models.py`.
- A custom `StudentValidationError` exception was added.
- Student fields were defined for `student_id`, `name`, `email`, and `grades`.
- Validation was added for required fields, email format, and grade values.
- Methods were added for adding grades, calculating average grade, checking pass/fail status, and exporting a student summary as a dictionary.
- Pytest tests were added for the Student model.

#### What was learned
- `@dataclass` reduces boilerplate when creating simple data-focused classes.
- `field(default_factory=list)` is safer than using a mutable list as a default value.
- `__post_init__()` can be used to clean and validate data after object creation.
- Custom exceptions make validation errors clearer and easier to test.
- Type hints make the class easier to understand and maintain.
- Unit tests can verify both successful behaviour and expected validation failures.

#### Test results
- 14 Student model tests passed.
- Tests covered:
  - student creation
  - text field cleaning
  - required field validation
  - email validation
  - grade validation
  - average grade calculation
  - pass/fail logic
  - dictionary export

#### Issues encountered
- A typo was found in the first commit message and Pull Request title: `wiht` instead of `with`.
- The PR title was edited on GitHub.
- The commit message was corrected using `git commit --amend`.
- The corrected commit was pushed safely to the feature branch using `git push --force-with-lease`.

#### Questions for mentor
-none as of yet


## Session 03 - Student Records Manager

#### What was worked on
- A `StudentRecords` manager class was implemented in `src/student_records/records.py`.
- A custom `StudentRecordsError` exception was added.
- The manager was designed to store students by `student_id`.
- Methods were added for adding, retrieving, removing, listing, and searching students.
- Grade updates were supported through the records manager.
- Class average calculation was added.
- A dictionary summary export method was added.
- Pytest tests were added for the records manager.

#### What was learned
- A dictionary is useful for storing records by unique ID.
- A manager class helps separate collection-level behaviour from individual object behaviour.
- Duplicate student IDs should be rejected to protect data integrity.
- Search and lookup functions should clean user input before matching.
- List comprehensions can be used to build sorted and filtered student lists.
- Full workflow tests help confirm that multiple methods work together correctly.

#### Test results
- 26 tests passed in total.
- 12 StudentRecords manager tests passed.
- Existing Student model tests continued to pass.
- Tests covered:
  - adding students
  - rejecting duplicate IDs
  - retrieving students
  - removing students
  - adding grades to existing students
  - sorted student listing
  - name search
  - email lookup
  - class average calculation
  - dictionary summary export

#### Issues encountered
- No major implementation issue was encountered during the StudentRecords manager tests.

#### Questions for mentor
- Should the records manager support updating student details later?
- Should student search support multiple fields, such as name and email together?


## Session 04 - JSON Storage for Student Records

#### What was worked on
- A JSON storage module was implemented in `src/student_records/storage.py`.
- A custom `StudentStorageError` exception was added.
- Functions were added to convert `Student` objects into JSON-serialisable dictionaries.
- Functions were added to rebuild `Student` objects from stored dictionary data.
- Functions were added to save and load `StudentRecords` using JSON files.
- Validation was added for missing files, invalid JSON, missing fields, invalid grades, and invalid stored structure.
- An example `students.json` file was added under `examples/`.
- Pytest tests were added for storage behaviour.

#### What was learned
- JSON storage allows records to persist after the program exits.
- `json.dumps()` can convert Python dictionaries into formatted JSON text.
- `json.loads()` can convert JSON text back into Python data.
- Storage code should validate external data carefully before creating application objects.
- `Path` from `pathlib` is useful for reading and writing files.
- Round-trip tests are useful for confirming that saved data can be loaded back correctly.

#### Test results
- 34 tests passed in total.
- 8 JSON storage tests passed.
- Existing Student model and StudentRecords manager tests continued to pass.
- Tests covered:
  - converting students to dictionaries
  - creating students from stored data
  - rejecting missing required fields
  - rejecting invalid grades
  - saving and loading records
  - rejecting missing files
  - rejecting invalid JSON
  - rejecting missing students list

#### Issues encountered
- The storage test file was initially created under a nested path: `tests/test/test_storage.py`.
- The file was moved to the cleaner location: `tests/test_storage.py`.
- The old nested folder could not be removed with `rmdir` because it contained a `__pycache__` folder.
- The nested folder was removed using `rm -rf tests/test`.

#### Questions for mentor
- Is JSON storage sufficient for this stage, or should SQLite be introduced later?
- Should storage functions support backup files before overwriting existing data?
- Should future versions include CSV import/export?