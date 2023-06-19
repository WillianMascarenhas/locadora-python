from rest_framework import serializers
from movies.models import Options, Movie, MovieOrder
from users.serializers import LoginSerializer
from users.models import User


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, allow_null=True, default=None)
    rating = serializers.ChoiceField(choices=Options.choices, default=Options["G"])
    synopsis = serializers.CharField(allow_null=True, default=None)

    added_by = serializers.SerializerMethodField()


    def create(self, validated_data) -> Movie:
        return Movie.objects.create(**validated_data)
    
    def update(self, instance: Movie, validated_data: dict) -> Movie:
        for key, value in validated_data.items():
            setattr(instance, key, value)

            instance.save()
            # esse save salva a nova instancia no banco de dados

        return instance
    
    def get_added_by(self, obj: Movie) -> str:
        # lembrar que esta mudando o serializer.data e não validated_date na nora de retornar
        return obj.user.email
    

    
class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(source="movie.title", read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by= serializers.CharField(source="user.email", read_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data: dict) -> MovieOrder:
        return MovieOrder.objects.create(**validated_data)