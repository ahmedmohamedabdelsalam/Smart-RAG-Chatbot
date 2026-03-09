# Contributing to MySmartRAG-Bot

Thank you for your interest in contributing to MySmartRAG-Bot! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. Please be respectful and professional in all interactions.

## How Can I Contribute?

### Reporting Bugs
- Check if the bug has already been reported in [Issues](https://github.com/AhmedAbdelsalam/MySmartRAG-Bot/issues)
- If not, create a new issue with a clear title and description
- Include steps to reproduce, expected behavior, and actual behavior
- Add relevant logs, screenshots, or workflow JSON if applicable

### Suggesting Enhancements
- Open an issue with the tag `enhancement`
- Clearly describe the feature and its benefits
- Provide examples or mockups if possible

### Adding New Workflows
- Create workflows following n8n best practices
- Use clear, descriptive node names
- Add comprehensive workflow documentation
- Include example configurations and test data
- Place workflow in the appropriate category directory

### Improving Documentation
- Fix typos, clarify instructions, or add missing information
- Add examples and use cases
- Create tutorials or guides
- Update API references

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/AhmedAbdelsalam/MySmartRAG-Bot.git
   cd MySmartRAG-Bot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

3. **Set Up Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   python scripts/setup_wizard.py
   ```

4. **Run Tests**
   ```bash
   npm test
   pytest tests/
   ```

## Coding Standards

### Python Code
- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where applicable
- Write docstrings for functions and classes
- Keep functions focused and under 50 lines when possible
- Use meaningful variable and function names

Example:
```python
def validate_workflow(workflow_path: str) -> bool:
    """
    Validate an n8n workflow JSON file.
    
    Args:
        workflow_path: Path to the workflow JSON file
        
    Returns:
        True if workflow is valid, False otherwise
    """
    # Implementation here
    pass
```

### Workflow JSON
- Use descriptive workflow names
- Add meaningful node labels
- Include sticky notes for documentation
- Use consistent naming conventions
- Add metadata for categorization

### Documentation
- Use clear, concise language
- Include code examples where relevant
- Keep line length under 100 characters
- Use proper markdown formatting
- Add table of contents for long documents

## Submitting Changes

### Pull Request Process

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   python scripts/workflow_validator.py --check-all
   pytest tests/
   ```

4. **Commit with Clear Messages**
   ```bash
   git commit -m "feat: Add workflow for X feature"
   ```
   
   Commit message format:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `refactor:` Code refactoring
   - `test:` Adding tests
   - `chore:` Maintenance tasks

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a pull request on GitHub with:
   - Clear title and description
   - Reference to related issues
   - Summary of changes
   - Testing performed

6. **Code Review**
   - Address review comments
   - Make requested changes
   - Keep discussion professional and constructive

### What to Include in PR
- [ ] Description of changes
- [ ] Tests for new functionality
- [ ] Updated documentation
- [ ] No breaking changes (or clearly documented)
- [ ] Follows coding standards
- [ ] Passes all tests

## Project Structure

```
MySmartRAG-Bot/
├── workflows/           # n8n workflow JSON files (categorized)
├── scripts/             # Python utility scripts
├── docs/                # Detailed documentation
├── examples/            # Example configurations and templates
├── assets/              # Media, diagrams, screenshots
├── tests/               # Automated tests
├── README.md            # Main project documentation
├── CHANGELOG.md         # Version history
└── CONTRIBUTING.md      # This file
```

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the `question` tag
- Reach out to the maintainer
- Check existing documentation in the `docs/` directory

Thank you for contributing to MySmartRAG-Bot!
