database_url = "postgres://movie_m8dy_user:WMCe34LEJp5xWHMBqw85EAjqm5wEgxdL@dpg-cgqabgseooggt0vd6d20-a.oregon-postgres.render.com/movie_m8dy"
#creando motor de base de datos

engine = create_engine(database_url, echo=True)
#conector 
conn=engine.connect()
meta=MetaData()
#conecotor a base de datos 
Session = sessionmaker(bind=engine)
Base = declarative_base()
