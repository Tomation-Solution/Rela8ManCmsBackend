from rest_framework import viewsets, pagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializer
from utils import custom_permissions


class SliderPagination(pagination.PageNumberPagination):
    page_size = 5  # Default page size
    page_size_query_param = "page_size"  # Allows clients to override page size
    max_page_size = 100


class HomePageSliderViewset(viewsets.ModelViewSet):
    serializer_class = serializer.HomePageSliderSerializer
    permission_classes = [custom_permissions.IsAuthenticated]
    pagination_class = SliderPagination

    def get_queryset(self):
        archived = self.request.query_params.get("archived", "false").lower() == "true"
        return models.HomePageSlider.objects.filter(is_archived=archived).order_by(
            "order_position", "id"
        )

    @action(detail=False, methods=["get"], permission_classes=[])
    def get_slider(self, request, pk=None):
        queryset = self.get_queryset()

        # Apply pagination manually
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[custom_permissions.IsAuthenticated],
    )
    def archive_slider(self, request, pk=None):
        try:
            slider = self.get_object()  # Retrieves the object with the given pk
            if slider.is_archived is True:
                slider.is_archived = False
            else:
                slider.is_archived = True

            slider.save()
            serializer = self.serializer_class(slider, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.HomePageSlider.DoesNotExist:
            return Response(
                {"error": "Slider not found"}, status=status.HTTP_404_NOT_FOUND
            )


class FooterContentViewset(viewsets.ModelViewSet):
    serializer_class = serializer.FooterContentSerializer
    permission_classes = [custom_permissions.IsAuthenticated]

    def get_queryset(self):
        return models.FooterContent.objects.all()

    def get_object(self):
        """Always return the single footer content instance"""
        return models.FooterContent.get_instance()

    def list(self, request, *args, **kwargs):
        """Return the single footer content instance"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Return the single footer content instance"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create or update the single footer content instance"""
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        """Update the single footer content instance"""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Partial update the single footer content instance"""
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Prevent deletion of footer content"""
        return Response(
            {"error": "Footer content cannot be deleted"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @action(detail=False, methods=["get"], permission_classes=[])
    def content(self, request):
        """Public endpoint to get footer content"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["patch"],
        permission_classes=[custom_permissions.IsAuthenticated],
    )
    def update_content(self, request):
        """Update footer content"""
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Footer content updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK,
        )
