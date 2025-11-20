// PATTERN: React Hook Form (Form Handling)

import { useForm } from 'react-hook-form';

function BasicForm() {
  const { register, handleSubmit } = useForm();
  const onSubmit = data => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("firstName")} placeholder="First Name" />
      <input {...register("lastName")} placeholder="Last Name" />
      <button type="submit">Submit</button>
    </form>
  );
}

// PATTERN: React Hook Form (Form Handling)

import { useForm } from 'react-hook-form';

function ValidatedForm() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const onSubmit = data => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register("email", { required: "Email is required", pattern: /^\S+@\S+$/i })}
        placeholder="Email"
      />
      {errors.email && <p>{errors.email.message}</p>}
      <button type="submit">Submit</button>
    </form>
  );
}

// PATTERN: React Hook Form (Form Handling)

import { useForm } from 'react-hook-form';

function ErrorDisplayForm() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const onSubmit = data => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register("username", { required: "Username is required", minLength: { value: 3, message: "Min length 3" } })}
        placeholder="Username"
      />
      {errors.username && <p style={{ color: 'red' }}>{errors.username.message}</p>}
      <button type="submit">Register</button>
    </form>
  );
}

// PATTERN: React Hook Form (Form Handling)

import { useForm } from 'react-hook-form';

function SubmissionForm() {
  const { register, handleSubmit } = useForm();
  const onSubmit = data => {
    alert(JSON.stringify(data, null, 2));
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("taskName")} placeholder="Task Name" />
      <button type="submit">Add Task</button>
    </form>
  );
}

// PATTERN: React Hook Form (Form Handling)

import { useForm } from 'react-hook-form';

function WatchForm() {
  const { register, watch } = useForm();
  const searchQuery = watch("searchQuery");

  return (
    <div>
      <input {...register("searchQuery")} placeholder="Type to watch..." />
      <p>Current search: {searchQuery}</p>
    </div>
  );
}

// PATTERN: React Hook Form (Form Handling)

import { useForm } from 'react-hook-form';

function ResetForm() {
  const { register, handleSubmit, reset } = useForm();
  const onSubmit = data => {
    alert(JSON.stringify(data));
    reset(); // Resets the form after submission
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("itemName")} placeholder="Item Name" />
      <button type="submit">Add Item</button>
      <button type="button" onClick={() => reset()}>Clear Form</button>
    </form>
  );
}

// PATTERN: React Hook Form (Form Handling)

import { useForm } from 'react-hook-form';

function DefaultValuesForm() {
  const { register, handleSubmit } = useForm({
    defaultValues: {
      productName: "Sample Product",
      price: 99.99
    }
  });
  const onSubmit = data => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("productName")} />
      <input type="number" {...register("price", { valueAsNumber: true })} />
      <button type="submit">Update Product</button>
    </form>
  );
}