"""
Tests for the ActivatorModel, ActivatorQuerySet, and ActivatorModelManager.

This module tests the Common app's ActivatorModel functionality including:
- QuerySet active() and inactive() methods
- ModelManager active() and inactive() methods
- Status filtering behavior
- Default status values
"""

from django.db import models

import pytest

from apps.Common.models.ActivatorModel import (
    ActivatorModel,
    ActivatorModelManager,
    ActivatorQuerySet,
)

pytestmark = pytest.mark.django_db


# =============================================================================
# Test Model Creation (Concrete Implementation)
# =============================================================================


class ConcreteActivatorItem(ActivatorModel):
    """Concrete model for testing ActivatorModel abstract base class."""

    name = models.CharField(max_length=100)

    class Meta:
        app_label = "Common"


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def create_test_items(db):
    """Create test items with different statuses."""
    # Ensure the table exists for testing
    from django.db import connection

    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(ConcreteActivatorItem)

    # Create active items
    active_item1 = ConcreteActivatorItem.objects.create(
        name="Active Item 1", status=ActivatorModel.ACTIVE_STATUS
    )
    active_item2 = ConcreteActivatorItem.objects.create(
        name="Active Item 2", status=ActivatorModel.ACTIVE_STATUS
    )

    # Create inactive items
    inactive_item1 = ConcreteActivatorItem.objects.create(
        name="Inactive Item 1", status=ActivatorModel.INACTIVE_STATUS
    )
    inactive_item2 = ConcreteActivatorItem.objects.create(
        name="Inactive Item 2", status=ActivatorModel.INACTIVE_STATUS
    )

    yield {
        "active": [active_item1, active_item2],
        "inactive": [inactive_item1, inactive_item2],
        "all": [active_item1, active_item2, inactive_item1, inactive_item2],
    }

    # Cleanup
    ConcreteActivatorItem.objects.all().delete()
    with connection.schema_editor() as schema_editor:
        schema_editor.delete_model(ConcreteActivatorItem)


# =============================================================================
# QuerySet Tests
# =============================================================================


class TestActivatorQuerySet:
    """Test cases for ActivatorQuerySet methods."""

    def test_queryset_active_filters_active_items(self, create_test_items):
        """
        Test that QuerySet.active() returns only items with ACTIVE_STATUS.

        Verifies that the active() method correctly filters the queryset
        to include only items with status=ACTIVE_STATUS.
        """
        active_items = ConcreteActivatorItem.objects.all().active()

        assert active_items.count() == 2
        assert all(item.status == ActivatorModel.ACTIVE_STATUS for item in active_items)
        assert set(active_items) == set(create_test_items["active"])

    def test_queryset_inactive_filters_inactive_items(self, create_test_items):
        """
        Test that QuerySet.inactive() returns only items with INACTIVE_STATUS.

        Verifies that the inactive() method correctly filters the queryset
        to include only items with status=INACTIVE_STATUS.
        """
        inactive_items = ConcreteActivatorItem.objects.all().inactive()

        assert inactive_items.count() == 2
        assert all(
            item.status == ActivatorModel.INACTIVE_STATUS for item in inactive_items
        )
        assert set(inactive_items) == set(create_test_items["inactive"])

    def test_queryset_active_returns_empty_when_no_active_items(self, db):
        """
        Test that QuerySet.active() returns empty queryset when no active items exist.

        Verifies that the active() method returns an empty queryset
        when all items are inactive.
        """
        # Ensure the table exists
        from django.db import connection

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(ConcreteActivatorItem)

        # Create only inactive items
        ConcreteActivatorItem.objects.create(
            name="Inactive Item", status=ActivatorModel.INACTIVE_STATUS
        )

        active_items = ConcreteActivatorItem.objects.all().active()

        assert active_items.count() == 0
        assert list(active_items) == []

        # Cleanup
        ConcreteActivatorItem.objects.all().delete()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(ConcreteActivatorItem)

    def test_queryset_inactive_returns_empty_when_no_inactive_items(self, db):
        """
        Test that QuerySet.inactive() returns empty queryset when no inactive items exist.

        Verifies that the inactive() method returns an empty queryset
        when all items are active.
        """
        # Ensure the table exists
        from django.db import connection

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(ConcreteActivatorItem)

        # Create only active items
        ConcreteActivatorItem.objects.create(
            name="Active Item", status=ActivatorModel.ACTIVE_STATUS
        )

        inactive_items = ConcreteActivatorItem.objects.all().inactive()

        assert inactive_items.count() == 0
        assert list(inactive_items) == []

        # Cleanup
        ConcreteActivatorItem.objects.all().delete()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(ConcreteActivatorItem)

    def test_queryset_active_can_be_chained(self, create_test_items):
        """
        Test that QuerySet.active() can be chained with other QuerySet methods.

        Verifies that the active() method returns a proper QuerySet
        that can be further filtered.
        """
        # Create an additional active item with a specific name
        from django.db import connection

        specific_item = ConcreteActivatorItem.objects.create(
            name="Specific Active Item", status=ActivatorModel.ACTIVE_STATUS
        )

        active_specific = ConcreteActivatorItem.objects.active().filter(
            name="Specific Active Item"
        )

        assert active_specific.count() == 1
        assert active_specific.first() == specific_item

        # Cleanup
        specific_item.delete()

    def test_queryset_inactive_can_be_chained(self, create_test_items):
        """
        Test that QuerySet.inactive() can be chained with other QuerySet methods.

        Verifies that the inactive() method returns a proper QuerySet
        that can be further filtered.
        """
        # Create an additional inactive item with a specific name
        specific_item = ConcreteActivatorItem.objects.create(
            name="Specific Inactive Item", status=ActivatorModel.INACTIVE_STATUS
        )

        inactive_specific = ConcreteActivatorItem.objects.inactive().filter(
            name="Specific Inactive Item"
        )

        assert inactive_specific.count() == 1
        assert inactive_specific.first() == specific_item

        # Cleanup
        specific_item.delete()


# =============================================================================
# ModelManager Tests
# =============================================================================


class TestActivatorModelManager:
    """Test cases for ActivatorModelManager methods."""

    def test_manager_active_filters_active_items(self, create_test_items):
        """
        Test that ModelManager.active() returns only items with ACTIVE_STATUS.

        Verifies that the manager's active() method correctly filters
        to include only items with status=ACTIVE_STATUS.
        """
        active_items = ConcreteActivatorItem.objects.active()

        assert active_items.count() == 2
        assert all(item.status == ActivatorModel.ACTIVE_STATUS for item in active_items)
        assert set(active_items) == set(create_test_items["active"])

    def test_manager_inactive_filters_inactive_items(self, create_test_items):
        """
        Test that ModelManager.inactive() returns only items with INACTIVE_STATUS.

        Verifies that the manager's inactive() method correctly filters
        to include only items with status=INACTIVE_STATUS.
        """
        inactive_items = ConcreteActivatorItem.objects.inactive()

        assert inactive_items.count() == 2
        assert all(
            item.status == ActivatorModel.INACTIVE_STATUS for item in inactive_items
        )
        assert set(inactive_items) == set(create_test_items["inactive"])

    def test_manager_active_returns_empty_when_no_active_items(self, db):
        """
        Test that ModelManager.active() returns empty queryset when no active items exist.

        Verifies that the manager's active() method returns an empty queryset
        when all items are inactive.
        """
        # Ensure the table exists
        from django.db import connection

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(ConcreteActivatorItem)

        # Create only inactive items
        ConcreteActivatorItem.objects.create(
            name="Inactive Item", status=ActivatorModel.INACTIVE_STATUS
        )

        active_items = ConcreteActivatorItem.objects.active()

        assert active_items.count() == 0
        assert list(active_items) == []

        # Cleanup
        ConcreteActivatorItem.objects.all().delete()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(ConcreteActivatorItem)

    def test_manager_inactive_returns_empty_when_no_inactive_items(self, db):
        """
        Test that ModelManager.inactive() returns empty queryset when no inactive items exist.

        Verifies that the manager's inactive() method returns an empty queryset
        when all items are active.
        """
        # Ensure the table exists
        from django.db import connection

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(ConcreteActivatorItem)

        # Create only active items
        ConcreteActivatorItem.objects.create(
            name="Active Item", status=ActivatorModel.ACTIVE_STATUS
        )

        inactive_items = ConcreteActivatorItem.objects.inactive()

        assert inactive_items.count() == 0
        assert list(inactive_items) == []

        # Cleanup
        ConcreteActivatorItem.objects.all().delete()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(ConcreteActivatorItem)

    def test_manager_active_can_be_chained(self, create_test_items):
        """
        Test that ModelManager.active() can be chained with other QuerySet methods.

        Verifies that the manager's active() method returns a proper QuerySet
        that can be further filtered.
        """
        # Create an additional active item with a specific name
        specific_item = ConcreteActivatorItem.objects.create(
            name="Manager Active Item", status=ActivatorModel.ACTIVE_STATUS
        )

        active_specific = ConcreteActivatorItem.objects.active().filter(
            name="Manager Active Item"
        )

        assert active_specific.count() == 1
        assert active_specific.first() == specific_item

        # Cleanup
        specific_item.delete()

    def test_manager_inactive_can_be_chained(self, create_test_items):
        """
        Test that ModelManager.inactive() can be chained with other QuerySet methods.

        Verifies that the manager's inactive() method returns a proper QuerySet
        that can be further filtered.
        """
        # Create an additional inactive item with a specific name
        specific_item = ConcreteActivatorItem.objects.create(
            name="Manager Inactive Item", status=ActivatorModel.INACTIVE_STATUS
        )

        inactive_specific = ConcreteActivatorItem.objects.inactive().filter(
            name="Manager Inactive Item"
        )

        assert inactive_specific.count() == 1
        assert inactive_specific.first() == specific_item

        # Cleanup
        specific_item.delete()

    def test_manager_returns_activator_queryset(self):
        """
        Test that ModelManager.get_queryset() returns an ActivatorQuerySet instance.

        Verifies that the custom manager properly returns the custom QuerySet class.
        """
        # Ensure the table exists
        from django.db import connection

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(ConcreteActivatorItem)

        queryset = ConcreteActivatorItem.objects.get_queryset()

        assert isinstance(queryset, ActivatorQuerySet)

        # Cleanup
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(ConcreteActivatorItem)


# =============================================================================
# Model Default Behavior Tests
# =============================================================================


class TestActivatorModelDefaults:
    """Test cases for ActivatorModel default behavior."""

    def test_default_status_is_active(self, db):
        """
        Test that new instances default to ACTIVE_STATUS.

        Verifies that items created without specifying status
        are automatically set to active.
        """
        # Ensure the table exists
        from django.db import connection

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(ConcreteActivatorItem)

        item = ConcreteActivatorItem.objects.create(name="Default Item")

        assert item.status == ActivatorModel.ACTIVE_STATUS

        # Cleanup
        item.delete()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(ConcreteActivatorItem)

    def test_can_create_inactive_item(self, db):
        """
        Test that items can be explicitly created as inactive.

        Verifies that the INACTIVE_STATUS can be set during creation.
        """
        # Ensure the table exists
        from django.db import connection

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(ConcreteActivatorItem)

        item = ConcreteActivatorItem.objects.create(
            name="Inactive Item", status=ActivatorModel.INACTIVE_STATUS
        )

        assert item.status == ActivatorModel.INACTIVE_STATUS

        # Cleanup
        item.delete()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(ConcreteActivatorItem)

    def test_activate_date_auto_set_on_save(self, db):
        """
        Test that activate_date is automatically set if not provided.

        Verifies that the save() method sets activate_date to now()
        when it's not explicitly provided.
        """
        # Ensure the table exists
        from django.db import connection

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(ConcreteActivatorItem)

        item = ConcreteActivatorItem.objects.create(name="Item Without Date")

        assert item.activate_date is not None

        # Cleanup
        item.delete()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(ConcreteActivatorItem)
