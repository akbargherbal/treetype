# PATTERN: Django Patterns (D-Level → C-Level)

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

# PATTERN: Django Patterns (D-Level → C-Level)

from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    age = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    website = models.URLField(blank=True)
    last_login = models.DateTimeField(auto_now=True)

# PATTERN: Django Patterns (D-Level → C-Level)

from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_date = models.DateField()

    def __str__(self):
        return self.title

# PATTERN: Django Patterns (D-Level → C-Level)

from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='articles')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# PATTERN: Django Patterns (D-Level → C-Level)

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

# PATTERN: Django Patterns (D-Level → C-Level)

from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['due_date', 'title']
        verbose_name = "Project Task"
        verbose_name_plural = "Project Tasks"

    def __str__(self):
        return self.title

# PATTERN: Django Patterns (D-Level → C-Level)

from .models import Product

# Get all available products under $50
available_cheap_products = Product.objects.filter(is_available=True, price__lt=50.00)

# Get all products that are not available or are too expensive
unavailable_or_expensive_products = Product.objects.exclude(is_available=True, price__lt=100.00)

# Get products with 'book' in their name, excluding those with 'ebook'
books = Product.objects.filter(name__icontains='book').exclude(name__icontains='ebook')

# PATTERN: Django Patterns (D-Level → C-Level)

from django.shortcuts import get_object_or_404
from .models import Author

# Safely retrieve a single author by primary key
try:
    author = Author.objects.get(pk=1)
    print(f"Found author: {author.name}")
except Author.DoesNotExist:
    print("Author not found.")

# Using get_object_or_404 in a view context
def author_detail_view(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author_detail.html', {'author': author})

# PATTERN: Django Patterns (D-Level → C-Level)

from .models import Book

# Get all books
all_books = Book.objects.all()

# Get all books ordered by title alphabetically
books_by_title = Book.objects.order_by('title')

# Get all books ordered by publication date (descending) then by title
recent_books = Book.objects.order_by('-publication_date', 'title')

# Get the first 5 books
first_five_books = Book.objects.all()[:5]

# PATTERN: Django Patterns (D-Level → C-Level)

from .models import Product

# Get a list of dictionaries for product names and prices
product_data = Product.objects.values('name', 'price')
for p in product_data:
    print(f"{p['name']}: ${p['price']}")

# Get a list of tuples for product names
product_names_tuples = Product.objects.values_list('name')
for name_tuple in product_names_tuples:
    print(name_tuple[0])

# Get a flat list of product names
product_names_flat = Product.objects.values_list('name', flat=True)
for name in product_names_flat:
    print(name)

# PATTERN: Django Patterns (D-Level → C-Level)

from django.db.models import Q
from .models import Product

# Products that are available AND (price < 50 OR name contains 'sale')
complex_products = Product.objects.filter(
    Q(is_available=True) & (Q(price__lt=50) | Q(name__icontains='sale'))
)

# Products that are NOT available OR (price > 100 AND description is not empty)
another_query = Product.objects.filter(
    Q(is_available=False) | (Q(price__gt=100) & ~Q(description=''))
)

# Products with 'book' in name OR 'novel' in description
books_or_novels = Product.objects.filter(Q(name__icontains='book') | Q(description__icontains='novel'))

# PATTERN: Django Patterns (D-Level → C-Level)

from django.db.models import F
from .models import Product

# Increase the price of all available products by 10%
Product.objects.filter(is_available=True).update(price=F('price') * 1.1)

# Set the description to be the same as the name for products with empty description
Product.objects.filter(description='').update(description=F('name'))

# Find products where price is greater than twice the cost (assuming a 'cost' field exists)
# Product.objects.filter(price__gt=F('cost') * 2)

# PATTERN: Django Patterns (D-Level → C-Level)

from django.db.models import Avg, Count, Sum
from .models import Book, Author

# Aggregate: Calculate total number of books and average publication year
stats = Book.objects.aggregate(total_books=Count('id'), avg_year=Avg('publication_date__year'))
print(f"Total books: {stats['total_books']}, Average publication year: {stats['avg_year']}")

# Annotate: Get each author's name and their total number of books
authors_with_book_count = Author.objects.annotate(num_books=Count('books'))
for author in authors_with_book_count:
    print(f"{author.name}: {author.num_books} books")

# PATTERN: Django Patterns (D-Level → C-Level)

from .models import Book

# Fetch books and their related author in a single query
# Avoids N+1 query problem for ForeignKey relationships
books_with_authors = Book.objects.select_related('author').all()

for book in books_with_authors:
    # Accessing book.author won't trigger another database query
    print(f"Book: {book.title}, Author: {book.author.name}")

# Filter and select_related
specific_books = Book.objects.select_related('author').filter(publication_date__year=2023)

# PATTERN: Django Patterns (D-Level → C-Level)

from .models import Article, Tag

# Fetch articles and their related tags efficiently
# Uses a separate query for tags and joins them in Python
articles_with_tags = Article.objects.prefetch_related('tags').all()

for article in articles_with_tags:
    tag_names = ", ".join([tag.name for tag in article.tags.all()])
    print(f"Article: {article.title}, Tags: {tag_names}")

# Prefetch related for reverse ForeignKey (e.g., Author and their books)
from .models import Author
authors_with_books = Author.objects.prefetch_related('books').all()
for author in authors_with_books:
    book_titles = ", ".join([book.title for book in author.books.all()])
    print(f"Author: {author.name}, Books: {book_titles}")

# PATTERN: Django Patterns (D-Level → C-Level)

from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.filter(is_available=True).order_by('name')
    context = {
        'products': products,
        'title': 'Available Products'
    }
    return render(request, 'shop/product_list.html', context)

# In shop/urls.py:
# path('products/', product_list, name='product_list'),

# PATTERN: Django Patterns (D-Level → C-Level)

from django.views.generic import ListView
from .models import Book

class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html' # <app>/<model>_list.html
    context_object_name = 'books' # default is object_list
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.filter(publication_date__year__gte=2000).order_by('-publication_date')

# In library/urls.py:
# path('books/', BookListView.as_view(), name='book_list'),

# PATTERN: Django Patterns (D-Level → C-Level)

from django.views.generic import DetailView
from .models import Author

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'library/author_detail.html' # <app>/<model>_detail.html
    context_object_name = 'author' # default is object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books_by_author'] = self.object.books.all()
        return context

# In library/urls.py:
# path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),

# PATTERN: Django Patterns (D-Level → C-Level)

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm # Assuming a BookForm exists

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm # Or fields = ['title', 'author', 'publication_date']
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('book_list') # Redirect after successful creation

    def form_valid(self, form):
        # Optional: Perform actions before saving
        form.instance.created_by = self.request.user # If user is logged in
        return super().form_valid(form)

# In library/urls.py:
# path('books/new/', BookCreateView.as_view(), name='book_create'),

# PATTERN: Django Patterns (D-Level → C-Level)

from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm # Assuming a ProductForm exists

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm # Or fields = ['name', 'price', 'is_available']
    template_name = 'shop/product_form.html'
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        # Optional: Perform actions before saving
        # form.instance.last_updated_by = self.request.user
        return super().form_valid(form)

# In shop/urls.py:
# path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),

# PATTERN: Django Patterns (D-Level → C-Level)

# In myproject/urls.py or myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_form, name='contact'),
]

# PATTERN: Django Patterns (D-Level → C-Level)

# In myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Integer parameter for product ID
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    # Slug parameter for article slug
    path('articles/<slug:article_slug>/', views.article_detail, name='article_detail'),
    # UUID parameter for unique identifier
    path('users/<uuid:user_uuid>/', views.user_profile, name='user_profile'),
]

# PATTERN: Django Patterns (D-Level → C-Level)

# In myproject/urls.py (project-level urls.py)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')), # Include URLs from the 'shop' app
    path('blog/', include('blog.urls', namespace='blog')), # Include with a namespace
    path('', include('core.urls')), # Include root URLs from 'core' app
]

# PATTERN: Django Patterns (D-Level → C-Level)

from django.urls import reverse
from django.http import HttpResponseRedirect

# Get URL for a view without arguments
home_url = reverse('home')
print(f"Home URL: {home_url}")

# Get URL for a view with arguments
product_detail_url = reverse('product_detail', args=[123])
print(f"Product 123 URL: {product_detail_url}")

# Get URL for a namespaced view
article_url = reverse('blog:article_detail', kwargs={'article_slug': 'my-first-post'})
print(f"Article URL: {article_url}")

# Use in a view for redirection
def create_product_view(request):
    # ... process form ...
    return HttpResponseRedirect(reverse('product_list'))

# PATTERN: Django Patterns (D-Level → C-Level)

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email")
    message = forms.CharField(widget=forms.Textarea, label="Your Message")
    newsletter = forms.BooleanField(required=False, label="Subscribe to newsletter")

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@example.com'):
            raise forms.ValidationError("Please use an @example.com email address.")
        return email

# PATTERN: Django Patterns (D-Level → C-Level)

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date']
        # Or exclude = ['created_at', 'updated_at']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

# PATTERN: Django Patterns (D-Level → C-Level)

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'is_available']

    def clean_name(self):
        name = self.cleaned_data['name']
        if 'badword' in name.lower():
            raise forms.ValidationError("Product name contains inappropriate language.")
        return name

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be a positive number.")
        return price

# PATTERN: Django Patterns (D-Level → C-Level)

from django.shortcuts import render, redirect
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # send_email(name, email, message)
            return redirect('contact_success') # Redirect to a success page
    else:
        form = ContactForm() # An unbound form for GET request
    return render(request, 'myapp/contact.html', {'form': form})

# PATTERN: Django Patterns (D-Level → C-Level)

from django.shortcuts import render
from .models import Article

def article_detail(request, article_slug):
    article = Article.objects.get(slug=article_slug)
    related_articles = Article.objects.filter(tags__in=article.tags.all()).exclude(pk=article.pk)[:3]

    context = {
        'article': article,
        'related_articles': related_articles,
        'user_is_premium': request.user.is_authenticated and request.user.profile.is_premium,
        'page_title': article.title,
    }
    return render(request, 'blog/article_detail.html', context)

# PATTERN: Django Patterns (D-Level → C-Level)

from django.db import models

class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)

    def expensive(self):
        return self.get_queryset().filter(price__gt=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    objects = models.Manager() # Default manager
    active_products = ActiveProductManager() # Custom manager

# Usage:
# active_items = Product.active_products.all()
# expensive_active_items = Product.active_products.expensive()

# PATTERN: Django Patterns (D-Level → C-Level)

from django.db import models
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug: # Generate slug only if it's not set
            self.slug = slugify(self.title)
        super().save(*args, **kwargs) # Call the "real" save() method

    def __str__(self):
        return self.title

# PATTERN: Django Patterns (D-Level → C-Level)

# In myapp/middleware.py
from django.http import HttpResponse

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before the view is called.
        print(f"Request path: {request.path}")

        response = self.get_response(request)

        # Code to be executed for each request after the view is called.
        print(f"Response status: {response.status_code}")
        return response

# In settings.py:
# MIDDLEWARE = [
#     ...,
#     'myapp.middleware.SimpleMiddleware',
#     ...,
# ]