import reflex as rx
from app.states.governance_state import GovernanceState


def vendor_status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Active",
                "px-2 py-0.5 rounded-md text-xs font-medium bg-green-50 text-green-700 border border-green-200 w-fit",
            ),
            (
                "Suspended",
                "px-2 py-0.5 rounded-md text-xs font-medium bg-red-50 text-red-700 border border-red-200 w-fit",
            ),
            "px-2 py-0.5 rounded-md text-xs font-medium bg-gray-50 text-gray-700 border border-gray-200 w-fit",
        ),
    )


def vendors_view() -> rx.Component:
    return rx.fragment(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("truck", class_name="h-5 w-5 text-blue-600"),
                    rx.el.div(
                        rx.el.div(
                            "Vendors & Sources",
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.div(
                            f"{GovernanceState.active_vendor_count} active • {GovernanceState.suspended_vendor_count} suspended",
                            class_name="text-xs text-gray-500",
                        ),
                    ),
                    class_name="flex items-center gap-3",
                ),
                class_name="flex items-center justify-between p-4 border-b border-gray-200",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Vendor Name",
                        class_name="text-xs font-medium text-gray-600 mb-1 block",
                    ),
                    rx.el.input(
                        placeholder="Acme Reagents",
                        default_value=GovernanceState.new_vendor_name,
                        on_change=GovernanceState.set_new_vendor_name.debounce(
                            300
                        ),
                        class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Code",
                        class_name="text-xs font-medium text-gray-600 mb-1 block",
                    ),
                    rx.el.input(
                        placeholder="VEN-XXX",
                        default_value=GovernanceState.new_vendor_code,
                        on_change=GovernanceState.set_new_vendor_code.debounce(
                            300
                        ),
                        class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Category",
                        class_name="text-xs font-medium text-gray-600 mb-1 block",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option(
                                "Reagent Manufacturer",
                                value="Reagent Manufacturer",
                            ),
                            rx.el.option(
                                "Reference Standard", value="Reference Standard"
                            ),
                            rx.el.option("Glassware", value="Glassware"),
                            rx.el.option("Consumables", value="Consumables"),
                            rx.el.option("In-house", value="In-house"),
                            rx.el.option(
                                "Service Provider", value="Service Provider"
                            ),
                            value=GovernanceState.new_vendor_category,
                            on_change=GovernanceState.set_new_vendor_category,
                            class_name="appearance-none w-full pl-3 pr-8 py-2 text-sm border border-gray-200 rounded-lg bg-white text-gray-700 focus:outline-none focus:border-blue-500",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                        ),
                        class_name="relative",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Contact Person",
                        class_name="text-xs font-medium text-gray-600 mb-1 block",
                    ),
                    rx.el.input(
                        placeholder="Full name",
                        default_value=GovernanceState.new_vendor_contact,
                        on_change=GovernanceState.set_new_vendor_contact.debounce(
                            300
                        ),
                        class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Email",
                        class_name="text-xs font-medium text-gray-600 mb-1 block",
                    ),
                    rx.el.input(
                        placeholder="contact@vendor.com",
                        default_value=GovernanceState.new_vendor_email,
                        on_change=GovernanceState.set_new_vendor_email.debounce(
                            300
                        ),
                        class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Phone",
                        class_name="text-xs font-medium text-gray-600 mb-1 block",
                    ),
                    rx.el.input(
                        placeholder="+1 555 000 0000",
                        default_value=GovernanceState.new_vendor_phone,
                        on_change=GovernanceState.set_new_vendor_phone.debounce(
                            300
                        ),
                        class_name="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-3 px-4 py-4",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("plus", class_name="h-4 w-4"),
                    "Register Vendor",
                    on_click=GovernanceState.add_vendor,
                    class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg",
                ),
                class_name="px-4 py-3 border-t border-gray-200 flex justify-end",
            ),
            class_name="bg-white border border-gray-200 rounded-lg",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Vendor Directory",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="px-4 py-3 border-b border-gray-200",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Code",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Name",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Category",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Contact",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Last Audit",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="text-left text-xs font-semibold text-gray-600 px-4 py-2.5",
                            ),
                            rx.el.th("", class_name="px-4 py-2.5"),
                            class_name="bg-gray-50 border-b border-gray-200",
                        ),
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            GovernanceState.vendors,
                            lambda v: rx.el.tr(
                                rx.el.td(
                                    v["code"],
                                    class_name="text-xs font-mono text-gray-700 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    rx.el.div(
                                        rx.el.div(
                                            v["name"],
                                            class_name="text-sm font-medium text-gray-900",
                                        ),
                                        rx.el.div(
                                            v["notes"],
                                            class_name="text-xs text-gray-500 truncate max-w-xs",
                                        ),
                                    ),
                                    class_name="px-4 py-2.5",
                                ),
                                rx.el.td(
                                    v["category"],
                                    class_name="text-sm text-gray-700 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    rx.el.div(
                                        rx.el.div(
                                            v["contact_person"],
                                            class_name="text-sm text-gray-700",
                                        ),
                                        rx.el.div(
                                            v["email"],
                                            class_name="text-xs text-gray-500",
                                        ),
                                    ),
                                    class_name="px-4 py-2.5",
                                ),
                                rx.el.td(
                                    v["last_audit"],
                                    class_name="text-xs text-gray-600 px-4 py-2.5",
                                ),
                                rx.el.td(
                                    vendor_status_badge(v["status"]),
                                    class_name="px-4 py-2.5",
                                ),
                                rx.el.td(
                                    rx.el.button(
                                        rx.cond(
                                            v["status"] == "Active",
                                            "Suspend",
                                            "Activate",
                                        ),
                                        on_click=lambda: (
                                            GovernanceState.toggle_vendor_status(
                                                v["id"]
                                            )
                                        ),
                                        class_name="text-xs font-medium px-2 py-1 rounded-md border border-gray-200 hover:bg-gray-50 text-gray-700",
                                    ),
                                    class_name="px-4 py-2.5",
                                ),
                                class_name="border-b border-gray-100 hover:bg-blue-50/30",
                            ),
                        ),
                    ),
                    class_name="table-auto w-full",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
        ),
    )