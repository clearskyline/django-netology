from rest_framework import serializers

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):
    students = serializers.StringRelatedField(many=True)

    class Meta:
        model = Course
        fields = ("id", "name", "students")
