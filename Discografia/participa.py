import flet as ft
from conectar import Conectar
from clases import Participa

conectando = Conectar()
cursor = conectando.cursor()


class ParticipaVista:



    def mostrar_lista(self, page: ft.Page, volver_menu):
        lista = ft.ListView(expand=True, spacing=8, padding=10)

        def cargar_lista():
            lista.controls.clear()
            try:
                cursor.execute("""
                    SELECT p.id_interprete, i.nombre, p.titulo, p.fecha
                    FROM participa p
                    JOIN interprete i ON p.id_interprete = i.id_interprete
                    ORDER BY p.fecha DESC
                """)
                resultados = cursor.fetchall()

                if not resultados:
                    lista.controls.append(ft.Text("No hay participaciones registradas.", size=16))
                else:
                    for fila in resultados:
                        id_i, nombre, titulo, fecha = fila
                        lista.controls.append(
                            ft.Row(controls=[
                                ft.Text(
                                    f" {nombre}:'{titulo}'  |  Fecha: {fecha}",
                                    size=14, expand=True
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar participación",
                                    icon_color="red",
                                    on_click=lambda e, id=id_i, t=titulo: self.eliminar_participacion(page, id, t, cargar_lista)
                                ),
                            ])
                        )
            except Exception as ex:
                lista.controls.append(ft.Text(f"Error: {ex}", color="red"))
            page.update()

        cargar_lista()

        boton_alta  = ft.ElevatedButton("Nueva Participación", on_click=lambda e: self.mostrar_formulario_alta(page, volver_menu, cargar_lista))
        boton_volver = ft.ElevatedButton("<-- Volver al Menú", on_click=lambda e: volver_menu())

        page.clean()
        page.add(
            ft.Text("Gestión de Participaciones", size=22, weight=ft.FontWeight.BOLD),
            ft.Row(controls=[boton_alta, boton_volver]),
            ft.Divider(),
            lista
        )
        page.update()



    def mostrar_formulario_alta(self, page: ft.Page, volver_menu, cargar_lista):
        formu_id_interprete = ft.TextField(label="ID del Intérprete", keyboard_type=ft.KeyboardType.NUMBER)
        formu_titulo        = ft.TextField(label="Título de la Grabación")
        formu_fecha         = ft.TextField(label="Fecha de Participación (AAAA-MM-DD)")

        def registrar(e):
            part = Participa()
            part.id_interprete = formu_id_interprete.value.strip()
            part.titulo        = formu_titulo.value.strip()
            part.fecha         = formu_fecha.value.strip()

            if not part.id_interprete or not part.titulo or not part.fecha:
                page.snack_bar = ft.SnackBar(ft.Text(" Todos los campos son obligatorios."), open=True)
                page.update()
                return

            try:
                cursor.execute(
                    "INSERT INTO participa(id_interprete, titulo, fecha) VALUES (%s, %s, %s)",
                    (part.id_interprete, part.titulo, part.fecha)
                )
                conectando.commit()
                page.snack_bar = ft.SnackBar(ft.Text("Participación registrada correctamente."), open=True)
                page.update()
                self.mostrar_lista(page, volver_menu)
            except Exception as ex:
                conectando.rollback()
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
                page.update()

        boton_registrar = ft.ElevatedButton("Registrar", on_click=registrar)
        boton_volver    = ft.ElevatedButton("<-- Volver", on_click=lambda e: self.mostrar_lista(page, volver_menu))

        page.clean()
        page.add(
            ft.Text("Alta de Participación", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("Relaciona un intérprete con una grabación y la fecha en que participó.", size=13, color="grey"),
            formu_id_interprete,
            formu_titulo,
            formu_fecha,
            ft.Row(controls=[boton_registrar, boton_volver])
        )
        page.update()


    def eliminar_participacion(self, page, id_interprete, titulo, cargar_lista):
        try:
            cursor.execute(
                "DELETE FROM participa WHERE id_interprete = %s AND titulo = %s",
                (id_interprete, titulo)
            )
            conectando.commit()
            page.snack_bar = ft.SnackBar(ft.Text("Participación eliminada."), open=True)
            page.update()
            cargar_lista()
        except Exception as ex:
            conectando.rollback()
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"), open=True)
            page.update()