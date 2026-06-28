import flet as ft
from conectar import Conectar
from clases import Grabacion

conectando = Conectar()
cursor = conectando.cursor()


class GrabacionVista:



    def mostrar_lista(self, page: ft.Page, volver_menu):
        lista = ft.ListView(expand=True, spacing=8, padding=10)

        def cargar_lista():
            lista.controls.clear()
            try:
                cursor.execute("""
                    SELECT g.titulo, g.categoria, g.num_temas, g.descripcion, c.nombre
                    FROM grabaciones g
                    LEFT JOIN compania c ON g.id_compania = c.id_compania
                """)
                resultados = cursor.fetchall()

                if not resultados:
                    lista.controls.append(ft.Text("No hay grabaciones registradas.", size=16))
                else:
                    for fila in resultados:
                        titulo, categoria, num_temas, descripcion, compania = fila
                        lista.controls.append(
                            ft.Row(controls=[
                                ft.Column(controls=[
                                    ft.Text(f"{titulo}", size=15, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"   Categoría: {categoria} | Temas: {num_temas} | Compañía: {compania}", size=13),
                                ], expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Modificar",
                                    on_click=lambda e, t=titulo: self.mostrar_formulario_modificar_por_titulo(page, t, volver_menu)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_color="red",
                                    on_click=lambda e, t=titulo: self.eliminar_grabacion(page, t, cargar_lista)
                                ),
                            ])
                        )
            except Exception as ex:
                lista.controls.append(ft.Text(f"Error: {ex}", color="red"))
            page.update()

        cargar_lista()

        boton_alta  = ft.ElevatedButton("Nueva Grabación", on_click=lambda e: self.mostrar_formulario_alta(page, volver_menu, cargar_lista))
        boton_volver = ft.ElevatedButton("<-- Volver al Menú", on_click=lambda e: volver_menu())

        page.clean()
        page.add(
            ft.Text("Gestión de Grabaciones", size=22, weight=ft.FontWeight.BOLD),
            ft.Row(controls=[boton_alta, boton_volver]),
            ft.Divider(),
            lista
        )
        page.update()



    def mostrar_formulario_alta(self, page: ft.Page, volver_menu, cargar_lista):
        formu_titulo      = ft.TextField(label="Título")
        formu_categoria   = ft.TextField(label="Categoría (jazz, rock, ...)")
        formu_num_temas   = ft.TextField(label="Número de Temas", keyboard_type=ft.KeyboardType.NUMBER)
        formu_descripcion = ft.TextField(label="Descripción", multiline=True, min_lines=3)
        formu_id_compania = ft.TextField(label="ID Compañía", keyboard_type=ft.KeyboardType.NUMBER)

        def registrar(e):
            grab = Grabacion()
            grab.titulo      = formu_titulo.value.strip()
            grab.categoria   = formu_categoria.value.strip()
            grab.num_temas   = formu_num_temas.value.strip()
            grab.descripcion = formu_descripcion.value.strip()
            grab.id_compania = formu_id_compania.value.strip()

            if not grab.titulo:
                page.snack_bar = ft.SnackBar(ft.Text("El título es obligatorio."), open=True)
                page.update()
                return

            try:
                cursor.execute(
                    "INSERT INTO grabaciones(titulo, categoria, num_temas, descripcion, id_compania) VALUES (%s, %s, %s, %s, %s)",
                    (grab.titulo, grab.categoria, grab.num_temas, grab.descripcion, grab.id_compania or None)
                )
                conectando.commit()
                page.snack_bar = ft.SnackBar(ft.Text(f"Grabación '{grab.titulo}' registrada."), open=True)
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
            ft.Text("Alta de Grabación", size=20, weight=ft.FontWeight.BOLD),
            formu_titulo,
            formu_categoria,
            formu_num_temas,
            formu_descripcion,
            formu_id_compania,
            ft.Row(controls=[boton_registrar, boton_volver])
        )
        page.update()


    def eliminar_grabacion(self, page, titulo, cargar_lista):
        try:
            cursor.execute("DELETE FROM grabaciones WHERE titulo = %s", (titulo,))
            conectando.commit()
            page.snack_bar = ft.SnackBar(ft.Text(f"Grabación '{titulo}' eliminada."), open=True)
            page.update()
            cargar_lista()
        except Exception as ex:
            conectando.rollback()
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"), open=True)
            page.update()


    def mostrar_formulario_modificar_por_titulo(self, page, titulo, volver_menu):
        try:
            cursor.execute(
                "SELECT titulo, categoria, num_temas, descripcion, id_compania FROM grabaciones WHERE titulo = %s",
                (titulo,)
            )
            resultado = cursor.fetchone()
            if resultado:
                grab = Grabacion()
                grab.titulo      = resultado[0]
                grab.categoria   = resultado[1]
                grab.num_temas   = resultado[2]
                grab.descripcion = resultado[3]
                grab.id_compania = resultado[4]
                self.mostrar_formulario_modificar(page, grab, volver_menu)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {ex}"), open=True)
            page.update()

    def mostrar_buscador_modificar(self, page: ft.Page, volver_menu):
        campo_titulo = ft.TextField(label="Título de la grabación a modificar")

        def buscar(e):
            titulo = campo_titulo.value.strip()
            if not titulo:
                page.snack_bar = ft.SnackBar(ft.Text("Ingrese un título."), open=True)
                page.update()
                return
            try:
                cursor.execute(
                    "SELECT titulo, categoria, num_temas, descripcion, id_compania FROM grabaciones WHERE titulo = %s",
                    (titulo,)
                )
                resultado = cursor.fetchone()
                if resultado:
                    grab = Grabacion()
                    grab.titulo      = resultado[0]
                    grab.categoria   = resultado[1]
                    grab.num_temas   = resultado[2]
                    grab.descripcion = resultado[3]
                    grab.id_compania = resultado[4]
                    self.mostrar_formulario_modificar(page, grab, volver_menu)
                else:
                    page.snack_bar = ft.SnackBar(ft.Text(f"No encontrada: {titulo}"), open=True)
                    page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {ex}"), open=True)
                page.update()

        boton_buscar = ft.ElevatedButton("Buscar", on_click=buscar)
        boton_volver = ft.ElevatedButton("<-- Volver", on_click=lambda e: self.mostrar_lista(page, volver_menu))

        page.clean()
        page.add(
            ft.Text("Modificar Grabación — Buscar por Título", size=20, weight=ft.FontWeight.BOLD),
            campo_titulo,
            ft.Row(controls=[boton_buscar, boton_volver])
        )
        page.update()

    def mostrar_formulario_modificar(self, page, grab, volver_menu):
        formu_titulo      = ft.TextField(label="Título", value=grab.titulo, read_only=True)
        formu_categoria   = ft.TextField(label="Categoría", value=grab.categoria)
        formu_num_temas   = ft.TextField(label="Número de Temas", value=str(grab.num_temas), keyboard_type=ft.KeyboardType.NUMBER)
        formu_descripcion = ft.TextField(label="Descripción", value=grab.descripcion, multiline=True, min_lines=3)
        formu_id_compania = ft.TextField(label="ID Compañía", value=str(grab.id_compania) if grab.id_compania else "")

        def guardar(e):
            try:
                cursor.execute(
                    "UPDATE grabaciones SET categoria=%s, num_temas=%s, descripcion=%s, id_compania=%s WHERE titulo=%s",
                    (formu_categoria.value, formu_num_temas.value, formu_descripcion.value,
                     formu_id_compania.value or None, grab.titulo)
                )
                conectando.commit()
                page.snack_bar = ft.SnackBar(ft.Text("Grabación modificada correctamente."), open=True)
                page.update()
                self.mostrar_lista(page, volver_menu)
            except Exception as ex:
                conectando.rollback()
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
                page.update()

        boton_guardar = ft.ElevatedButton("Guardar Cambios", on_click=guardar)
        boton_volver  = ft.ElevatedButton("<-- Volver", on_click=lambda e: self.mostrar_lista(page, volver_menu))

        page.clean()
        page.add(
            ft.Text("Modificar Grabación", size=20, weight=ft.FontWeight.BOLD),
            formu_titulo,
            formu_categoria,
            formu_num_temas,
            formu_descripcion,
            formu_id_compania,
            ft.Row(controls=[boton_guardar, boton_volver])
        )
        page.update()