import flet as ft
from conectar import Conectar
from clases import Interprete

conectando = Conectar()
cursor = conectando.cursor()


class InterpreteVista:


    def mostrar_lista(self, page: ft.Page, volver_menu):
        lista = ft.ListView(expand=True, spacing=8, padding=10)

        def cargar_lista():
            lista.controls.clear()
            try:
                cursor.execute("SELECT id_interprete, nombre, descripcion FROM interprete")
                resultados = cursor.fetchall()

                if not resultados:
                    lista.controls.append(ft.Text("No hay intérpretes registrados.", size=16))
                else:
                    for fila in resultados:
                        id_i, nombre, descripcion = fila
                        lista.controls.append(
                            ft.Row(controls=[
                                ft.Column(controls=[
                                    ft.Text(f"[{id_i}] {nombre}", size=15, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"   {descripcion[:60]}..." if descripcion and len(descripcion) > 60 else f"   {descripcion}", size=13),
                                ], expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Modificar",
                                    on_click=lambda e, id=id_i: self.mostrar_buscador_modificar(page, volver_menu, id)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_color="red",
                                    on_click=lambda e, id=id_i: self.eliminar_interprete(page, id, cargar_lista)
                                ),
                            ])
                        )
            except Exception as ex:
                lista.controls.append(ft.Text(f"Error: {ex}", color="red"))
            page.update()

        cargar_lista()

        boton_alta  = ft.ElevatedButton("Nuevo Intérprete", on_click=lambda e: self.mostrar_formulario_alta(page, volver_menu, cargar_lista))
        boton_volver = ft.ElevatedButton("<-- Volver al Menú", on_click=lambda e: volver_menu())

        page.clean()
        page.add(
            ft.Text("Gestión de Intérpretes", size=22, weight=ft.FontWeight.BOLD),
            ft.Row(controls=[boton_alta, boton_volver]),
            ft.Divider(),
            lista
        )
        page.update()


    def mostrar_formulario_alta(self, page: ft.Page, volver_menu, cargar_lista):
        formu_nombre      = ft.TextField(label="Nombre del Intérprete")
        formu_descripcion = ft.TextField(label="Descripción / Discografía relevante", multiline=True, min_lines=3)

        def registrar(e):
            interp = Interprete()
            interp.nombre      = formu_nombre.value.strip()
            interp.descripcion = formu_descripcion.value.strip()

            if not interp.nombre:
                page.snack_bar = ft.SnackBar(ft.Text("El nombre es obligatorio."), open=True)
                page.update()
                return

            try:
                cursor.execute(
                    "INSERT INTO interprete(nombre, descripcion) VALUES (%s, %s)",
                    (interp.nombre, interp.descripcion)
                )
                conectando.commit()
                page.snack_bar = ft.SnackBar(ft.Text(f"Intérprete '{interp.nombre}' registrado."), open=True)
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
            ft.Text("Alta de Intérprete", size=20, weight=ft.FontWeight.BOLD),
            formu_nombre,
            formu_descripcion,
            ft.Row(controls=[boton_registrar, boton_volver])
        )
        page.update()

  

    def eliminar_interprete(self, page, id_interprete, cargar_lista):
        try:
            cursor.execute("DELETE FROM interprete WHERE id_interprete = %s", (id_interprete,))
            conectando.commit()
            page.snack_bar = ft.SnackBar(ft.Text(f"Intérprete ID {id_interprete} eliminado."), open=True)
            page.update()
            cargar_lista()
        except Exception as ex:
            conectando.rollback()
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error al eliminar: {ex}"), open=True)
            page.update()



    def mostrar_buscador_modificar(self, page: ft.Page, volver_menu, id_preseleccionado=None):
        campo_id = ft.TextField(
            label="ID del Intérprete a modificar",
            keyboard_type=ft.KeyboardType.NUMBER,
            value=str(id_preseleccionado) if id_preseleccionado else ""
        )

        if id_preseleccionado:
            try:
                cursor.execute(
                    "SELECT id_interprete, nombre, descripcion FROM interprete WHERE id_interprete = %s",
                    (id_preseleccionado,)
                )
                resultado = cursor.fetchone()
                if resultado:
                    interp = Interprete()
                    interp.id_interprete = resultado[0]
                    interp.nombre        = resultado[1]
                    interp.descripcion   = resultado[2]
                    self.mostrar_formulario_modificar(page, interp, volver_menu)
                    return
            except Exception:
                pass

        def buscar(e):
            id_val = campo_id.value.strip()
            if not id_val:
                page.snack_bar = ft.SnackBar(ft.Text("Ingrese un ID."), open=True)
                page.update()
                return
            try:
                cursor.execute(
                    "SELECT id_interprete, nombre, descripcion FROM interprete WHERE id_interprete = %s",
                    (id_val,)
                )
                resultado = cursor.fetchone()
                if resultado:
                    interp = Interprete()
                    interp.id_interprete = resultado[0]
                    interp.nombre        = resultado[1]
                    interp.descripcion   = resultado[2]
                    self.mostrar_formulario_modificar(page, interp, volver_menu)
                else:
                    page.snack_bar = ft.SnackBar(ft.Text(f"No encontrado ID: {id_val}"), open=True)
                    page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
                page.update()

        boton_buscar = ft.ElevatedButton("Buscar", on_click=buscar)
        boton_volver = ft.ElevatedButton("<-- Volver", on_click=lambda e: self.mostrar_lista(page, volver_menu))

        page.clean()
        page.add(
            ft.Text("Modificar Intérprete — Buscar por ID", size=20, weight=ft.FontWeight.BOLD),
            campo_id,
            ft.Row(controls=[boton_buscar, boton_volver])
        )
        page.update()

    def mostrar_formulario_modificar(self, page, interp, volver_menu):
        formu_id          = ft.TextField(label="ID", value=str(interp.id_interprete), read_only=True)
        formu_nombre      = ft.TextField(label="Nombre", value=interp.nombre)
        formu_descripcion = ft.TextField(label="Descripción", value=interp.descripcion, multiline=True, min_lines=3)

        def guardar(e):
            try:
                cursor.execute(
                    "UPDATE interprete SET nombre=%s, descripcion=%s WHERE id_interprete=%s",
                    (formu_nombre.value, formu_descripcion.value, interp.id_interprete)
                )
                conectando.commit()
                page.snack_bar = ft.SnackBar(ft.Text("Intérprete modificado correctamente."), open=True)
                page.update()
                self.mostrar_lista(page, volver_menu)
            except Exception as ex:
                conectando.rollback()
                page.snack_bar = ft.SnackBar(ft.Text(f" Error: {ex}"), open=True)
                page.update()

        boton_guardar = ft.ElevatedButton("Guardar Cambios", on_click=guardar)
        boton_volver  = ft.ElevatedButton("<-- Volver", on_click=lambda e: self.mostrar_lista(page, volver_menu))

        page.clean()
        page.add(
            ft.Text("Modificar Intérprete", size=20, weight=ft.FontWeight.BOLD),
            formu_id,
            formu_nombre,
            formu_descripcion,
            ft.Row(controls=[boton_guardar, boton_volver])
        )
        page.update()