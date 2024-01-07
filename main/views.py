from django.shortcuts import render

from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework import views, generics
from rest_framework.status import *
from rest_framework.response import Response


from main.models import *
from .serializers import *
from django.http import Http404
from datetime import date
#from .permissions import IsAuthorOrReadOnly




class CommentListView(views.APIView): #챌린지에 달린 댓글 보기
    serializer_class = CommentsSerializer

    def get(self, request, pk):
        comment = Comments.objects.filter(challenge=pk)
        
        if comment.exists():
            serializer = self.serializer_class(comment, many=True, context={'request': request})
            return Response({'message': '댓글 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            raise Http404("찾을 수 없습니다.")
        

# Create your views here.
class CommentView(views.APIView): 
    serializer_class = CommentsSerializer

    def post(self, request, pk):
        challenge = get_object_or_404(Challenge, pk=pk)
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save( challenge=challenge)
            return Response({'message': '댓글 작성 성공', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '댓글 작성 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CommentRView(views.APIView): 
    serializer_class=CommentsSerializer 

    def get_object(self, pk):
        challenge = get_object_or_404(Challenge, pk=pk)
        self.check_object_permissions(self.request, challenge)
        return challenge
    
    def patch(self, request, pk, comment_pk):
        challenge = self.get_object(pk=pk)
        comment = get_object_or_404(Comments, challenge=challenge, pk=comment_pk)
        serializer = self.serializer_class(instance=comment, data=request.data, partial=True,
                                    context={'request': request})
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': '댓글 수정 성공', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '댓글 수정 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, comment_pk):
        challenge = self.get_object(pk=pk)
        comment = get_object_or_404(Comments, challenge=challenge, pk=comment_pk)
        comment.delete()
        
        return Response({'message': '댓글 삭제 성공'}, status=status.HTTP_200_OK)


class RecommentView(views.APIView): 
    serializer_class = RecommentsSerializer 

    def post(self, request, comment_pk):
        comment = get_object_or_404(Comments, pk=comment_pk)
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(comment=comment)
            return Response({'message': '대댓글 작성 성공', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '대댓글 작성 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class DeleteGoalView(views.APIView): 
    serializer_class = GoalsSerializer 

    def get_object(self, goal_pk):
        goal = get_object_or_404(Goals, pk=goal_pk)
        self.check_object_permissions(self.request, goal)
        return goal

    def patch(self, request, goal_pk):
        goal =Goals.objects.get( pk=goal_pk)
        goal.activate = not goal.activate  # 반전
        goal.save()

        goal_serializer = GoalsSerializer(goal)

        return Response({'message' : '활성화 여부 변경 성공', 'data' : goal_serializer.data})


    
class  DeleteChallengeView(views.APIView): 
    serializer_class = ChallengeSerializer

    def get_object(self, challenge_pk):
        challenge = get_object_or_404(Challenge, pk=challenge_pk)
        self.check_object_permissions(self.request, challenge)
        return challenge
    
    def delete(self, request, challenge_pk):
        challenge = self.get_object(challenge_pk)
        challenge.delete()
        
        return Response({'message': '챌린지 그만두기 성공'}, status=status.HTTP_200_OK)

class ChallengeListView(views.APIView):
    def get_queryset(self):
        user = self.request.user
        return user.challenge_set.all()

    def get(self, request):
        challenges = self.get_queryset()
        serializer = GoalChallengeSerializer(challenges, many=True)

        if challenges.exists():
            return Response({'message': '챌린지 & 목표 목록 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '내가 만든 챌린지가 없습니다.'})

class ChallengeAddView(views.APIView):
    serializer_class = ChallengeSerializer

    def get(self, request):
        challenges=Challenge.objects.all().order_by('-created_at')
        challenge_serializer = self.serializer_class(challenges, many=True)
        return Response({'message': '챌린지 & 목표 목록 조회 성공', 'data': challenge_serializer.data})


    def post(self, request):
        challenge_serializer =  self.serializer_class(data=request.data)
        if challenge_serializer.is_valid(raise_exception=True):
            challenge_serializer.save(user=request.user)
            return Response({'message': '챌린지 작성 성공', 'data': challenge_serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '챌린지 작성 실패', 'data': challenge_serializer.errors}, status=HTTP_400_BAD_REQUEST)

class GoalAddView(views.APIView):
    serializer_class = GoalsSerializer

    def get(self, request, challenge_pk):
        challenge = get_object_or_404(Challenge, pk=challenge_pk)
        goal = Goals.objects.filter(challenge=challenge)
        serializer = self.serializer_class(goal, many=True)
        return Response({'message': '목표 목록 조회 성공', 'data': serializer.data})

    def post(self, request, challenge_pk):
        challenge=get_object_or_404(Challenge, pk=challenge_pk)
        #현재 목표의 수 확인
        current_goal_count=Goals.objects.filter(challenge=challenge).count()
        #목표가 3개 이상이면 에러 응답
        if current_goal_count >= 3:
            return Response({'message': '최대 3개의 목표까지만 작성할 수 있습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(challenge=challenge)
            goals = Goals.objects.filter(challenge=challenge)
            serializer = self.serializer_class(goals, many=True)
            return Response({'message': '목표 생성 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '목표 생성 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)

class AchievementView(views.APIView):
    serializer_class = AchieveSerializer

    def get(self, request, goal_pk):
        goal = get_object_or_404(Goals, pk=goal_pk)
        achieve = get_object_or_404(Achieve, goal=goal, today=True)
        self.check_object_permissions(request, achieve)

        # 이 부분에서 원하는 로직을 추가하거나 필요하면 데이터를 직접 반환
        achieve_serializer = AchieveSerializer(achieve)
        return Response({'message': '오늘 목표 조회 성공', 'data': achieve_serializer.data})

    def patch(self, request, goal_pk):
        achieve = get_object_or_404(Achieve, goal__pk=goal_pk, today=True)
        achieve.is_done = not achieve.is_done  # 반대로 변경
        achieve.save()
        achieve_serializer = AchieveSerializer(achieve)

        return Response({'message': '목표 달성 여부 변경 성공', 'data': achieve_serializer.data})

class ReactionView(views.APIView):
    EMOTION_TYPES = ['good', 'question', 'fighting', 'fire', 'mark', 'heart']

    def get_emotion_counts(self, challenge, emotion_type):
        if emotion_type not in self.EMOTION_TYPES:
            return {}

        emotion_field = getattr(challenge, emotion_type)
        count = emotion_field.count()

        return {f'{emotion_type}_count': count}

    def post(self, request, challenge_id, emotion_type):
        try:
            challenge = Challenge.objects.get(pk=challenge_id)
        except Challenge.DoesNotExist:
            return Response({'error': 'Challenge not found'}, status=status.HTTP_404_NOT_FOUND)

        if emotion_type not in self.EMOTION_TYPES:
            return Response({'error': 'Invalid emotion type'}, status=status.HTTP_400_BAD_REQUEST)

        emotion_field = getattr(challenge, emotion_type)

        if emotion_field.filter(id=request.user.id).exists():
            emotion_field.remove(request.user)
            is_selected = False
        else:
            emotion_field.add(request.user)
            is_selected = True

        # 감정 개수도 반환
        emotion_counts = self.get_emotion_counts(challenge, emotion_type)

        response_data = {
            'message': f'{emotion_type} 리액션 변경 성공',
            'data': {
                'challenge_id': challenge_id,
                'emotion_type': emotion_type,
                'is_selected': is_selected,
                **emotion_counts,
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)
