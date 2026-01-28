---
name: rails-controller-patterns
description: Rails controller patterns and conventions. Automatically invoked when working with controllers, routes, strong parameters, before_actions, or request handling. Triggers on "controller", "action", "routes", "routing", "strong params", "params.expect", "before_action", "respond_to", "RESTful", "CRUD", "redirect", "render".
allowed-tools: Read, Grep, Glob
---

# Rails Controller Patterns

Patterns for building well-structured Rails controllers.

## When This Skill Applies

- Implementing RESTful controller actions
- Handling request parameters safely
- Setting up before_action filters
- Managing response formats
- Designing routes
- Error handling in controllers

## Core Principles

### Thin Controllers
Controllers should:
- Handle HTTP concerns (params, session, response)
- Delegate business logic to models/services
- Keep actions under 10 lines

### RESTful Design
Stick to standard CRUD actions:
- `index`, `show`, `new`, `create`, `edit`, `update`, `destroy`
- Add custom actions sparingly

## Detailed Documentation

- [patterns.md](patterns.md) - Controller patterns and examples

## Controller Structure

```ruby
class PostsController < ApplicationController
  # 1. Before actions
  before_action :authenticate_user!
  before_action :set_post, only: [:show, :edit, :update, :destroy]

  # 2. Actions (CRUD order)
  def index
    @posts = Post.recent.page(params[:page])
  end

  def show
  end

  def new
    @post = current_user.posts.build
  end

  def create
    @post = current_user.posts.build(post_params)

    if @post.save
      redirect_to @post, notice: 'Post created.'
    else
      render :new, status: :unprocessable_entity
    end
  end

  def edit
  end

  def update
    if @post.update(post_params)
      redirect_to @post, notice: 'Post updated.'
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def destroy
    @post.destroy
    redirect_to posts_path, notice: 'Post deleted.'
  end

  private

  # 3. Private methods
  def set_post
    @post = current_user.posts.find(params[:id])
  end

  def post_params
    params.expect(post: [:title, :content, :published])
  end
end
```

## Strong Parameters (Rails 8+)

```ruby
# Rails 8+ syntax with expect
def post_params
  params.expect(post: [:title, :content, tags: []])
end

# Nested attributes
def user_params
  params.expect(user: [:name, :email, profile_attributes: [:bio, :avatar]])
end

# Traditional permit (still works)
def post_params
  params.require(:post).permit(:title, :content, tags: [])
end
```

## Quick Reference

| Action | HTTP Verb | Path | Purpose |
|--------|-----------|------|---------|
| index | GET | /posts | List all |
| show | GET | /posts/:id | Show one |
| new | GET | /posts/new | Form for new |
| create | POST | /posts | Create |
| edit | GET | /posts/:id/edit | Form for edit |
| update | PATCH/PUT | /posts/:id | Update |
| destroy | DELETE | /posts/:id | Delete |

## Key Conventions

- Use `redirect_to` after successful changes
- Use `render :action, status: :unprocessable_entity` for validation failures
- Return appropriate HTTP status codes
- Keep private methods minimal
