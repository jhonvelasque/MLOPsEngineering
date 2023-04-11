import psycopg2

conexion = psycopg2.connect(
   host='dpg-cgqabgseooggt0vd6d20-a.oregon-postgres.render.com',
   user='movie_m8dy_user',
   password='WMCe34LEJp5xWHMBqw85EAjqm5wEgxdL',
   dbname='movie_m8dy'   
)
cursor = conexion.cursor()