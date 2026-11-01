import hashlib
import json

from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post, IdempotencyRecord
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        key = request.headers.get('Idempotency-Key')

        if not key:
            return Response(
                {"error": "Idempotency-Key header is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request_data = json.dumps(request.data, sort_keys=True)

        request_hash = hashlib.sha256(
            request_data.encode('utf-8')
        ).hexdigest()

        with transaction.atomic():
            record = IdempotencyRecord.objects.filter(key=key).first()

            if record:
                if record.request_hash != request_hash:
                    return Response(
                        {"error": "Idempotency key reused with different request data"},
                        status=status.HTTP_409_CONFLICT
                    )

                return Response(
                    record.response_data,
                    status=record.status_code
                )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(author=request.user)

            response_data = serializer.data

            IdempotencyRecord.objects.create(
                key=key,
                request_hash=request_hash,
                response_data=response_data,
                status_code=status.HTTP_201_CREATED
            )

            return Response(
                response_data,
                status=status.HTTP_201_CREATED
            )


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]