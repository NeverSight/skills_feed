---
name: angular-forms
description: Angular Reactive Forms for form building, validation, and state management. Use when creating forms, implementing validators, handling form submissions, building dynamic forms, or integrating forms with NgRx Signals in Angular applications. Covers FormControl, FormGroup, and FormArray.
license: Complete terms in LICENSE.txt
---

# Angular Forms Skill

## Rules

### Form Creation
- Use `ReactiveFormsModule` for reactive forms
- Use `FormControl` for individual form fields
- Use `FormGroup` to group multiple form controls
- Use `FormArray` for dynamic lists of form controls
- Use `FormBuilder` for simplified form creation

### Validation
- Use built-in validators: `Validators.required`, `Validators.email`, `Validators.min`, `Validators.max`, `Validators.pattern`
- Custom validators MUST return `ValidationErrors | null`
- Show validation errors ONLY after field is touched
- Disable submit button when form is invalid

### Form State Management
- Check form state: `valid`, `invalid`, `touched`, `dirty`, `pristine`
- Reset form using `form.reset()`
- Update form values using `form.patchValue()` or `form.setValue()`

### NgRx Signals Integration
- Store form instance in `signalStore` state
- Use `rxMethod` for async form submission
- Use `tapResponse` for handling submission success/error
- Reset form on successful submission

### Form Submission
- Use `(ngSubmit)` event for form submission
- Validate form before processing: `if (form.valid)`
- Handle errors with user feedback

---

## Context

### Summary
Angular Reactive Forms provide a model-driven approach to handling form inputs with built-in validation, state management, and integration with Angular's reactive programming patterns.

### When to Use This Skill

Activate this skill when you need to:
- Create reactive forms with FormControl and FormGroup
- Implement built-in and custom validators
- Handle form submissions and data binding
- Build dynamic forms with FormArray
- Implement cross-field validation
- Integrate forms with NgRx Signals stores
- Handle async validators
- Implement form state management (touched, dirty, valid)
- Create reusable form components

### Basic Reactive Form Example

```typescript
import { Component } from '@angular/core';
import { ReactiveFormsModule, FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-user-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="userForm" (ngSubmit)="onSubmit()">
      <input formControlName="name" placeholder="Name">
      @if (userForm.controls.name.touched && userForm.controls.name.errors) {
        <span>Name is required</span>
      }
      
      <input formControlName="email" type="email" placeholder="Email">
      @if (userForm.controls.email.touched && userForm.controls.email.errors?.['email']) {
        <span>Invalid email</span>
      }
      
      <button type="submit" [disabled]="userForm.invalid">Submit</button>
    </form>
  `
})
export class UserFormComponent {
  userForm = new FormGroup({
    name: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.required, Validators.email])
  });
  
  onSubmit() {
    if (this.userForm.valid) {
      console.log(this.userForm.value);
    }
  }
}
```

### Custom Validators Example

```typescript
// Custom validator function
function minAgeValidator(minAge: number): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    if (!control.value) return null;
    
    const birthDate = new Date(control.value);
    const age = new Date().getFullYear() - birthDate.getFullYear();
    
    return age >= minAge ? null : { minAge: { required: minAge, actual: age } };
  };
}

// Usage
age: new FormControl('', [Validators.required, minAgeValidator(18)])
```

### Integration with NgRx Signals Example

```typescript
export const UserFormStore = signalStore(
  { providedIn: 'root' },
  withState({
    form: new FormGroup({
      name: new FormControl(''),
      email: new FormControl('')
    }),
    submitting: false,
    error: null as string | null
  }),
  withMethods((store, userService = inject(UserService)) => ({
    submitForm: rxMethod<void>(
      pipe(
        tap(() => patchState(store, { submitting: true })),
        switchMap(() => userService.createUser(store.form().value)),
        tapResponse({
          next: () => {
            store.form().reset();
            patchState(store, { submitting: false });
          },
          error: (error: Error) => patchState(store, { 
            error: error.message, 
            submitting: false 
          })
        })
      )
    )
  }))
);
```

### References

- [Angular Forms Documentation](https://angular.dev/guide/forms)
- [Form Validation](https://angular.dev/guide/forms/form-validation)
