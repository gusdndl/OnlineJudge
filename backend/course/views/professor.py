from django.http import request
from utils.api import APIView, validate_serializer

from account.models import User

from ..models import Course, Takes
from ..serializers import CourseSerializer, CreateCourseSerializer, CourseListSerializer, RegisterStudentSerializer, TakesSerializer

class CourseAPI(APIView):
    def get(self, request):
        cousre_id = request.GET.get("id")
        if cousre_id:
            try:
                course = Course.objects.get(id=cousre_id)
                return self.success(CourseSerializer(course).data)
            except Course.DoesNotExist:
                return self.error("Course does not exist")

        courses = Course.objects.filter(created_by=request.user)
        return self.success(self.paginate_data(request, courses, CourseSerializer))

    @validate_serializer(CreateCourseSerializer)
    def post(self, request):
        data = request.data
        course = Course.objects.create(title=data["title"],
                                        course_code=data["course_code"],
                                        class_number=data["class_number"],
                                        created_by=request.user,
                                        registered_year=data["registered_year"],
                                        semester=data["semester"])
        return self.success(CourseSerializer(course).data)


class StudentManagementAPI(APIView): # params? data? 
    @validate_serializer(RegisterStudentSerializer)
    def post(self, request):
        data = request.data
        course_id = data["course_id"]# request.GET.get('course_id')
        user_id = data["user_id"]# request.GET.get('user_id')

        try:
            Course.objects.get(id=course_id)
            User.objects.get(id=user_id)
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        except User.DoesNotExist:
            return self.error("User does not exist")

        try:
            Registration.objects.get(user_id=user_id, course_id=course_id)
            return self.error("User has been already registered to the course")
        except Registration.DoesNotExist:
            registration = Registration.objects.create(user_id=user_id,
                                        course_id=course_id)
        return self.success(RegistrationSerializer(registration).data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="course_id",
                in_=openapi.IN_QUERY,
                description="Unique ID of a course",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="count",
                in_=openapi.IN_QUERY,
                description="Return number of total registered user if 1( { 'total_students': registration count } )",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                description="Number of registration to show",
                type=openapi.TYPE_STRING,
                default=10,
            ),
            openapi.Parameter(
                name="offset",
                in_=openapi.IN_QUERY,
                description="ID of the first registration of list",
                type=openapi.TYPE_STRING,
                default=0,
            ),
        ],
        operation_description="Get contest list generated by requesting admin",
        responses={200: UserListSerializer},
    )
    @admin_role_required
    def get(self, request):
        course_id = request.GET.get("course_id")
        get_students_count = request.GET.get("count")

        if not course_id:
            return self.error("Invalid parameter, course_id is required")

        try: 
            course = Course.objects.get(id=course_id)
            ensure_created_by(course, request.user)
        except Course.DoesNotExist:
            return self.error("Course does not exist")

        registration = Registration.objects.filter(course_id=course_id)

        # Return number of total registered students
        if get_students_count == "1":
            return self.success({ 'total_students': registration.count() })
        return self.success(self.paginate_data(request, registration, UserListSerializer))

    @swagger_auto_schema(
        request_body=EditRegisterSerializer,
        operation_description="Change registered course of a user",
        responses={200: RegistrationSerializer},
    )
    @validate_serializer(EditRegisterSerializer)
    @admin_role_required
    def put(self, request):
        data = request.data
        course_id = data["course_id"]

        try:
            registration = Registration.objects.get(id=data.pop("registration_id"))
        except Registration.DoesNotExist:
            return self.error("Register information does not exist")

        try:
            course = Course.objects.get(id=course_id)
            ensure_created_by(course, request.user)
            course = Course.objects.get(id=registration.course_id)
            ensure_created_by(course, request.user)
        except Course.DoesNotExist:
            return self.error("Course does not exist")

        try:
            Registration.objects.get(user_id=registration.user_id, course_id=course_id)
            return self.error("User has been already registered to the course")
        except Registration.DoesNotExist:
            for k, v in data.items():
                setattr(registration, k, v)
            registration.save()
        return self.success(RegistrationSerializer(registration).data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="registration_id",
                in_=openapi.IN_QUERY,
                description="Id of registration to delete",
                required=True,
                type=openapi.TYPE_INTEGER,
            )
        ],
        operation_description="Delete a registered user",
    )
    @admin_role_required
    def delete(self, request):
        id = request.GET.get("registration_id")
        if not id:
            return self.error("Invalid parameter, registration_id is required")

        try:
            registration = Registration.objects.get(id=id)
            course = Course.objects.get(id=registration.course_id)
            ensure_created_by(course, request.user)
        except Registration.DoesNotExist:
            return self.error("Register information does not exists")

        registration.delete()
        return self.success()