from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView


from .check_service import post_submission
from .models import Problem, Submission
from .serializers import SubmissionSerializer


class ProblemListView(ListView):
    """
    Render main page with problems list
    """
    model = Problem
    template_name = 'main/problem_list.html'


class ProblemView(DetailView):
    """
    Render page with single problem
    """
    model = Problem
    template_name = 'main/problem_page.html'


class SubmissionDetailApiView(RetrieveAPIView):
    """
    Return serialized submission by id
    """
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class SubmissionListApiView(APIView):
    """
    Return list of submissions
    """
    def get(self, request, *args, **kwargs):
        submissions_qs = Submission.objects
        problem_id = self.request.query_params.get('problem')
        if problem_id:
            submissions_qs = submissions_qs.filter(problem_id=problem_id)
        return Response(SubmissionSerializer(submissions_qs, many=True).data)


class ReceiveSubmissionApiView(APIView):
    """
    Receive submission and send to check
    """
    authentication_classes = []

    def post(self, request, problem_id: int):
        data = request.data
        problem = get_object_or_404(Problem, id=problem_id)

        result = dict()
        if 'code' in data:
            submission_id, submission_status = post_submission(problem.id, data['code'])

            result['submission_id'] = submission_id
            result['status'] = submission_status
        else:
            result['status'] = 'Нет решения в запросе'
        return Response(result)
