import graphene


class Picture(graphene.ObjectType):
    id = graphene.ID()
    # @TODO Impement custom scalar for picture url
    url = graphene.String()


class Query(graphene.ObjectType):
    pictures = graphene.List(Picture)
    picture = graphene.Field(Picture)

    def resolve_pictures(root, info):
        return [{'id': 'uuid', 'url': 'https://saintmtool.net/'}]

    def resolve_picture(root, info):
        return {'id': 'some_id', 'url': 'https://saintmtool.net'}


schema = graphene.Schema(query=Query)