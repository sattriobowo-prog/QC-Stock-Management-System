import reflex as rx
from app.states.auth_state import AuthState


def nav_link(label: str, icon: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-4 w-4"),
        rx.el.span(label, class_name="text-sm font-medium"),
        href=href,
        class_name="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition-colors",
    )


def nav_section(title: str) -> rx.Component:
    return rx.el.div(
        title,
        class_name="text-xs font-semibold text-gray-400 uppercase tracking-wider px-3 pt-4 pb-1",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("flask-conical", class_name="h-6 w-6 text-blue-600"),
                rx.el.div(
                    rx.el.div(
                        "QC Stock", class_name="text-sm font-bold text-gray-900"
                    ),
                    rx.el.div(
                        "Laboratory Management",
                        class_name="text-xs text-gray-500",
                    ),
                ),
                class_name="flex items-center gap-2 px-4 py-4 border-b border-gray-200",
            ),
            rx.el.nav(
                nav_section("Overview"),
                nav_link("Dashboard", "layout-dashboard", "/"),
                nav_section("Inventory"),
                nav_link("Items", "package", "/inventory"),
                nav_link("Lots & Batches", "boxes", "/lots"),
                nav_link("Locations", "map-pin", "/inventory"),
                nav_section("Operations"),
                nav_link("Material Requests", "clipboard-list", "/requests"),
                nav_link("Issue / Consume", "circle_minus", "/issue"),
                nav_link("Receiving", "circle_plus", "/receiving"),
                nav_link("Adjustments", "settings-2", "/adjustments"),
                nav_link("Transfers", "arrow-right-left", "/transfers"),
                nav_link("Expiry Tasks", "calendar-clock", "/expiry"),
                nav_section("Tools"),
                nav_link("Scan & Lookup", "scan-line", "/scan"),
                nav_link("Lot Labels", "tag", "/labels"),
                nav_link("Notifications", "bell", "/notifications"),
                nav_section("Governance"),
                nav_link("Vendors", "truck", "/vendors"),
                nav_link("Documents", "file-text", "/documents"),
                nav_link("Reports", "bar-chart-3", "/reports"),
                nav_link("Audit Trail", "shield-check", "/settings"),
                nav_section("System"),
                nav_link("Migration", "database", "/migration"),
                nav_link("Admin / Roles", "users", "/admin"),
                nav_link("Settings", "settings", "/settings"),
                class_name="flex flex-col gap-0.5 px-2 py-2 flex-1 overflow-y-auto",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.img(
                        src=f"https://api.dicebear.com/9.x/notionists/svg?seed={AuthState.current_user}",
                        class_name="size-9 rounded-full bg-blue-100",
                    ),
                    rx.el.div(
                        rx.el.div(
                            AuthState.current_user,
                            class_name="text-sm font-semibold text-gray-900 truncate",
                        ),
                        rx.el.div(
                            AuthState.current_role,
                            class_name="text-xs text-blue-600 font-medium",
                        ),
                        class_name="flex flex-col min-w-0",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="border-t border-gray-200 px-4 py-3",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="flex flex-col w-64 h-screen shrink-0 bg-white border-r border-gray-200 sticky top-0",
    )