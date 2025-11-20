// PATTERN: React Hook Form (Form Handling)

import React from 'react';
import { useForm } from 'react-hook-form';

function MyBasicForm() {
  const { register, handleSubmit } = useForm();

  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("firstName")} placeholder="First Name" />
      <button type="submit">Submit</button>
    </form>
  );
}

// PATTERN: React Hook Form (Form Handling)

import React from 'react';
import { useForm } from 'react-hook-form';

function MyValidatedForm() {
  const { register, handleSubmit } = useForm();

  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register("email", { required: true, pattern: /^\S+@\S+$/i })}
        placeholder="Email"
      />
      <button type="submit">Submit</button>
    </form>
  );
}

// PATTERN: React Hook Form (Form Handling)

import React from 'react';
import { useForm } from 'react-hook-form';

function MyFormWithErrors() {
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register("username", { required: "Username is required" })}
        placeholder="Username"
      />
      {errors.username && <p>{errors.username.message}</p>}
      <button type="submit">Submit</button>
    </form>
  );
}

// PATTERN: React Hook Form (Form Handling)

import React from 'react';
import { useForm } from 'react-hook-form';

function MySubmissionForm() {
  const { register, handleSubmit } = useForm();

  const onSubmit = (data) => {
    console.log("Form submitted:", data);
    // e.g., send data to an API
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("productName")} placeholder="Product Name" />
      <button type="submit">Save Product</button>
    </form>
  );
}

// PATTERN: React Hook Form (Form Handling)

import React from 'react';
import { useForm } from 'react-hook-form';

function MyWatchForm() {
  const { register, watch } = useForm();
  const watchedValue = watch("searchQuery", ""); // Watch 'searchQuery'

  return (
    <div>
      <input {...register("searchQuery")} placeholder="Search..." />
      <p>You are typing: {watchedValue}</p>
    </div>
  );
}

// PATTERN: React Hook Form (Form Handling)

import React from 'react';
import { useForm } from 'react-hook-form';

function MyResetForm() {
  const { register, handleSubmit, reset } = useForm();

  const onSubmit = (data) => {
    console.log("Submitted:", data);
    reset(); // Resets all form fields to their default/empty state
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("taskName")} placeholder="Task Name" />
      <button type="submit">Add Task</button>
    </form>
  );
}

// PATTERN: React Hook Form (Form Handling)

import React from 'react';
import { useForm } from 'react-hook-form';

function MyDefaultValuesForm() {
  const { register, handleSubmit } = useForm({
    defaultValues: {
      itemName: "Default Item",
      quantity: 1
    }
  });

  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("itemName")} />
      <input type="number" {...register("quantity")} />
      <button type="submit">Save</button>
    </form>
  );
}