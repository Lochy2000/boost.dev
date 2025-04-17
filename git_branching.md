# Git Branching Explained

This document explains how to perform common Git branching operations.

## 1. Create a New Branch

To create a new branch, use the following command:

```bash
git branch <branch_name>
```

**Example:**

To create a branch named "feature/new-feature", run:

```bash
git branch feature/new-feature
```

## 2. Switch to a Branch

To switch to an existing branch, use the following command:

```bash
git checkout <branch_name>
```

**Example:**

To switch to the "feature/new-feature" branch, run:

```bash
git checkout feature/new-feature
```

Alternatively, you can create and switch to a new branch in one step using:

```bash
git checkout -b <branch_name>
```

**Example:**

```bash
git checkout -b feature/new-feature
```

## 3. Switch Back to the Main Branch

To switch back to the main branch (usually named "main" or "master"), use the following command:

```bash
git checkout main
```

or

```bash
git checkout master
```

**Example:**

```bash
git checkout main
```

## 4. Switch Back to the Local Branch

To switch back to your local branch, use the same `git checkout` command with your branch name:

```bash
git checkout <branch_name>
```

**Example:**

To switch back to the "feature/new-feature" branch, run:

```bash
git checkout feature/new-feature
```

## 5. Push the Local Branch to GitHub

To push your local branch to GitHub, use the following command:

```bash
git push -u origin <branch_name>
```

**Explanation:**

*   `git push`:  The command to push your local changes to a remote repository.
*   `-u origin`: Sets the upstream branch for your local branch. This means that Git will remember the relationship between your local branch and the remote branch.
*   `<branch_name>`: The name of your branch.

**Example:**

To push the "feature/new-feature" branch to GitHub, run:

```bash
git push -u origin feature/new-feature
```

After the first push with the `-u` option, you can simply use `git push` to push subsequent changes.