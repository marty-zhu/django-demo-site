from django.test import TestCase, Client
from django.urls import reverse

from catalog.models import *
from django.contrib.auth.models import Permission

class TestIndexView(TestCase):
    
    def test_empty_library(self):
        resp = self.client.get(reverse('catalog:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['num_visits'], 0)
        self.assertEqual(resp.context['num_books'], 0)
        self.assertEqual(resp.context['num_authors'], 0)
        self.assertEqual(resp.context['num_genres'], 0)
        self.assertEqual(resp.context['num_language'], 0)

    #TODO: add populated library test


class TestLoginRedirect(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        num_authors = 3
        for author_id in range(num_authors):
            Author.objects.create(
                first_name = 'Test',
                last_name = f'Author{author_id}'
            )

        test_user = User.objects.create_user(
            username='test_user',
            password='fortesting',
        )
        test_user.save()
        
    def test_page_redirects_when_not_logged_in(self):
        resp = self.client.get(reverse('catalog:authors'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(
            resp, '/accounts/login/?next=/catalog/authors/'
            )

    def test_login(self):
        self.client.login(
            username='test_user',
            password='fortesting',
        )
        resp = self.client.get(reverse('catalog:authors'))
        self.assertEqual(str(resp.context['user']), 'test_user')
        self.assertEqual(resp.status_code, 200)


class TestAuthorListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data for entire class. Runs once.

        WARNING: Don't use this if one of the test methods will change
        the data, use `setUp()` instead.
        """
        num_authors = 13
        
        for author_id in range(num_authors):
            Author.objects.create(
                first_name = 'Test',
                last_name = f"Author{author_id}"
            )

        test_user = User.objects.create_user(
            username = 'test_user',
            password = 'fortesting'
        )
        test_user.save()

    def setUp(self):
        """Set up test data for each test in the class.
        Runs once for every test method in the class.
        """
        self.client.login(
            username = 'test_user',
            password = 'fortesting',
        )
        
    def test_url_accessible_by_locator(self):
        resp = self.client.get('/catalog/authors/')
        self.assertEqual(resp.status_code, 200)

    def test_url_accessible_by_name(self):
        resp = self.client.get(reverse('catalog:authors'))
        self.assertEqual(resp.status_code, 200)

    def test_view_template_is_correct(self):
        resp = self.client.get('/catalog/authors/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalog/authors.html')

    def test_pagination_is_ten(self):
        resp = self.client.get('/catalog/authors/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertEqual(
            len(resp.context['list_of_all_authors']), 10
            )

    def test_view_lists_all_authors(self):
        resp = self.client.get(reverse('catalog:authors') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertEqual(
            len(resp.context['list_of_all_authors']), 3
        )


class TestBookListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(
            first_name='John',
            last_name='Doe',
        )
        author.save()
        genre = Genre.objects.create(
            name='Test Genre',
        )
        language = Language.objects.create(
            name='Test Language'
        )

        num_books = 15
        for num in range(num_books):
            book = Book.objects.create(
                isbn=num,
                title=f'Test Title {num}',
                summary=f'This is a test book for book {num}',
            )
            book.authors.add(author)
            book.genre.add(genre)
            book.language = language
            book.save()
        
        test_user = User.objects.create_user(
            username='test_user',
            password='fortesting'
        )
        test_user.save()

    def setUp(self):
        self.client.login(
            username='test_user',
            password='fortesting'
        )

    def test_page_accessible_by_locator(self):
        resp = self.client.get('/catalog/books/')
        self.assertEqual(resp.status_code, 200)

    def test_page_accessible_by_name(self):
        resp = self.client.get(reverse('catalog:books'))
        self.assertEqual(resp.status_code, 200)

    def test_page_template_is_correct(self):
        resp = self.client.get('/catalog/books/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('catalog/books.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('catalog:books'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertEqual(
            len(resp.context['list_of_all_books']),
            10
        )

    def test_all_books_are_displayed(self):
        resp = self.client.get(reverse('catalog:books') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertEqual(
            len(resp.context['list_of_all_books']),
            5
        )

class TestBookDetailView(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_page_accessible_by_locator(self):
        self.fail('Test note yet written.')

    def test_page_accessible_by_name(self):
        self.fail('Test note yet written.')

    def test_page_template_is_correct(self):
        self.fail('Test note yet written.')

    def test_page_display_correct_content(self):
        self.fail('Test note yet written.')


class TestLoanedBooksByUserListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username='test_user1',
            password='fortesting',
        )
        test_user1.save()
        test_user2 = User.objects.create_user(
            username='test_user2',
            password='fortesting',
        )
        test_user2.save()

        books = []
        for num in range(1, 4):
            book = Book.objects.create(
                title=f'TestBook{num}',
                isbn=num,
            )
            books.append(book)
        
        book_copies = []
        books_in_lib = dict(zip(books, [1,2,1]))
        for book, count in books_in_lib.items():
            for num in range(count):
                book_copy = BookInstance.objects.create(
                    book=book,
                )
                book_copies.append(book_copy)

        return_date = timezone.localtime() + timedelta(days=1)
        status = 'o'
        book1 = book_copies[0]
        book1.borrower = test_user1
        book1.due_back = return_date
        book1.status = status
        book1.save()
        book2 = book_copies[1]
        book2.borrower = test_user1
        book2.due_back = return_date
        book2.status = status
        book2.save()
        book3 = book_copies[2]
        book3.borrower = test_user2
        book3.due_back = return_date
        book3.status = status
        book3.save()

    def test_page_accessible_by_locator(self):
        self.client.login(
            username='test_user1',
            password='fortesting',
        )
        resp = self.client.get('/catalog/mybooks/')
        self.assertEqual(str(resp.context['user']), 'test_user1')
        self.assertEqual(resp.status_code, 200)

    def test_page_accessible_by_name(self):
        self.client.login(
            username='test_user2',
            password='fortesting',
        )
        resp = self.client.get(reverse('catalog:my-borrowed'))
        self.assertEqual(str(resp.context['user']), 'test_user2')
        self.assertEqual(resp.status_code, 200)

    def test_only_books_by_user1_is_displayed(self):
        self.client.login(
            username='test_user1',
            password='fortesting',
        )
        resp = self.client.get('/catalog/mybooks/')
        self.assertEqual(str(resp.context['user']), 'test_user1')
        self.assertTrue('bookinstance_list' in resp.context)
        self.assertEqual(
            len(resp.context['bookinstance_list']),
            2
        )

    def test_only_books_by_user2_is_displayed(self):
        self.client.login(
            username='test_user2',
            password='fortesting',
        )
        resp = self.client.get('/catalog/mybooks/')
        self.assertEqual(str(resp.context['user']), 'test_user2')
        self.assertTrue('bookinstance_list' in resp.context)
        self.assertEqual(
            len(resp.context['bookinstance_list']),
            1
        )

    def test_books_not_by_user_is_not_displayed(self):
        self.client.login(
            username='test_user2',
            password='fortesting',
        )
        resp = self.client.get('/catalog/mybooks/')
        self.assertEqual(str(resp.context['user']), 'test_user2')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            len(resp.context['bookinstance_list']),
            1
        )
        user_2_book = resp.context['bookinstance_list'][0]

        self.client.login(
            username='test_user1',
            password='fortesting',
        )
        resp = self.client.get('/catalog/mybooks/')
        self.assertEqual(str(resp.context['user']), 'test_user1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            len(resp.context['bookinstance_list']),
            2
        )
        user_1_books = resp.context['bookinstance_list']
        self.assertTrue(user_2_book not in user_1_books)  


class TestAllLoandedBooksLibrarianListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username='test_user1',
            password='fortesting',
        )
        test_user2 = User.objects.create_user(
            username='test_user2',
            password='fortesting',
        )
        test_user3 = User.objects.create_user(
            username='test_user3',
            password='fortesting',
        )
        test_user1.save()
        test_user2.save()
        test_user3.save()
        users = [test_user1, test_user2, test_user3]

        book_copies = []
        for num in range(1,22):
            book = Book.objects.create(
                title=f"Test Book {num}",
                isbn=num,
            )
            copy = BookInstance.objects.create(
                book=book,
                status='o',
                due_back=timezone.localtime() + timedelta(days=num),
                borrower=users[num%3]
            )
            book_copies.append(copy)
        
        librarian = User.objects.create_user(
            username='test_librarian',
            password='fortesting',
        )
        permission = Permission.objects.get(name='Set book as returned')
        librarian.user_permissions.add(permission)
        librarian.save()

    def setUp(self):
        self.client.login(
            username='test_librarian',
            password='fortesting',
        )

    def test_page_accessible_by_locator(self):
        resp = self.client.get('/catalog/librarian/booksloaned/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.context['user']), 'test_librarian')

    def test_page_accessible_by_name(self):
        resp = self.client.get(reverse('catalog:books-on-loan'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.context['user']), 'test_librarian')

    def test_page_template_is_correct(self):
        resp = self.client.get(reverse('catalog:books-on-loan'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.context['user']), 'test_librarian')
        self.assertTemplateUsed('catalog/bookinstance_on_loan_list.html')

    def test_page_is_paginated(self):
        resp = self.client.get('/catalog/librarian/booksloaned/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.context['user']), 'test_librarian')
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])

    def test_all_books_on_loan_is_listed(self):
        resp = self.client.get('/catalog/librarian/booksloaned/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.context['user']), 'test_librarian')
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertEqual(
            len(resp.context['bookinstance_list']),
            20
        )
        resp = self.client.get('/catalog/librarian/booksloaned/' \
                               + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            len(resp.context['bookinstance_list']),
            1
        )

    def test_books_not_on_loan_is_not_displayed(self):
        book = Book.objects.create(
            title='Book not on loan',
            isbn=999,
        )
        book_copy = BookInstance.objects.create(
            book=book,
            status='a',
        )
        book_copy.save()
        resp = self.client.get('/catalog/librarian/booksloaned/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.context['user']), 'test_librarian')
        self.assertTrue(book_copy not in resp.context['bookinstance_list'])
        resp = self.client.get('/catalog/librarian/booksloaned/' \
                               + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(book_copy not in resp.context['bookinstance_list'])

    def test_books_ordered_by_due_date(self):
        resp = self.client.get('/catalog/librarian/booksloaned/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.context['user']), 'test_librarian')
        bookinstance_list = resp.context['bookinstance_list']
        resp = self.client.get('/catalog/librarian/booksloaned/' \
                               + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.context['user']), 'test_librarian')
        bookinstance_list = bookinstance_list | resp.context['bookinstance_list']
        last_date = 0
        for bookinstance in bookinstance_list:
            if last_date == 0:
                last_date = bookinstance.due_back
            else:
                self.assertTrue(last_date <= bookinstance.due_back)
                last_date = bookinstance.due_back