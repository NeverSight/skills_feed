---
name: pulumi-terraform-to-pulumi
description: Migrate Terraform projects to Pulumi. Use when users need to move infrastructure from Terraform to Pulumi, translate HCL configurations, or convert Terraform modules to Pulumi components.
---

# Migrating from Terraform to Pulumi

First establish scope and plan the migration by working out with the user:

- where the Terraform sources are (`${terraform_dir}`)
- where the migrated Pulumi project lives (`${pulumi_dir}`)
- what is the target Pulumi language (such as TypeScript, Python, YAML)
- whether migration aims to setup Pulumi stack states, or only translate source code

Confirm the plan with the user before proceeding.

Create a new Pulumi project in `${pulumi_dir}` in the chosen language. Edit sources to be empty and not declare any
resources. Ensure a Pulumi stack exists.

You must run `pulumi_up` tool before proceeding to ensure initial stack state is written.

Now produce a draft Pulumi state translation:

    pulumi plugin run terraform-migrate -- stack \
        --from ${terraform_dir} \
        --to ${pulumi_dir} \
        --out /tmp/pulumi-state.json \
        --plugins /tmp/required-providers.json

Do NOT install the plugin as it will auto-install as needed.

Sometimes terraform-migrate plugin fails because `tofu refresh` is not authorized. DO NOT skip this step. Work with the
user to find or build a Pulumi ESC environment to run the command in to make it succeed.

Read the generated `/tmp/required-providers.json` and install all these Pulumi providers into the new project,
respecting the suggested versions even if they downgrade an already installed provider. The file will contain records
such as `[{"name":"aws","version":"7.12.0"}]`.

Install providers as project dependencies using the language-specific package manager (NOT `pulumi plugin install`,
which only downloads plugins without adding dependencies):

    # TypeScript/JavaScript
    npm install @pulumi/aws@7.12.0

    # Python
    pip install pulumi_aws==7.12.0

    # Go
    go get github.com/pulumi/pulumi-aws/sdk/v7@v7.12.0

    # C#
    dotnet add package Pulumi.Aws --version 7.12.0

Import the translated state draft (`/tmp/pulumi-state.json`) into the Pulumi stack:

    pulumi stack import --file /tmp/pulumi-state.json

Translate source code to match both the Terraform source and the translated state. Aim for exact match. You can consult
the state draft `/tmp/pulumi-state.json` for Pulumi resource types and names to use.

Iterate on fixing the source code until `pulumi_preview` tool confirms that there are no changes to make and the diff
is empty or almost empty. Provider diffs or diffs on tags may be OK.

Offer the user to link an ESC environment to the stack so that each Pulumi stack can seamlessly have access to the
provider credentials it needs.

When all looks good, create a Pull Request with the migrated source code.

IMPORTANT:

- when creating a Pulumi project, do NOT use /workspace, create one under the checked out project
- do NOT run `pulumi convert`, instead use the terraform-migrate plugin
- do NOT run `pulumi package add terraform-module`
