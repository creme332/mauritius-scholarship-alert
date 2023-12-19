# Code Conventions

## Introduction
This document outlines the coding conventions and standards to be followed while writing code for `mauritius-scholarship-alert`. Consistent adherence to these conventions ensures readability, maintainability, and a unified coding style across the project.

## Table of Contents
- [Code Conventions](#code-conventions)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Naming Conventions](#naming-conventions)
  - [Formatting](#formatting)
  - [Imports](#imports)
  - [Functions and Methods](#functions-and-methods)
  - [Error Handling](#error-handling)
  - [Documentation](#documentation)
  - [Testing](#testing)

## Naming Conventions
- Variables: Use descriptive names following snake_case (e.g., `user_profile`)
- Constants: Uppercase with underscores separating words (e.g., `MAX_RETRY_COUNT`)
- Functions and Methods: Use lowercase with words separated by underscores (e.g., `calculate_discount`)
- Classes: Use CamelCase (e.g., `UserProfileManager`)

## Formatting
- Use `autopep8` formatter.

## Imports
- Import each module on a separate line
- Use absolute imports whenever possible

## Functions and Methods
- Keep functions and methods concise with a single responsibility
- Use meaningful names reflecting the function's purpose

## Error Handling
- Handle exceptions gracefully and provide informative error messages
- Avoid catching generic exceptions unless necessary

## Documentation
- Include docstrings for modules, classes, functions, and methods
- Follow the Google Style Python Docstrings format for documenting functions and classes

## Testing
- Write unit tests for all functions and methods
- Ensure tests cover edge cases and expected behaviors

