import sqlalchemy as _sql
# вариант использования импорта

metadata = _sql.MetaData()

# способ 1 создания модели
# ИМПЕРАТИВНЫЙ

roles = _sql.Table(
    'roles',
    metadata,
    _sql.Column('id', _sql.Integer, primary_key=True),
    _sql.Column('role', _sql.String(30))
)

users = _sql.Table(
    'users',
    metadata,
    _sql.Column('id', _sql.Integer, primary_key=True),
    _sql.Column('email', _sql.String(50)),
    _sql.Column('username', _sql.String(50)),
    _sql.Column('password', _sql.String(255)),
    _sql.Column('first_name', _sql.String(50)),
    _sql.Column('second_name', _sql.String(50)),
    _sql.Column('role_id', _sql.Integer, _sql.ForeignKey('roles.id')),
)
