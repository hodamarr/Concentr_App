from rest_framework import generics, mixins, status
import random as r
import string
from .serializers import *
from rest_framework.permissions import (
    IsAuthenticated,
    BasePermission, AllowAny,
)
from rest_framework.request import Request
from rest_framework.response import Response
from dateutil import parser
#from concentrApp.celery import add_task, get_day
from .tasks import task
import datetime

class ReturnResponse():
    @staticmethod
    def return_201_success_post(data) -> Response:
        return Response({'data': data},
                        status=status.HTTP_201_CREATED)

    @staticmethod
    def return_200_success_get(data) -> Response:
        return Response({'data': data},
                        status=status.HTTP_200_OK)

    @staticmethod
    def return_404_not_found(message) -> Response:
        return Response({'error': message},
                        status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def return_400_bed_request(message) -> Response:
        return Response({'error': message},
                        status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def return_500_internal_server_error(error_message):
        response_data = {
            'error': error_message
        }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IsExperimentAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.exp_admin == request.user


class ExperimentListCreateView(generics.GenericAPIView,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.UpdateModelMixin):
    serializer_class = ExperimentSerializer
    queryset = Experiment.objects.all()
    permission_classes = [IsAuthenticated, IsExperimentAdminPermission]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(exp_admin=user)
        return super().perform_create(serializer)

    def get(self, request: Request, *args, **kwargs):
        user_id = request.user.id
        # Retrieve all experiments for the user with the given user ID
        experiments = Experiment.objects.filter(exp_admin=user_id)
        # Serialize the experiments
        experiment_data = ExperimentSerializer(experiments, many=True).data
        return ReturnResponse.return_200_success_get(data=experiment_data)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        return self.partial_update(request, *args, **kwargs)

class ContextCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = ContextSerializer
    permission_classes = [IsAuthenticated, IsExperimentAdminPermission]

    def post(self, request):
        experiment_name = request.data.get('experiment')
        try:
            experiment = Experiment.objects.get(name=experiment_name)
        except Experiment.DoesNotExist as e:
            return ReturnResponse.return_404_not_found(str(e))
        name = request.data.get('name')
        description = request.data.get('description')
        context = Context.objects.create(
            name=name,
            description=description,
            experiment=experiment
        )
        context.save()
        serializer = self.serializer_class(context)
        return ReturnResponse.return_201_success_post(serializer.data)

    def get(self, request):
        experiment_name = request.headers.get('experiment')
        try:
            experiment = Experiment.objects.get(name=experiment_name)
            data = Context.objects.filter(experiment=experiment)
        except (Experiment.DoesNotExist, Context.DoesNotExist) as e:
            return ReturnResponse.return_400_bed_request(str(e))
        return ReturnResponse.return_200_success_get([{"id": item.id, "name": item.name, "description": item.description} for item in data])


class ParticipantExperimentCreateView(generics.GenericAPIView,
                                      mixins.CreateModelMixin):
    serializer_class = ParticipantExperimentSerializer
    permission_classes = [IsAuthenticated, IsExperimentAdminPermission]

    def post(self, request, *args, **kwargs):
        experiment_id = request.data.get('experiment_id')
        gender = request.data.get('gender')
        is_female = True if gender == 'f' else False
        try:
            experiment = Experiment.objects.get(name=experiment_id)
        except Experiment.DoesNotExist as e:
            return ReturnResponse.return_400_bed_request(str(e))


        participant_code = ''.join(
            r.choices(
                string.ascii_letters +
                string.digits,
                k=15))

        participant = Participant.objects.create(
            participant_code=participant_code,
            is_female=is_female)
        participant.save()

        participant_experiment = ParticipantExperiment.objects.create(
            participant=participant,
            experiment=experiment,
        )
        participant_experiment.save()

        serializer = self.serializer_class(participant_experiment)
        return ReturnResponse.return_201_success_post(serializer.data)

    def get(self, request, *args, **kwargs):
        experiment_id = request.GET.get('experiment')
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Experiment.DoesNotExists as e:
            return ReturnResponse.return_400_bed_request(str(e))

        experiment_participants = ParticipantExperiment.objects.filter(
            experiment=experiment)
        participants = [
            {"code": i.participant.participant_code, "score": i.participant.score,
             "gender": 'f' if i.participant.is_female == True else 'm' } for i in experiment_participants]
        return ReturnResponse.return_200_success_get(participants)


class QuestionCreateList(generics.GenericAPIView,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsExperimentAdminPermission]
    queryset = Question.objects.all()

    def _visit(self, question, is_visited):
        if is_visited[question.id] == False:
            is_visited[question.id] = True
            obj = {
                "id":question.id,
                "description": question.description,
                "created_at": question.created_at,
                "updated_at":question.updated_at,
                "answers": [{"id": i.id, "answer":i.text} for i in Answer.objects.filter(question=question)],
                "childrens":[],
                "related_answer": question.related_answer,
            }
            childrens = Question.objects.filter(parent=question)
            for children in childrens:
                obj["childrens"].append(self._visit(children, is_visited))
            return obj

    def _init_dfs(self, context, father_id=None):
        result = []
        try:
            questions = Question.objects.filter(context=context)
            if father_id:
                top_level_questions = questions.filter(id=father_id)
            else:
                top_level_questions = questions.filter(parent=None)
            is_visited = {i.id: False for i in questions}
            for q in top_level_questions:
                result.append(self._visit(q, is_visited))
        except Exception as e:
            pass
        finally:
            return result

    def get(self, request, *args, **kwargs):
        experiment_name = request.headers.get('experiment')
        context_name = request.headers.get('context')
        param = kwargs.get('id')
        try:
            experiment = Experiment.objects.get(name=experiment_name)
            context = Context.objects.get(
                name=context_name, experiment=experiment)
        except (Context.DoesNotExists, Experiment.DoesNotExists) as e:
            return ReturnResponse.return_404_not_found(str(e))

        if param:
        # check if exists - if not exists throw exception
            if not Question.objects.get(id=param):
                return ReturnResponse.return_404_not_found('question is not found')
            return ReturnResponse.return_200_success_get(self._init_dfs(context, father_id=param))
        else:
            # do regular dfs
            return ReturnResponse.return_200_success_get(self._init_dfs(context))

    def post(self, request):
        try:
            parent = Question.objects.get(id=request.data.get('parent_id')) if request.data.get('parent_id') else None
            related_answer = request.data.get('related_answer') if request.data.get('related_answer') else -1
            experiment_name = request.data.get('experiment')
            context_name = request.data.get('context')
            description = request.data.get('description')
            experiment = Experiment.objects.get(name=experiment_name)
            context = Context.objects.get(
                name=context_name, experiment=experiment)
        except (Context.DoesNotExists, Experiment.DoesNotExists) as e:
            return ReturnResponse.return_404_not_found(str(e))

        question = Question.objects.create(
            context=context, description=description, parent=parent, related_answer=related_answer)
        question.save()
        serializer = self.serializer_class(question)
        return ReturnResponse.return_201_success_post(serializer.data)

    def delete(self, request, *args, **kwargs):
        try:
            instance = Question.objects.get(id=kwargs['pk'])
        except Question.DoesNotExist as e:
            return ReturnResponse.return_400_bed_request(str(e))
        if not instance.children.exists():
            instance.delete()
            return ReturnResponse.return_200_success_get("deleted")
        else:
            return ReturnResponse.return_400_bed_request("Question is not children")

    def patch(self, request, *args, **kwargs):
        try:
            question = Question.objects.get(id=kwargs['pk'])
            if 'description' in request.data:
                question.description = request.data['description']
            if 'related_answer' in request.data:
                question.related_answer = request.data['related_answer']
            question.save()
            serialized_data = self.serializer_class(question).data
            return ReturnResponse.return_200_success_get(serialized_data)
        except Exception as e:
            return ReturnResponse.return_404_not_found(str(e))


class AnswerCreateListView(generics.GenericAPIView,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin,):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsExperimentAdminPermission]
    queryset = Answer.objects.all()

    def post(self, request):
        try:
            question_id = request.data.get('question_id')
            text = request.data.get('text')
            question = Question.objects.filter(id=question_id)[0]
            answer = Answer.objects.create(
                text=text,
                question=question,
            )
            answer.save()
            serializer = self.serializer_class(answer)
            return ReturnResponse.return_201_success_post(serializer.data)

        except Exception as e:
            return ReturnResponse.return_400_bed_request(str(e))

    def get(self, request, *args, **kwargs):
        param = request.query_params.get('question_id')
        try:
            question = Question.objects.get(id=param)
            answers = Answer.objects.filter(question=question)
            serialized_data = self.serializer_class(answers, many=True).data
            return ReturnResponse.return_200_success_get(serialized_data)
        except Question.DoesNotExist:
            return ReturnResponse.return_404_not_found("Question not found")
        except Exception as e:
            return ReturnResponse.return_500_internal_server_error(str(e))

    def delete(self, request, *args, **kwargs):
        answer_id = kwargs['pk']
        if len(Question.objects.filter(related_answer=answer_id)) == 0:
            try:
                Answer.objects.get(id=answer_id).delete()
                return ReturnResponse.return_200_success_get('deleted')
            except Answer.DoesNotExist as e:
                return ReturnResponse.return_400_bed_request(str(e))
            except Exception as e:
                return ReturnResponse.return_500_internal_server_error(str(e))
        else:
            return ReturnResponse.return_400_bed_request("This Answer has related question!")

    def patch(self, request, *args, **kwargs):
        try:
            instance = Answer.objects.get(id=kwargs['pk'])
            instance.text = request.data['text']
            instance.save()
            serialized_data = self.serializer_class(instance).data
            return ReturnResponse.return_200_success_get(serialized_data)
        except Exception as e:
            return ReturnResponse.return_400_bed_request(str(e))
        except Answer.DoesNotExist as e:
            return ReturnResponse.return_400_bed_request(str(e))


class PartipantSubmissionGet(generics.GenericAPIView):
    serializer_class = ParticipantSubmissionSerializer
    permission_classes = [IsAuthenticated, IsExperimentAdminPermission]
    queryset = ParticipantSubmission.objects.all()

    def get(self, request, args, **kwargs):
        experiment_id = request.GET('experiment_id')
        try:
            experiment = Experiment.objects.get(id=experiment_id)
            ret = self.queryset.filter(experiment=experiment)
            serialized = self.serializer_class(ret)
            return ReturnResponse.return_200_success_get(serialized.data)
        except (Experiment.DoesNotExist, ParticipantSubmission.DoesNotExist) as e:
            return ReturnResponse.return_404_not_found(str(e))
        except Exception as e:
            return ReturnResponse.return_500_internal_server_error(str(e))


class ParticipantSubmissionView(generics.GenericAPIView,
                            mixins.CreateModelMixin):
    serializer_class = ParticipantSubmissionSerializer
    authentication_classes = []  # remove authentication requirement
    permission_classes = [AllowAny]  # allow any user to access the view

    def post(self, request):
        try:
            participant_code = request.data.get('participant')
            context_id = request.data.get('context')
            question_id = request.data.get('question')
            answer_id = request.data.get('answer')

            participant = Participant.objects.get(
                participant_code=participant_code)
            context = Context.objects.get(id=context_id)
            question = Question.objects.get(id=question_id)
            answer = Answer.objects.get(id=answer_id)

            participant_submittion = ParticipantSubmission.objects.create(
                participant=participant,
                context=context,
                question=question,
                answer=answer
            )
            participant.score = participant.score + 10

            participant.save()
            participant_submittion.save()

            serializer = self.serializer_class(participant_submittion)
            return ReturnResponse.return_201_success_post(serializer.data)

        except Exception as e:
            return ReturnResponse.return_400_bed_request(str(e))


class ParticipantLoginView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = ParticipantSerializer
    authentication_classes = []  # remove authentication requirement
    permission_classes = [AllowAny]  # allow any user to access the view
    queryset = Participant.objects.all()

    def post(self, request):
        participant_code = request.data.get('participant')
        experiment_id = request.data.get('experiment_id')
        try:
            participant = Participant.objects.get(participant_code=participant_code)
            experiment = Experiment.objects.get(id=experiment_id)
        except (Participant.DoesNotExist, Experiment.DoesNotExist) as e:
            return ReturnResponse.return_404_not_found(str(e))
        return ReturnResponse.return_200_success_get("ok")

    def patch(self, request, *args, **kwargs):
        try:
            code = kwargs['pk']
            participant = Participant.objects.get(participant_code=code)
            participant.expo_token = request.data.get('token')
            participant.save()
            serialized = self.serializer_class(participant)
            return ReturnResponse.return_200_success_get(serialized.data)
        except Exception as e:
            return ReturnResponse.return_404_not_found(str(e))

    def get(self, request):
        code = request.query_params.get('code')
        try:
            data = self.queryset.get(participant_code=code)
            return ReturnResponse.return_200_success_get(data.score)
        except Exception as e:
            return ReturnResponse.return_404_not_found(str(e))

class ScheduleListView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated, IsExperimentAdminPermission]
# TODO_: create url with params
    def post(self, request):
        _participant_code = request.data.get('participant')
        _times = request.data.get('time')
        _experiment_id = request.data.get('experiment_id')
        _context_id = request.data.get('context_id')
        # check if the participant code exist and ok
        try:
            experiment = Experiment.objects.get(id=_experiment_id)
            participant = Participant.objects.get(participant_code=_participant_code)
            ParticipantExperiment.objects.get(experiment=experiment, participant=participant)
            context = Context.objects.get(id=_context_id)

        except Exception as e:
            return Response({"message":"participant or experiment not found!"}, status=status.HTTP_404_NOT_FOUND)
        # check if "time" is ok
        for _time in _times:
            try:
                schedule = Schedule.objects.create(participant=participant, experiment=experiment,
                                                context=context, ping_times=_time)
                schedule.save()
                # parsed_time = _time.split(":")
                # hour = int(parsed_time[0])
                # minute = int(parsed_time[1])
                # time_obj = datetime.time(hour=hour, minute=minute)
                # current_datetime = datetime.datetime.now()
                # schedule_eta = current_datetime.replace(hour=hour, minute=minute, second=0, microsecond=0)
                #
                # # schedule_eta = {
                # #     'minute': time_obj.minute,
                # #     'hour': time_obj.hour,
                # #     'day_of_week': '0-6',  # Sunday to Thursday
                # # }
                #
                # participant_token = participant.expo_token
                # task.apply_async(args=[participant_token], eta=schedule_eta)
            except Exception as e:
                return Response({"messeage":e}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "success"}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        param = request.query_params.get('experiment_id')
        data = []
        if not param:
            return ReturnResponse.return_400_bed_request("No experiment parameter!")
        try:
            experiment = Experiment.objects.get(id=param)
            schedule_data = Schedule.objects.filter(experiment=experiment)
            participant_experiment = ParticipantExperiment.objects.filter(experiment=experiment)
            for pe in participant_experiment:
                serialized_data = self.serializer_class(schedule_data.filter(participant_id=pe.id), many=True).data
                if serialized_data:
                    data.append(serialized_data)
            return ReturnResponse.return_200_success_get(data)
        except (Schedule.DoesNotExists, Experiment.DoesNotExists) as e:
            return ReturnResponse.return_404_not_found(str(e))
        except Exception as e:
            return ReturnResponse.return_500_internal_server_error(str(e))


# PARTICIPANT GET QUESTIONS
class QuestionForParticipantsListView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = ParticipantSerializer
    authentication_classes = []  # remove authentication requirement
    permission_classes = [AllowAny]  # allow any user to access the view

    def get(self, request, *args, **kwargs):
        try:
            context_id = request.data['context_id']
            participant_code = request.data['participant']
            experiment_id = request.data['experiment_id']
            experiment = Experiment.objects.get(id=experiment_id)
            participant = Participant.objects.get(participant_code=participant_code)
            ParticipantExperiment.objects.get(experiment=experiment, participant=participant)
            context = Context.objects.get(id=context_id, experiment=experiment)
            result = QuestionCreateList._init_dfs()
            return ReturnResponse.return_200_success_get(result)
        except (Experiment.DoesNotExists, Participant.DoesNotExists, ParticipantExperiment.DoesNotExists) as e:
            return ReturnResponse.return_400_bed_request(str(e))
        except Exception as e:
            return ReturnResponse.return_500_internal_server_error(str(e))
