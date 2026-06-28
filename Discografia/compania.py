import flet as ft
from conectar import Conectar
from clases import Compania

conectando = Conectar()
cursor = conectando.cursor()


class CompaniaVista:



    def mostrar_lista(self, page: ft.Page, volver_menu):
        """Pantalla principal: lista todas las compañías con botones de acción."""

        lista = ft.ListView(expand=True, spacing=8, padding=10)

        def cargar_lista():
            lista.controls.clear()
            try:
                cursor.execute("SELECT id_compania, nombre, direccion FROM compania")
                resultados = cursor.fetchall()

                if not resultados:
                    lista.controls.append(ft.Text("No hay compañías registradas.", size=16))
                else:
                    for fila in resultados:
                        id_c, nombre, direccion = fila
                        lista.controls.append(
                            ft.Row(controls=[
                                ft.Text(f"[{id_c}] {nombre} — {direccion}", size=15, expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Modificar",
                                    on_click=lambda e, id=id_c: self.mostrar_buscador_modificar(page, volver_menu, id)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_color="red",
                                    on_click=lambda e, id=id_c: self.eliminar_compania(page, id, cargar_lista)
                                ),
                            ])
                        )
            except Exception as ex:
                lista.controls.append(ft.Text(f"Error al cargar: {ex}", color="red"))
            page.update()

        cargar_lista()

        boton_alta = ft.ElevatedButton(
            " Nueva Compañía",
            on_click=lambda e: self.mostrar_formulario_alta(page, volver_menu, cargar_lista)
        )
        boton_volver = ft.ElevatedButton(
            "<-- Volver al Menú",
            on_click=lambda e: volver_menu()
        )

        page.clean()
        page.add(
            ft.Text("Gestión de Compañías", size=22, weight=ft.FontWeight.BOLD),
            ft.Row(controls=[boton_alta, boton_volver]),
            ft.Divider(),
            lista
        )
        page.update()


    def mostrar_formulario_alta(self, page: ft.Page, volver_menu, cargar_lista):
        """Formulario para registrar una nueva compañía."""

        formu_nombre    = ft.TextField(label="Nombre de la Compañía")
        formu_direccion = ft.TextField(label="Dirección")

        def registrar(e):
            comp = Compania()
            comp.nombre    = formu_nombre.value.strip()
            comp.direccion = formu_direccion.value.strip()

            if not comp.nombre:
                page.snack_bar = ft.SnackBar(ft.Text(" El nombre es obligatorio."), open=True)
                page.update()
                return

            try:
                cursor.execute(
                    "INSERT INTO compania(nombre, direccion) VALUES (%s, %s)",
                    (comp.nombre, comp.direccion)
                )
                conectando.commit()
                page.snack_bar = ft.SnackBar(ft.Text(f"Compañía '{comp.nombre}' registrada."), open=True)
                page.update()
                self.mostrar_lista(page, volver_menu)
            except Exception as ex:
                conectando.rollback()
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {ex}"), open=True)
                page.update()

        boton_registrar = ft.ElevatedButton("Registrar", on_click=registrar)
        boton_volver    = ft.ElevatedButton("<-- Volver", on_click=lambda e: self.mostrar_lista(page, volver_menu))

        page.clean()
        page.add(
            ft.Text("Alta de Compañía", size=20, weight=ft.FontWeight.BOLD),
            formu_nombre,
            formu_direccion,
            ft.Row(controls=[boton_registrar, boton_volver])
        )
        page.update()

   

    def eliminar_compania(self, page, id_compania, cargar_lista):
        """Elimina una compañía por su ID."""
        try:
            cursor.execute("DELETE FROM compania WHERE id_compania = %s", (id_compania,))
            conectando.commit()
            page.snack_bar = ft.SnackBar(ft.Text(f"Compañía ID {id_compania} eliminada."), open=True)
            page.update()
            cargar_lista()
        except Exception as ex:
            conectando.rollback()
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"), open=True)
            page.update()

 

    def mostrar_buscador_modificar(self, page: ft.Page, volver_menu, id_preseleccionado=None):
        """Busca la compañía por ID para modificar."""

        campo_id = ft.TextField(
            label="ID de la Compañía a modificar",
            keyboard_type=ft.KeyboardType.NUMBER,
            value=str(id_preseleccionado) if id_preseleccionado else ""
        )

        def buscar(e):
            id_val = campo_id.value.strip()
            if not id_val:
                page.snack_bar = ft.SnackBar(ft.Text("Ingrese un ID."), open=True)
                page.update()
                return
            try:
                cursor.execute(
                    "SELECT id_compania, nombre, direccion FROM compania WHERE id_compania = %s",
                    (id_val,)
                )
                resultado = cursor.fetchone()
                if resultado:
                    comp = Compania()
                    comp.id_compania = resultado[0]
                    comp.nombre      = resultado[1]
                    comp.direccion   = resultado[2]
                    self.mostrar_formulario_modificar(page, comp, volver_menu)
                else:
                    page.snack_bar = ft.SnackBar(ft.Text(f"No se encontró compañía con ID: {id_val}"), open=True)
                    page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
                page.update()

        if id_preseleccionado:
            try:
                cursor.execute(
                    "SELECT id_compania, nombre, direccion FROM compania WHERE id_compania = %s",
                    (id_preseleccionado,)
                )
                resultado = cursor.fetchone()
                if resultado:
                    comp = Compania()
                    comp.id_compania = resultado[0]
                    comp.nombre      = resultado[1]
                    comp.direccion   = resultado[2]
                    self.mostrar_formulario_modificar(page, comp, volver_menu)
                    return
            except Exception as ex:
                pass

        boton_buscar = ft.ElevatedButton("Buscar", on_click=buscar)
        boton_volver = ft.ElevatedButton("<-- Volver", on_click=lambda e: self.mostrar_lista(page, volver_menu))

        page.clean()
        page.add(
            ft.Text("Modificar Compañía — Buscar por ID", size=20, weight=ft.FontWeight.BOLD),
            campo_id,
            ft.Row(controls=[boton_buscar, boton_volver])
        )
        page.update()

    def mostrar_formulario_modificar(self, page: ft.Page, comp, volver_menu):
        """Formulario con datos cargados para editar."""

        formu_id        = ft.TextField(label="ID", value=str(comp.id_compania), read_only=True)
        formu_nombre    = ft.TextField(label="Nombre", value=comp.nombre)
        formu_direccion = ft.TextField(label="Dirección", value=comp.direccion)

        def guardar(e):
            try:
                cursor.execute(
                    "UPDATE compania SET nombre = %s, direccion = %s WHERE id_compania = %s",
                    (formu_nombre.value.strip(), formu_direccion.value.strip(), comp.id_compania)
                )
                conectando.commit()
                page.snack_bar = ft.SnackBar(ft.Text("Compañía modificada correctamente."), open=True)
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
            ft.Text("Modificar Compañía", size=20, weight=ft.FontWeight.BOLD),
            formu_id,
            formu_nombre,
            formu_direccion,
            ft.Row(controls=[boton_guardar, boton_volver])
        )
        page.update()