from flask_app.config.mysqlconnection import connectToMySQL

class Musica:
    def __init__(self, data ):
        self.id = data['id']
        self.name_music = data['name_music']
        self.music = data['music']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query="INSERT INTO musica_tabla (name_music , music) VALUES ( %(name_music)s , %(music)s );"
        return connectToMySQL('schema_musica').query_db( query, data )

    @classmethod
    def get_all(cls, name_music, music):
        query ="SELECT * FROM musica_tabla WHERE (name_music = %(name_music)s) and (music = %(music)s);"
        results = connectToMySQL('schema_musica').query_db(query, id)
        print("QUE HAY AQUI?", results)
        musica_result = []
        for musica in results:
            musica_result.append( cls(musica) )
        return musica_result

    @classmethod
    def get_one(cls, data):
        query="SELECT * FROM musica_tabla WHERE name_music = %(name_music)s;"
        results = connectToMySQL('schema_musica').query_db(query, data)
        print("QUE HAY AQUI?", results)
        if len(results) < 1:
            return False
        print("RETORNO GET EMAIL:",results)
        return cls(results[0])