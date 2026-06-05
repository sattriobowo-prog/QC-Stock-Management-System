import reflex as rx
from app.components.sidebar import sidebar
from app.states.auth_state import AuthState


def topbar(title: str, subtitle: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(title, class_name="text-xl font-semibold text-gray-900"),
            rx.el.p(subtitle, class_name="text-sm text-gray-500"),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("shield-check", class_name="h-3.5 w-3.5"),
                rx.el.span(
                    AuthState.current_role, class_name="text-xs font-medium"
                ),
                class_name="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 border border-blue-200",
            ),
            rx.el.button(
                rx.icon("bell", class_name="h-4 w-4"),
                class_name="p-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors relative",
            ),
            rx.el.button(
                rx.icon("circle-help", class_name="h-4 w-4"),
                class_name="p-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex items-center justify-between px-8 py-4 bg-white border-b border-gray-200 sticky top-0 z-10",
    )


def page_layout(title: str, subtitle: str, *content) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            topbar(title, subtitle),
            rx.el.div(
                *content,
                class_name="px-8 py-6 flex flex-col gap-6",
            ),
            class_name="flex-1 min-w-0 bg-gray-50 min-h-screen",
        ),
        class_name="flex min-h-screen w-full font-['Inter']",
    )