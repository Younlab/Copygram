from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from rest_framework import status


class Feed(APIView):
    def get(self, request, format=None):
        # 요청을 보낸 유저
        user = request.user

        # 유저의 following 목록
        following_users = user.following.all()
        image_list = []

        # 유저의 following 중인 유저들의 포스트 목록을 불러온 후에 하나의 리스트로 합치기
        for following_user in following_users:
            image_list += following_user.images.all()[:2]

        # 최신 순으로정렬
        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)
        serializer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(data=serializer.data)


class LikeImage(APIView):
    def get(self, request, image_id, format=None):
        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisiting_like = models.Like.objects.get(
                creator=request.user,
                image=found_image,
            )
            preexisiting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Like.DoesNotExist:

            new_like = models.Like.objects.create(
                creator=request.user,
                image=found_image
            )
            new_like.save()

            return Response(status=status.HTTP_201_CREATED)
