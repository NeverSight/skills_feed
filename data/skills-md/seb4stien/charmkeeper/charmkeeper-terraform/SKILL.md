---
name: charmkeeper-terraform
description: Use this skill when asked to write, test or fix terraform modules for a charm.
---

Plan:

- Find the terraform modules in the repository.
- Ensure each terraform module is following the implementation standards.
- Run the tests to ensure the modules work as expected.

# Implementation standards

- Expected versions:

  - `terraform`: ~> 1.12
  - `juju provider`: ~> 1.0

- The module should only have a "model_uuid" variable, no "model" variable.
- Lint terraform modules with `terraform fmt --recursive` and `tflint --recursive` (fix the errors and the warnings).

# Testing

## Writing terraform tests

- The `terraform/tests` folder should look like: https://github.com/canonical/platform-engineering-charm-template/tree/main/terraform/tests

  - There is a `setup` folder to configure the model. Follow the example from https://raw.githubusercontent.com/canonical/platform-engineering-charm-template/refs/heads/main/terraform/tests/setup/main.tf
  - There is `main.tftest.hcl` file. Follow the example of https://raw.githubusercontent.com/canonical/platform-engineering-charm-template/refs/heads/main/terraform/tests/main.tftest.hcl
  
    - Ensure that there is a renovate directive above each "revision" line.

  - After adapting the tests. There should not be a `terraform/tests/main.tf` file.

## Local testing

The terraform tests should be run in a virtual machine named "charmkeeper".

If the machine doesn't exist, create it with: `scripts/create-charmkeeper-vm.sh`.

If not already done, mount the working directory folder in the machine with

```bash
multipass mount --type native $PWD charmkeeper:/workdir
```

For each TERRAFORM_MODULE

```bash
multipass exec charmkeeper -d /workdir/$TERRAFORM_MODULE -- terraform init
multipass exec charmkeeper -d /workdir/$TERRAFORM_MODULE -- terraform test
```

## CI testing

This workflow is the reference to use to implement or update CI tests: https://raw.githubusercontent.com/canonical/platform-engineering-charm-template/refs/heads/main/.github/workflows/test_terraform_modules.yaml

- Adapt the k8s-controller and lxd-controller value depending on the charm type.
- Adapt the `terraform-directories` to reflect where the modules are in this charm.

# Maintain

## Configuring renovate

Configure renovate like https://raw.githubusercontent.com/canonical/platform-engineering-charm-template/refs/heads/main/renovate.json to

- Add a charmhub datasource and use it.
- Add a regex custom manager for revisions.
- Set ignorePath to an empty array to not exclude the tests/ folders of terraform.

