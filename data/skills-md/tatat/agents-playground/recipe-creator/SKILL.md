---
name: recipe-creator
description: Create custom recipes based on available ingredients, dietary restrictions, and preferences
---

# Recipe Creator

Generate personalized recipes based on what you have and what you need.

## Capabilities

- Create recipes from available ingredients
- Adapt recipes for dietary restrictions (vegan, gluten-free, keto)
- Scale recipes for different serving sizes
- Suggest ingredient substitutions
- Provide nutritional estimates

## Input Format

- Available ingredients (list)
- Dietary restrictions (optional)
- Cuisine preference (optional)
- Serving size (optional)
- Cooking time limit (optional)

## Output Format

```
Recipe: [Name]
Servings: [N]
Time: [Prep + Cook time]

Ingredients:
- [ingredient] - [amount]

Instructions:
1. [step]
2. [step]

Nutrition (per serving):
- Calories: [N]
- Protein: [N]g
```

## Tips

- Always check for allergens
- Suggest prep-ahead steps when possible
- Include storage instructions
