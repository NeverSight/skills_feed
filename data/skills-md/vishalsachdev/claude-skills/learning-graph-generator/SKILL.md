---
name: learning-graph-generator
description: Generates a comprehensive learning graph from a course description, including 200 concepts with dependencies, taxonomy categorization, and quality validation reports. Use this when the user wants to create a structured knowledge graph for educational content.
---

# Learning Graph Generator

**Version:** 0.02

You are tasked with generating a comprehensive high-quality learning graph from a course description.
A learning graph is the foundational data structure for intelligent textbooks that can recommend learning paths.
A learning graph is like a roadmap of Concepts to help students achieve their learning goals.
A learning graph is an DAG Concept graph.  Each arrow is a "Learning Dependency" relationship that suggest learning order.
The markdown you generate must be compatible with the mkdocs version of markdown.  Make sure you put a blank line before any lists.

Follow these steps carefully:

## Markdown Generation Rules

1. Always place a blank line before any markdown list.  This is required by the mkdocs markdown tools.

## Mkdocs Navigation Rules

After you add a markdown file (any file with an extension `.md`) make sure to add that file
to the navigation structure in the mkdocs.yml file.  Here is an example of the nav section
for the learning graph section:

```yml
  - Learning Graph:
    - Introduction: learning-graph/index.md
    - Course Description Assessment: learning-graph/course-description-assessment.md
    - Concept Enumeration: learning-graph/list-concepts.md
    - Graph Quality Analysis: learning-graph/graph-quality-analysis.md
    - Concept Taxonomy: learning-graph/concept-taxonomy.md
    - Taxonomy Distribution Report: learning-graph/taxonomy-distribution-report.md
```

## Step 0: Setup

Tell the user that they are running the version graph generator and the version number above.

The default context is that the skill is run from claude code in the home directory of an intelligent textbook that has been checked out from GitHub.
There should be a docs directory with a standard mkdocs.yml file in the home git directory.
You will create a directory called /docs/learning-graph it it does not already exist.  
The path is relative to the git home directory.  The assumption is that /docs is relative to the directory that claude was started in.

`mkdir -p docs/learning-graph; cd docs/learning-graph`

You will copy python programs from this skill package into the `/docs/learning-graph` directory.  
You will execute python from that directory.

If you do not see the `docs` directory and the `mkdocs.yml` file suggest that the user clone a sample textbook from the following location:

`git clone https://github.com/dmccreary/intelligent-book-template`
`cd intelligent-book-template`

## Step 1: Course Description Quality Assessment

Before you begin this step, verify that it has not already been done.
To do this, check the yml metadata in the `docs/course-description.md` file.

Here is a sample of the yml metadata:

```markdown
---
title: Course Description
description: A detailed course description 
quality_score: 95
---
# Course Description
```

If you see a quality_score above 85 you may tell the user you found a score above 85 and skip this entire step.  Tell them this is a way to save tokens.

If the quality score is below 85, analyze the provided course description at [course-description.md](../course-description.md) to ensure it has enough content to generate 200 high-quality concepts:

1. Verify the course has a title, prerequisites, intended audience, objectives, and outcomes ("After this course students will be able to").  If these fields are missing ask the user for this information. 
1. Examine the depth and breadth of topics covered
2. Assess whether the material has sufficient granularity for 200 distinct concepts
3. Check for diverse topic areas and learning objectives
4. Provide detailed feedback to the user about:
   - List the expected content that you found
   - Estimated number of concepts you can derive
   - Compare this concept number with similar courses
   - Describe areas where the course description is strong
   - Any gaps or areas that might be under-represented
   - Suggest how the 2001 Bloom taxonomy (remember, understand, apply, analyze, evaluate, create) could improve the outcomes descriptions
   - Objective overall quality assessment on a scale of (1-poor to 100-perfect)
   - Suggest that the user does not proceed unless a quality score is 70 or above

Use the following rubric for creating a quality score:

### 2.2 Course Description Quality Scoring System

Evaluate the course description using this 100-point scoring system:

| Element | Points | Criteria |
|---------|--------|----------|
| **Title** | 5 | Clear, descriptive course title present |
| **Target Audience** | 5 | Specific audience identified (e.g., "college undergraduate") |
| **Prerequisites** | 5 | Prerequisites listed or explicitly stated as "None" |
| **Main Topics Covered** | 10 | Comprehensive list of topics (ideally 5-10 topics) |
| **Topics Excluded** | 5 | Clear boundaries set for what's NOT covered |
| **Learning Outcomes Header** | 5 | Clear statement: "After this course, students will be able to..." |
| **Remember Level** | 10 | Multiple specific outcomes for remembering/recalling |
| **Understand Level** | 10 | Multiple specific outcomes for understanding/explaining |
| **Apply Level** | 10 | Multiple specific outcomes for applying/using |
| **Analyze Level** | 10 | Multiple specific outcomes for analyzing/breaking down |
| **Evaluate Level** | 10 | Multiple specific outcomes for evaluating/judging |
| **Create Level** | 10 | Multiple specific outcomes for creating/synthesizing; includes capstone ideas |
| **Descriptive Context** | 5 | Additional context about course importance, relevance, or value |

**Scoring Guidelines:**
- Award full points if element is complete and high-quality
- Award partial points if element is present but incomplete or vague
- Award 0 points if element is missing
- For Bloom's Taxonomy levels, require at least 3 specific, actionable outcomes for full points

Tell user what their score was and suggest they improve the course description until the score goes above 80.

Save this report to [course-description-assessment.md](./course-description-assessment.md)

5. **Ask the user if you should proceed** with generating the learning graph

## Step 2: Generate Concept Labels

Once the course-description has been approved, generate 200 concept labels from the course content:

**Requirements:**
- Each Concept label must be in Title Case
- Maximum length: 32 characters
- Labels should be clear, specific, and pedagogically sound
- Cover the full breadth of the course material
- Concept Labels are entity names, not questions
- Do not use questions in the Concept Label.  Don't use "What is Git", just use "Git"

!!! note
  Because these concept labels are used within a network graph, they must not be too long.
  Otherwise the graph will be hard to read.

**Output:**
- Save the numbered list to [concept-list.md](./concept-list.md)
- Format: Simple numbered list (1-200) in a markdown file
- Make sure that each number is unique so it can be used as a ConceptID
- Inform the user the file has been created
- Tell the user they should view the list and add and remove concepts now
- Tell the user it is best review the concept list before the next steps

Now ask the user to take some time to manually review the entire list of concept labels.
If there are concepts that are not appropriate they should be removed now.
If there are additional concepts that need to be added, they should be added now.
It will require a lot of extra tokens later to change the content later.
This is an important review step to ensure the quality of the textbook.
Pay special attention to the length of the concept labels and the quality of any abbreviations.

## Step 3: Generate Dependency Graph

Create a CSV file mapping dependencies between concepts:

**Format:**
- Filename: [learning-graph.csv](./learning-graph.csv)
- Columns: `ConceptID,ConceptLabel,Dependencies`
- ConceptID: Integer (1-200)
- ConceptLabel: The exact label from Step 2
- Dependencies: Pipe-delimited list of ConceptIDs (e.g., "1|3|7")

**Dependency Rules:**
- Foundational/prerequisite concepts have NO dependencies (empty Dependencies field)
- All other concepts must have at least one dependency
- No concept can depend on itself
- The graph must be a Directed Acyclic Graph (DAG) - no cycles
- Create meaningful learning pathways, not just linear chains
- Consider prerequisite relationships carefully

**Note:** The JSON file will be created in later steps (Steps 7-8) after the taxonomy is added to the CSV file. The complete JSON will include metadata, groups, nodes, and edges sections conforming to the learning-graph-schema.json.

## Step 4: Learning Graph Quality Validation

Perform comprehensive quality checks on the dependency graph
by using the Python program analyze-graph.py in this skill.
It will do the following checks:

1. **Verify DAG structure**: Ensure no cycles exist
2. **Check for self-dependencies**: No concept should depend on itself
3. **Foundational concepts**: Identify concepts with zero dependencies
4. **Orphaned nodes**: Identify concepts that nothing depends on (potential dead ends)
5. **Disconnected subgraphs**: Check if all concepts are connected to the main graph
6. **Linear chains**: Flag if too many concepts only depend on the immediately prior concept
7. **Indegree analysis**: Calculate indegree (number of concepts that depend on each concept)

Shell command `python analyze-graph.py learning-graph.csv quality-metrics.md`

Verify the report has been written to [quality-metrics.md](./quality-metrics.md)

**Generate the learning graph quality metrics report:**
- Total concepts with zero dependencies - outbound arrows (foundational prerequisites)
- Total concepts with 1+ dependencies
- Average number of dependencies per concept
- Maximum dependency chain length
- Number of orphaned nodes
- Number of disconnected subgraphs
- Top 10 concepts with highest indegree (most depended-upon concepts)

Give the user a general quality score on a scale of 1 (poor) to 100 (perfect).
If the learning graph does not get a score above 70, suggest that the user iterates on the process

## Step 5: Create Concept Taxonomy

Develop a categorical taxonomy for organizing concepts:

**Requirements:**
- Target: ~12 categories (can vary by 2-3 if natural groupings emerge)
- Categories should evenly distribute concepts
- Avoid having any single category exceed 30% of total concepts
- Use clear, descriptive category names with title case and spaces
- Create 3-5 letter abbreviations for each category (TaxonomyID)
- Note that a JSON representation of the taxonomy will be created to form the groups section of the learning graph

**Output:**
- Save taxonomy to [concept-taxonomy.md](./concept-taxonomy.md)
- Format as markdown with:
  - Category name
  - TaxonomyID abbreviation (3-5 letters uppercase)
  - Brief description of what concepts belong in this category

## Step 6: Add Taxonomy to CSV

Update the dependencies CSV file:

1. Add a new column: `TaxonomyID` to the existing CSV file if it does not exist
2. For each concept, assign the best matching TaxonomyID
3. Use "MISC" for concepts without a clear category match
4. Save the updated file to [learning-graph.csv](./learning-graph.csv)

You can use the Python Program add-taxonomy.py as a template
that will do the substitution.

**Final CSV columns:** `ConceptID,ConceptLabel,Dependencies,TaxonomyID`

## Step 7: Create the `metadata` section of the learning-graph.json file

The metadata section contains Dublin Core-inspired fields for the textbook extracted from the course-description.md file. The JSON schema for the learning graph is located in the file learning-graph-schema.json within this skill.

**Required fields:**
- `title`: Extract from the course description title
- `description`: Extract or summarize from the course description

**Optional but recommended fields:**
- `creator`: Author or organization name
- `date`: Current date in YYYY-MM-DD format
- `version`: Version number (e.g., "1.0")
- `format`: "Learning Graph JSON v1.0"
- `schema`: URL to the JSON schema
- `license`: License information (e.g., "CC BY-NC-SA 4.0 DEED")

Here is an example of the metadata section:

```json
"metadata": {
    "title": "Title Text From Course Description",
    "description": "A description of the course in a few sentences.",
    "creator": "Your Name",
    "date": "2025-11-01",
    "version": "1.0",
    "format": "Learning Graph JSON v1.0",
    "schema": "https://raw.githubusercontent.com/dmccreary/learning-graphs/refs/heads/main/src/schema/learning-graph-schema.json",
    "license": "CC BY-NC-SA 4.0 DEED"
  }
```

You can create a metadata.json file with these fields to pass to the csv-to-json.py program in Step 9.

## Step 8: Create the groups section of the JSON file

Convert the taxonomy categories into JSON format for the groups section of the learning-graph.json file. The JSON schema for the learning graph is located in the file learning-graph-schema.json within this skill.

The groups section creates a legend of concept types with distinct colors for visualization.

**Important:**
- The groups section uses taxonomy IDs (e.g., "FOUND", "DEF") as keys
- Each group must have a `classifierName` field containing the human-readable name (e.g., "Foundation Concepts")
- Each group must have a `color` field (CSS color value)
- Each group should have a `font` object with a `color` field for text readability

**Key structure:**
- **Group key**: Use the TaxonomyID from the CSV (uppercase, no spaces, e.g., "FOUND")
- **classifierName**: Display name with Title Case and spaces (e.g., "Foundation Concepts")
- **color**: Choose distinct colors for each taxonomy
- **font.color**: "white" for dark backgrounds, "black" for light backgrounds

Below is an example of the groups section:

```json
"groups": {
    "FOUND": {
      "classifierName": "Foundation Concepts",
      "color": "red",
      "font": {
        "color": "white"
      }
    },
    "DEF": {
      "classifierName": "Definitions",
      "color": "orange",
      "font": {
        "color": "black"
      }
    },
    "CORE": {
      "classifierName": "Core Concepts",
      "color": "gold",
      "font": {
        "color": "black"
      }
    },
    "INTER": {
      "classifierName": "Intermediate",
      "color": "green",
      "font": {
        "color": "white"
      }
    },
    "ADV": {
      "classifierName": "Advanced",
      "color": "blue",
      "font": {
        "color": "white"
      }
    },
    "MISC": {
      "classifierName": "Miscellaneous Concepts",
      "color": "indigo",
      "font": {
        "color": "white"
      }
    },
    "PROJ": {
      "classifierName": "Project Ideas",
      "color": "violet",
      "font": {
        "color": "white"
      }
    },
    "CAP": {
      "classifierName": "Capstone Projects",
      "color": "gray",
      "font": {
        "color": "white"
      }
    }
  }
```

**Note:** The csv-to-json.py program will automatically generate the groups section based on the taxonomies found in your CSV file. You can customize colors by creating an optional color-config.json file.

## Step 9: Generate the Complete Learning Graph JSON

Now that you have created the metadata.json file (Step 7) and have the taxonomy-enriched CSV (Step 6), run the csv-to-json.py program to generate the complete learning-graph.json file:

```bash
python csv-to-json.py learning-graph.csv learning-graph.json metadata.json
```

This command will:
1. Read the learning-graph.csv file (with ConceptID, ConceptLabel, Dependencies, TaxonomyID columns)
2. Use the metadata from metadata.json
3. Auto-generate the groups section based on the taxonomies in the CSV
4. Create nodes with proper group references (using TaxonomyIDs)
5. Create edges based on the dependencies
6. Output a complete learning-graph.json file conforming to the schema

Verify that the file [learning-graph.json](./learning-graph.json) is present and valid.

Optional: You can validate the JSON against the schema using:
```bash
./validate-learning-graph.sh learning-graph.json
```

## Step 10: Taxonomy Distribution Report

Generate a distribution analysis:

1. Count concepts in each category
2. Calculate percentages
3. Identify over-represented categories (>30%)
4. Suggest alternative categorization if needed

Use the python report in this skill called taxonomy-distribution.py

**Output:**
- Save to [taxonomy-distribution.md](./taxonomy-distribution.md)
- Format as markdown table with columns:
  - Category Name
  - TaxonomyID
  - Count
  - Percentage

## Step 11: Create new index.md from index-template.md

Create a new `index.md` file in the learning-graph directory from the file index-template.md in this skill.
Customize the new index.md file to reflect the name of this intelligent book.  Look for values in all uppercase (TEXTBOOK_NAME)
and replace them with the appropriate values.

## Step 12: Write session log

Export the session log to logs/learning-graph-generator-VERSION-DATE.md

Where:

1. VERSION is the version of this skill.
2. DATE is today's date in ISO format yyyy-mm-dd.

Note that the session log should also list what version of any Python program was used.
For example, not what version of the csv-to-json.py Python program was used in the session log.
This is important for debugging.

## Step 13: Completion

Inform the user that the learning graph generation is complete! Congratulate them and wish them success on their textbook or course material.  Tell them that the next step is the book-chapter-generator skill, but that it is critical to review
the concept lists, the concept taxonomies and the learning graph before they do this next step.

**Files created:**
- [course-description-assessment.md](./course-description-assessment.md) - quality assessment of the course description
- [concept-list.md](./concept-list.md) - Numbered list of 200 concepts
- [learning-graph.csv](./learning-graph.csv) - Full dependency graph with taxonomy
- [metadata.json](./metadata.json) - Metadata for the learning graph (title, description, creator, etc.)
- [learning-graph.json](./learning-graph.json) - Complete learning graph with metadata, groups, nodes, and edges in vis-network.js JSON format
- [concept-taxonomy.md](./concept-taxonomy.md) - Category definitions
- [quality-metrics.md](./quality-metrics.md) - Quality validation report
- [taxonomy-distribution.md](./taxonomy-distribution.md) - Category distribution analysis
- [index.md](./index.md) - Introduction page for the learning graph section


## Important Notes

- Maintain pedagogical integrity throughout the process
- Dependencies should reflect actual prerequisite knowledge
- Balance between granularity and comprehensiveness
- Ensure concepts build upon each other logically
- The learning graph should support multiple learning pathways, not just one linear path
