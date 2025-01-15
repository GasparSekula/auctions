from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import AuctionItem, User, Notification


class AuctionViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Log in the user
        self.client.login(username="testuser", password="testpass")

        # Create some auction items
        self.auction1 = AuctionItem.objects.create(
            title="Test Auction 1",
            description="Description of auction 1",
            current_price=10.00,
            starting_price=5.00,
            auction_end_date=timezone.make_aware(timezone.datetime(2025, 12, 31)),
            created_by=self.user,
        )
        self.auction2 = AuctionItem.objects.create(
            title="Test Auction 2",
            description="Description of auction 2",
            current_price=20.00,
            starting_price=10.00,
            auction_end_date=timezone.make_aware(timezone.datetime(2025, 12, 31)),
            created_by=self.user,
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/home.html')
        self.assertContains(response, "Welcome to the Auctionary!")

    def test_auction_list_view(self):
        response = self.client.get(reverse('auction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/auction_list.html')
        self.assertContains(response, self.auction1.title)
        self.assertContains(response, self.auction2.title)

    def test_auction_detail_view(self):
        response = self.client.get(reverse('auction_detail', args=[self.auction1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/auction_detail.html')
        self.assertContains(response, self.auction1.title)
        self.assertContains(response, self.auction1.description)

    def test_search_view_with_results(self):
        response = self.client.get(reverse('search'), {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.auction1.title)
        self.assertContains(response, self.auction2.title)

    def test_search_view_no_results(self):
        response = self.client.get(reverse('search'), {'search': 'NonExistent'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No results found")

    def test_create_auction_view_get(self):
        response = self.client.get(reverse('auction_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/auction_create.html')

    def test_create_auction_view_post_valid_data(self):
        data = {
            'title': 'New Auction',
            'description': 'Description of new auction',
            'starting_price': 10.00,
            'auction_end_date': '2024-12-31',
        }
        response = self.client.post(reverse('auction_create'), data)
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(AuctionItem.objects.filter(title='New Auction').exists())

    def test_create_auction_view_post_invalid_data(self):
        data = {
            'title': '',  # Missing title
            'description': 'Description of invalid auction',
        }
        response = self.client.post(reverse('auction_create'), data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered
        self.assertContains(response, "This field is required.")

    def test_export_auctions_csv(self):
        response = self.client.get(reverse('export_auctions', args=['excel']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="auctions.csv"', response['Content-Disposition'])

    def test_export_auctions_xml(self):
        response = self.client.get(reverse('export_auctions', args=['xml']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertIn('attachment; filename="auctions.xml"', response['Content-Disposition'])

    def test_user_auctions(self):
        response = self.client.get(reverse('user_auctions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/user_auctions.html')
        self.assertContains(response, self.auction1.title)
        self.assertContains(response, self.auction2.title)

    def test_notifications(self):
        Notification.objects.create(user=self.user, message="Test notification")
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/notifications.html')
        self.assertContains(response, "Test notification")

    def test_view_watchlist(self):
        self.user.watchlist.add(self.auction1)
        response = self.client.get(reverse('view_watchlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/watchlist.html')
        self.assertContains(response, self.auction1.title)
