"""
Unit tests for PriceAlert model and views.
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock

from .models import PriceAlert, PriceHistory
from .serializers import PriceAlertSerializer, PriceAlertCreateSerializer
from .services import PriceAlertService

User = get_user_model()


class PriceAlertModelTest(TestCase):
    """Test cases for PriceAlert model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_price_alert(self):
        """Test creating a price alert."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE'
        )
        self.assertEqual(alert.user, self.user)
        self.assertEqual(alert.target_price, Decimal('2800.00'))
        self.assertEqual(alert.condition, 'ABOVE')
        self.assertTrue(alert.is_active)
        self.assertFalse(alert.is_triggered)
        self.assertIsNone(alert.triggered_at)

    def test_price_alert_str(self):
        """Test string representation of PriceAlert."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE'
        )
        expected = f"{self.user.email} - ABOVE 2800.00 THB/g"
        self.assertEqual(str(alert), expected)

    def test_check_alert_above_condition(self):
        """Test checking alert with ABOVE condition."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE'
        )
        # Current price is below target, should not trigger
        self.assertFalse(alert.check_alert(Decimal('2700.00')))
        # Current price equals target, should trigger
        self.assertTrue(alert.check_alert(Decimal('2800.00')))
        # Current price is above target, should trigger
        self.assertTrue(alert.check_alert(Decimal('2900.00')))

    def test_check_alert_below_condition(self):
        """Test checking alert with BELOW condition."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='BELOW'
        )
        # Current price is above target, should not trigger
        self.assertFalse(alert.check_alert(Decimal('2900.00')))
        # Current price equals target, should trigger
        self.assertTrue(alert.check_alert(Decimal('2800.00')))
        # Current price is below target, should trigger
        self.assertTrue(alert.check_alert(Decimal('2700.00')))

    def test_check_alert_inactive(self):
        """Test that inactive alerts don't trigger."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE',
            is_active=False
        )
        self.assertFalse(alert.check_alert(Decimal('2900.00')))

    def test_check_alert_already_triggered(self):
        """Test that already triggered alerts don't trigger again."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE',
            is_triggered=True
        )
        self.assertFalse(alert.check_alert(Decimal('2900.00')))

    def test_trigger_alert(self):
        """Test triggering an alert."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE'
        )
        result = alert.trigger()
        self.assertTrue(result)
        self.assertTrue(alert.is_triggered)
        self.assertFalse(alert.is_active)
        self.assertIsNotNone(alert.triggered_at)

    def test_trigger_already_triggered_alert(self):
        """Test triggering an already triggered alert."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE',
            is_triggered=True
        )
        result = alert.trigger()
        self.assertFalse(result)


class PriceAlertSerializerTest(TestCase):
    """Test cases for PriceAlert serializers."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_price_alert_create_serializer_valid(self):
        """Test creating a valid alert with CreateSerializer."""
        data = {
            'target_price': '2800.00',
            'condition': 'ABOVE'
        }
        serializer = PriceAlertCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_price_alert_create_serializer_invalid_price_zero(self):
        """Test validation rejects zero price."""
        data = {
            'target_price': '0',
            'condition': 'ABOVE'
        }
        serializer = PriceAlertCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_price_alert_create_serializer_invalid_negative_price(self):
        """Test validation rejects negative price."""
        data = {
            'target_price': '-100.00',
            'condition': 'ABOVE'
        }
        serializer = PriceAlertCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_price_alert_serializer_read_only_fields(self):
        """Test that read-only fields are protected."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE'
        )
        serializer = PriceAlertSerializer(alert)
        self.assertIn('id', serializer.data)
        self.assertIn('user_email', serializer.data)
        self.assertIn('is_triggered', serializer.data)


class PriceAlertViewTest(APITestCase):
    """Test cases for PriceAlert views."""

    def setUp(self):
        """Set up test data."""
        # Clear all alerts first
        PriceAlert.objects.all().delete()
        User.objects.filter(username__in=['testuser', 'otheruser']).delete()
        
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_list_price_alerts(self):
        """Test listing price alerts for authenticated user."""
        # Create alerts for the user
        PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE'
        )
        PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2700.00'),
            condition='BELOW'
        )

        # Create alert for different user
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        PriceAlert.objects.create(
            user=other_user,
            target_price=Decimal('2900.00'),
            condition='ABOVE'
        )

        response = self.client.get('/api/alerts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        self.assertEqual(len(data), 2)  # Only user's alerts

    def test_create_price_alert(self):
        """Test creating a new price alert."""
        data = {
            'target_price': '2800.00',
            'condition': 'ABOVE'
        }
        response = self.client.post('/api/alerts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PriceAlert.objects.count(), 1)

    def test_create_price_alert_invalid(self):
        """Test creating an alert with invalid data."""
        data = {
            'target_price': '-100.00',
            'condition': 'ABOVE'
        }
        response = self.client.post('/api/alerts/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_price_alert(self):
        """Test retrieving a specific price alert."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE'
        )
        response = self.client.get(f'/api/alerts/{alert.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], alert.id)

    def test_update_price_alert(self):
        """Test updating a price alert."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE'
        )
        data = {
            'target_price': '2900.00',
            'condition': 'BELOW',
            'is_active': False
        }
        response = self.client.patch(f'/api/alerts/{alert.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        alert.refresh_from_db()
        self.assertEqual(alert.target_price, Decimal('2900.00'))
        self.assertEqual(alert.condition, 'BELOW')
        self.assertFalse(alert.is_active)

    def test_delete_price_alert(self):
        """Test deleting a price alert."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE'
        )
        response = self.client.delete(f'/api/alerts/{alert.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PriceAlert.objects.count(), 0)

    def test_toggle_price_alert_activate(self):
        """Test activating an alert via toggle endpoint."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE',
            is_active=False
        )
        response = self.client.post(f'/api/alerts/{alert.id}/toggle/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_active'])

        alert.refresh_from_db()
        self.assertTrue(alert.is_active)

    def test_toggle_price_alert_deactivate(self):
        """Test deactivating an alert via toggle endpoint."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE',
            is_active=True
        )
        response = self.client.post(f'/api/alerts/{alert.id}/toggle/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_active'])

        alert.refresh_from_db()
        self.assertFalse(alert.is_active)

    def test_unauthorized_access(self):
        """Test that unauthenticated users cannot access alerts."""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/alerts/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PriceAlertServiceTest(TestCase):
    """Test cases for PriceAlertService."""

    def setUp(self):
        """Set up test data."""
        # Clear all alerts first
        PriceAlert.objects.all().delete()
        User.objects.filter(username__in=['testuser', 'testuser2']).delete()
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )

    @patch('core.services.PriceAlertService._send_alert_notification')
    def test_check_and_trigger_alerts_above(self, mock_send):
        """Test checking and triggering alerts with ABOVE condition."""
        # Create alerts
        alert1 = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE'
        )
        alert2 = PriceAlert.objects.create(
            user=self.user2,
            target_price=Decimal('2900.00'),
            condition='ABOVE'
        )

        # Check with price that should trigger alert1 but not alert2
        triggered = PriceAlertService.check_and_trigger_alerts(Decimal('2850.00'))

        self.assertEqual(len(triggered), 1)
        self.assertEqual(triggered[0].id, alert1.id)

        alert1.refresh_from_db()
        self.assertTrue(alert1.is_triggered)

        alert2.refresh_from_db()
        self.assertFalse(alert2.is_triggered)

    @patch('core.services.PriceAlertService._send_alert_notification')
    def test_check_and_trigger_alerts_below(self, mock_send):
        """Test checking and triggering alerts with BELOW condition."""
        alert1 = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='BELOW'
        )
        alert2 = PriceAlert.objects.create(
            user=self.user2,
            target_price=Decimal('2700.00'),
            condition='BELOW'
        )

        # Check with price 2750: triggers alert1 (< 2800) but not alert2 (not < 2700)
        triggered = PriceAlertService.check_and_trigger_alerts(Decimal('2750.00'))

        self.assertEqual(len(triggered), 1)
        self.assertEqual(triggered[0].id, alert1.id)

        alert1.refresh_from_db()
        self.assertTrue(alert1.is_triggered)

        alert2.refresh_from_db()
        self.assertFalse(alert2.is_triggered)

    @patch('core.services.PriceAlertService._send_alert_notification')
    def test_check_and_trigger_multiple_alerts(self, mock_send):
        """Test triggering multiple alerts at once."""
        alert1 = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='BELOW'
        )
        alert2 = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2900.00'),
            condition='BELOW'
        )

        # Both should trigger
        triggered = PriceAlertService.check_and_trigger_alerts(Decimal('2700.00'))

        self.assertEqual(len(triggered), 2)

    def test_check_inactive_alerts(self):
        """Test that inactive alerts are not triggered."""
        alert = PriceAlert.objects.create(
            user=self.user,
            target_price=Decimal('2800.00'),
            condition='ABOVE',
            is_active=False
        )

        triggered = PriceAlertService.check_and_trigger_alerts(Decimal('2900.00'))

        self.assertEqual(len(triggered), 0)
        alert.refresh_from_db()
        self.assertFalse(alert.is_triggered)

    def test_broadcast_price_update(self):
        """Test broadcasting price updates."""
        price_data = {
            'price_per_gram': Decimal('2800.00'),
            'price_per_baht': Decimal('42683.20'),
            'currency': 'THB',
            'timestamp': timezone.now()
        }

        # Mock the channel layer to avoid actual WebSocket
        with patch('core.services.get_channel_layer') as mock_get_layer:
            mock_channel_layer = MagicMock()
            mock_get_layer.return_value = mock_channel_layer

            PriceAlertService.broadcast_price_update(price_data)

            # Verify group_send was called
            mock_channel_layer.group_send.assert_called()
