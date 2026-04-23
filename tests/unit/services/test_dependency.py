from inspect import signature
from unittest.mock import AsyncMock, Mock, patch

import pytest

from layered_architecture.enums import ServiceType
from layered_architecture.services.dependency import DependencyService


class TestDependencyService:
    def test_get_order_service_requires_explicit_db_argument(self) -> None:
        # Given
        get_order_service_signature = signature(
            DependencyService.get_order_service
        )

        # When
        db_parameter = get_order_service_signature.parameters["db"]

        # Then
        assert "db" in get_order_service_signature.parameters
        assert db_parameter.default is db_parameter.empty

    @pytest.mark.asyncio
    async def test_get_order_service_delegates_to_order_service_factory(
        self,
    ) -> None:
        # Given
        db = Mock(name="db_session")
        expected_service = Mock(name="order_service")

        with patch(
            "layered_architecture.services.dependency.OrderServiceFactory"
        ) as order_service_factory:
            factory_instance = order_service_factory.return_value
            factory_instance.get_service_by_service_type.return_value = (
                expected_service
            )

            # When
            result = await DependencyService.get_order_service(
                ServiceType.DELIVERY,
                db,
            )

            # Then
            assert result is expected_service
            order_service_factory.assert_called_once_with(db)
            factory_instance.get_service_by_service_type.assert_called_once_with(
                ServiceType.DELIVERY
            )

    @pytest.mark.asyncio
    async def test_get_order_service_by_id_delegates_to_order_service_factory(
        self,
    ) -> None:
        # Given
        db = Mock(name="db_session")
        expected_service = Mock(name="order_service")

        with patch(
            "layered_architecture.services.dependency.OrderServiceFactory"
        ) as order_service_factory:
            factory_instance = order_service_factory.return_value
            factory_instance.get_service_by_order_id = AsyncMock(
                return_value=expected_service
            )

            # When
            result = await DependencyService.get_order_service_by_id(
                "order-123",
                db,
            )

            # Then
            assert result is expected_service
            order_service_factory.assert_called_once_with(db)
            factory_instance.get_service_by_order_id.assert_awaited_once_with(
                "order-123"
            )
