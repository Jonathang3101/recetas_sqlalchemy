import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+mysqlconnector://root:12345678@localhost:3360/recetas_mariaDB')
Base = declarative_base()
Session = sessionmaker(bind=engine)




class Receta(Base):
    __tablename__ = 'recetas'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    ingredientes = Column(String(1000), nullable=False)
    pasos = Column(String(2000), nullable=False)


Base.metadata.create_all(engine)

#  agregar una nueva receta
def agregar_receta():
    nombre = input("Ingrese el nombre de la receta: ")
    ingredientes = input("Ingrese los ingredientes  ")
    pasos = input("Ingrese los pasos de la receta: ")

    nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, pasos=pasos)
    session = Session()
    session.add(nueva_receta)
    session.commit()
    print("Receta agregada correctamente.")
    session.close()

#  actualizar una receta existente
def actualizar_receta():
    id_receta = int(input("Ingrese el ID de la receta que desea actualizar: "))
    session = Session()
    receta = session.query(Receta).filter_by(id=id_receta).first()
    if receta:
        nueva_nombre = input("Ingrese el nuevo nombre de la receta : ")
        nuevos_ingredientes = input("Ingrese los nuevos ingredientes: ")
        nuevos_pasos = input("Ingrese los nuevos pasos de la receta : ")
        if nueva_nombre:
            receta.nombre = nueva_nombre
        if nuevos_ingredientes:
            receta.ingredientes = nuevos_ingredientes
        if nuevos_pasos:
            receta.pasos = nuevos_pasos
        session.commit()
        print("Receta actualizada correctamente.")
    else:
        print(" ")
    session.close()

#  eliminar una receta existente
def eliminar_receta():
    id_receta = int(input("Ingrese el ID de la receta que desea eliminar: "))
    session = Session()
    receta = session.query(Receta).filter_by(id=id_receta).first()
    if receta:
        session.delete(receta)
        session.commit()
        print("Receta eliminada correctamente.")
    else:
        print(" ")
    session.close()

#  ver el listado de recetas
def ver_recetas():
    session = Session()
    recetas = session.query(Receta).all()
    session.close()
    print("Listado de recetas:")
    for receta in recetas:
        print(f"{receta.id} - {receta.nombre}")

# buscar ingredientes y recetas 
def buscar_receta():
    ingrediente = input("Ingrese un ingrediente para buscar recetas que lo contengan: ")
    session = Session()
    recetas = session.query(Receta).filter(Receta.ingredientes.like(f"%{ingrediente}%")).all()
    session.close()
    print("Recetas que contienen el ingrediente:")
    for receta in recetas:
        print(f"ID: {receta.id} - Nombre: {receta.nombre}")
        print("Ingredientes:", receta.ingredientes)
        print("Pasos:", receta.pasos)
        print()


def main():
    while True:
        print("\n--- Menú ---")
        print("1) Agregar nueva receta")
        print("2) Actualizar receta existente")
        print("3) Eliminar receta existente")
        print("4) Ver listado de recetas")
        print("5) Buscar ingredientes y pasos de receta")
        print("6) Salir")
        opcion = input("Seleccione una opción: ").lower()
        if opcion == 1:
            agregar_receta()
        elif opcion == 2:
            actualizar_receta()
        elif opcion == 3:
            eliminar_receta()
        elif opcion == 4:
            ver_recetas()
        elif opcion == 5:
            buscar_receta()
        elif opcion == 6:
            print("Nos vemos!")
            break
        else:
            print("Inténtelo de nuevo.")

if __name__ == "__main__":
    main()
