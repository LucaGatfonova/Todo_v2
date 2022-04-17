import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from projects.models import Project, Todo
from users.models import User


# class ProjectType(DjangoObjectType):
#     class Meta:
#         model = Project
#         fields = '__all__'
#
#
# class Query(ObjectType):
#     all_projects = graphene.List(ProjectType)
#
#     def resolve_all_projects(root, info):
#         return Project.objects.all()
#
#
# schema = graphene.Schema(query=Query)


# class ProjectType(DjangoObjectType):
#     class Meta:
#         model = Project
#         fields = '__all__'
#
#
# class TodoType(DjangoObjectType):
#     class Meta:
#         model = Todo
#         fields = '__all__'
#
#
# class UserType(DjangoObjectType):
#     class Meta:
#         model = User
#         fields = '__all__'
#
#
# class Query(ObjectType):
#     project_by_id = graphene.Field(ProjectType, id=graphene.Int(required=False))
#     user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))
#     todo_by_user = graphene.List(TodoType, first_name=graphene.String(required=False))
#
#     def resolve_project_by_id(root, info, id=None):
#         if id:
#             try:
#                 return Project.objects.get(id=id)
#             except Project.DoesNotExist:
#                 return None
#         return Project.objects.all()
#
#     def resolve_user_by_id(root, info, id=None):
#         if id:
#             try:
#                 return User.objects.get(id=id)
#             except User.DoesNotExist:
#                 return None
#         return User.objects.all()
#
#     def resolve_todo_by_user(self, info, first_name=None):
#         todo = Todo.objects.all()
#         if first_name:
#             return todo.filter(user__first_name=first_name)
#         return todo
#
#
# schema = graphene.Schema(query=Query)


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = '__all__'


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class Query(ObjectType):
    project_by_id = graphene.Field(ProjectType, id=graphene.Int(required=False))
    user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))
    todo_by_user = graphene.List(TodoType, first_name=graphene.String(required=False))

    def resolve_project_by_id(root, info, id=None):
        if id:
            try:
                return Project.objects.get(id=id)
            except Project.DoesNotExist:
                return None
        return Project.objects.all()

    def resolve_user_by_id(root, info, id=None):
        if id:
            try:
                return User.objects.get(id=id)
            except User.DoesNotExist:
                return None
        return User.objects.all()

    def resolve_todo_by_user(self, info, first_name=None):
        todo = Todo.objects.all()
        if first_name:
            return todo.filter(user__first_name=first_name)
        return todo


class ProjectUpdateMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        id = graphene.ID()

    project = graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, name, id):
        project = Project.objects.get(id=id)
        project.name = name
        project.save()
        return ProjectUpdateMutation(project=project)


class ProjectCreateMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        repository_url = graphene.String()

    project = graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, name, repository_url):
        project = Project(name=name, repository_url=repository_url)
        project.save()
        return ProjectCreateMutation(project=project)


class ProjectDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    project = graphene.List(ProjectType)

    @classmethod
    def mutate(cls, root, info, id):
        Project.objects.get(id=id).delete()
        project = Project.objects.all()
        return ProjectDeleteMutation(project=project)


class Mutation(ObjectType):
    update_project = ProjectUpdateMutation.Field()
    create_project = ProjectUpdateMutation.Field()
    delete_project = ProjectDeleteMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


