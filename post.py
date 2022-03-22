from dao import DAO
import user

class Post:
    def __init__(self, user_id, title, contents, created, last_edit = None) -> None:
        self.user_id = user_id
        self.title = title
        self.contents = contents
        self.created = created
        self.last_edit = last_edit or created

class PostDisplayInfo:
    def __init__(self, post: Post, author: user.User) -> None:
        self.post = post
        self.author = author

class PostDAO(DAO):
    def _get_table_name(self):
        return 'posts'

    def _data(self, post: Post):
        return (post.user_id, post.title, post.contents, post.created, post.last_edit)

    def _store_sql(self):
        return f'''INSERT INTO {self._get_table_name()}
                    VALUES (:author, :title, :contents, :created, :edited)'''

    def create_table(self):
        sql = f'''CREATE TABLE IF NOT EXISTS {self._get_table_name()}
                        (author int, title text, contents text,
                         created date, edited date)'''
        self.cursor.execute(sql)

    def fetch_all(self):
        tname = self._get_table_name()
        entries = []
        for entry in self.cursor.execute(f'''SELECT rowid, * FROM {tname}
                                             ORDER BY created DESC'''):
            entries.append(entry)
        return list(map(lambda tup: Post(tup[1],
                                         tup[2],
                                         tup[3],
                                         tup[4],
                                         tup[5]),
                        entries))

    def fetch_all_display(self):
        posts = self.fetch_all()
        dposts = []
        userDAO = user.UserDAO()
        for p in posts:
            author_id = p.user_id
            usr = userDAO.get_user_by_id(author_id)
            dposts.append(PostDisplayInfo(p, usr))
        return dposts
    
    def fetch_by_user(self, username: str):
        user_table = 'users'
        post_table = self._get_table_name()
        sql = f'''SELECT {user_table}.username,
                         {user_table}.key,
                         {user_table}.salt,
                         {post_table}.author,
                         {post_table}.title,
                         {post_table}.created,
                         {post_table}.edited,
                         {post_table}.contents
                  FROM {user_table} INNER JOIN {post_table}
                  ON {user_table}.rowid = {post_table}.author
                  WHERE {user_table}.username = :username
                  ORDER BY {post_table}.created DESC'''
        res = self.cursor.execute(sql, (username,))
        dposts = []
        for row in res:
            username = row[0]
            key = row[1]
            salt = row[2]
            author_id = row[3]
            title = row[4]
            created = row[5]
            edited = row[6]
            contents = row[7]
            dposts.append(PostDisplayInfo(
                            Post(author_id, title, contents, created, edited),
                            user.User(username, key, salt)))
        return dposts