import graphene


class Picture(graphene.ObjectType):
    id = graphene.ID()
    # @TODO Impement custom scalar for picture url
    high_url = graphene.String()
    medium_url = graphene.String()
    original_url = graphene.String()
    small_url = graphene.String()


class Query(graphene.ObjectType):
    pictures = graphene.List(Picture)
    picture = graphene.Field(Picture, picture_id=graphene.String(required=True))

    async def resolve_pictures(root, info):
        return [{'id': 'uuid', 'small_url': 'https://saintmtool.net/'}]

    async def resolve_picture(root, info, picture_id: str):
        return {'id': 'some_id', 'smallUrl': 'https://saintmtool.net'}


schema = graphene.Schema(query=Query)